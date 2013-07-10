import maya.cmds as cmds

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('dmptoolsShelf')
PARENT = 'popup_custom'
WINDOWNAME = 'createCustomItem'

def removeItemsUI():
    """ ui that popup when the user right click on 'remove item' from the custom shelf
        it shows a list of the custom items created and saved in the settings file.
    """
    win = cmds.window(title='edit/remove custom items')
    form = cmds.formLayout()
    txt = cmds.textScrollList('item_list', allowMultiSelection=True, deleteKeyCommand=removeItems)
    for item in SETTINGS.getAll():
        name = cmds.menuItem(item.keys(), q=True, label=True)
        command = cmds.menuItem(item.keys(), q=True, command=True)
        sourceType = cmds.menuItem(item.keys(), q=True, sourceType=True)
        textScroll = cmds.textScrollList('item_list', e=True, append=name+' - '+command+' - '+sourceType)
        pop = cmds.popupMenu(p=textScroll, b=3)
        cmds.menuItem(p=pop, l='edit selected item', c=editItem)
        cmds.menuItem(p=pop, l='remove selected items', c=removeItems)
    cmds.formLayout(form, e=True, attachForm = [(txt, 'top', 5),(txt, 'bottom', 5), (txt, 'left', 5), (txt, 'right', 5)])
    # displays the window    
    cmds.showWindow(win)

def editItem(none=None):
    """ edit selected custom item """
    cmds.window('customEditItem', t='add custom item', s=False)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    name = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[0]
    command = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[1]
    sourceType = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[2]
    if sourceType == 'python':
        value = 1
    else:
        value = 2
    cmds.textFieldGrp('customname', label='name', text=name)
    cmds.textFieldGrp('customCommand', label='command', text=command)
    cmds.radioButtonGrp('customSourceRadioButton',label='source:', nrb=2, l1='python', l2='mel', select=value)
    cmds.separator('customSeparator', style='in')
    cmds.button(l='edit', command="print 'edit item!'")
    # displays the window
    cmds.showWindow('customEditItem')

def removeItems(none=None):
    """ remove item from popup menu and from the settings file """
    items = cmds.textScrollList('item_list', q=True, si=True)
    if items:
        cmds.textScrollList('item_list', e=True, ri=items)
        for item in items:
            key = item.split(' - ')
            for setting in SETTINGS.getAll():
                if key == setting.values()[0]:
                    cmds.deleteUI(setting.keys()[0], mi=True)
                    SETTINGS.remove(setting.keys()[0])

def checkSavedItems():
    """ check if there's custom items in the settings file and add them to the shelf """
    allItems = SETTINGS.getAll()
    if allItems:
        for item in allItems:
            # get name and command and create the menu item
            itemName = item.values()[0][0]
            itemCommand = item.values()[0][1]
            sourceType = item.values()[0][2]
            menuItem = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand, sourceType=sourceType)
            # remove old otem
            SETTINGS.remove(item.keys()[0])
            # add fresh one
            SETTINGS.add(menuItem, [itemName, itemCommand, sourceType])

def createItem(none=None):
    """ create/add the custom item to the shelf and save the item to the settings file """
    itemName = cmds.textFieldGrp('customname', q=True, text=True)
    itemCommand = cmds.textFieldGrp('customCommand', q=True, text=True)
    value = cmds.radioButtonGrp('customSourceRadioButton', q=True, select=True)
    if not itemName or not itemCommand or not value:
        raise UserWarning('You need to fill all the fields!')
    if value == 1:
        sourceType = 'python'
    else:
        sourceType = 'mel'
    cmds.deleteUI(WINDOWNAME, window=True)
    # create the custom item
    item = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand, sourceType=sourceType, ob=True)
    SETTINGS.add(item, [itemName, itemCommand, sourceType])

def addItemUI():
    """ create the ui that asks for the name, command and source type of the custom item """
    cmds.window(WINDOWNAME, t='add custom item', s=False)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('customname', label='name', text='')
    cmds.textFieldGrp('customCommand', label='command', text='')
    cmds.radioButtonGrp('customSourceRadioButton',label='source:', nrb=2, l1='python', l2='mel', select=1)
    cmds.separator('customSeparator', style='in')
    cmds.button(l='add', command=createItem)
    # displays the window
    cmds.showWindow(WINDOWNAME)

def addItem():
    """
     main function that displays the ui asking for the
     name, command and source type of the new custom item.
    """
    addItemUI()

