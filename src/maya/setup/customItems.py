import maya.cmds as cmds

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('dmptoolsShelf')
PARENT = 'dmptools_popup_custom'
WINDOWNAME = 'create_createCustomItem'

def deleteWindow(name):
    """ delete the window if exists """
    if cmds.window(name, q=True, ex=True):
        cmds.deleteUI(name, window=True)

def editItemUI(none=None):
    """ display the UI to edit selected custom item """
    deleteWindow('edit_customEditItem')
    cmds.window('edit_customEditItem', t='edit custom item', s=False)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    # get the name, command, type
    name = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[0]
    command = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[1]
    sourceType = cmds.textScrollList('item_list', q=True, si=True)[0].split(' - ')[2]
    # set the value 1: python 2: mel
    if sourceType == 'python':
        value = 1
    else:
        value = 2
    # set the fields
    cmds.textFieldGrp('edit_customname', label='name', text=name)
    cmds.textFieldGrp('edit_customCommand', label='command', text=command)
    cmds.radioButtonGrp('edit_customSourceRadioButton',label='source:', nrb=2, l1='python', l2='mel', select=value)
    cmds.separator('edit_customSeparator', style='in')
    cmds.button(l='edit', command=editItem)
    # displays the window
    cmds.showWindow('edit_customEditItem')

def editItem(none=None):
    """ first edit the item in the edit/remove UI
        then edit the item in the shelf and last edit the item in the settings file
    """
    # get edited item values
    itemName = cmds.textFieldGrp('edit_customname', q=True, text=True)
    itemCommand = cmds.textFieldGrp('edit_customCommand', q=True, text=True)
    value = cmds.radioButtonGrp('edit_customSourceRadioButton', q=True, select=True)
    if not itemName or not itemCommand or not value:
        raise UserWarning('You need to fill all the fields!')
    if value == 1:
        sourceType = 'python'
    else:
        sourceType = 'mel'
    itemFull = itemName+' - '+itemCommand+' - '+sourceType
    
    # delete the edit item window
    cmds.deleteUI('edit_customEditItem', window=True)
    
    # delete the old scrollList entry and insert the new one at the same place
    scrollItemSelected = cmds.textScrollList('item_list', q=True, si=True)[0]
    scrollItemIndex = cmds.textScrollList('item_list', q=True, sii=True)[0]
    cmds.textScrollList('item_list', e=True, ri=scrollItemSelected)
    cmds.textScrollList('item_list', e=True, appendPosition=[scrollItemIndex, itemFull], doubleClickCommand='editItemUI')

    # get the path of the shelf item to edit
    for item in SETTINGS.getAll():
        if item.values()[0][0] == scrollItemSelected.split(' - ')[0]:
            menuItemPath = item.keys()[0]
            cmds.menuItem(menuItemPath, e=True, label=itemName, command=itemCommand, sourceType=sourceType)
            SETTINGS.add(menuItemPath, [itemName, itemCommand, sourceType])

def editRemoveItemsUI():
    """ ui that pops up when the user right click on 'remove item' from the custom shelf
        it shows a list of the custom items created and saved in the settings file.
    """
    deleteWindow('editRemoveItems')
    cmds.window('editRemoveItems', title='edit/remove custom items')
    form = cmds.formLayout()
    txt = cmds.textScrollList('item_list', allowMultiSelection=True, deleteKeyCommand=removeItems)
    for item in SETTINGS.getAll():
        name = cmds.menuItem(item.keys(), q=True, label=True)
        command = cmds.menuItem(item.keys(), q=True, command=True)
        sourceType = cmds.menuItem(item.keys(), q=True, sourceType=True)
        textScroll = cmds.textScrollList('item_list', e=True, append=name+' - '+command+' - '+sourceType, doubleClickCommand=editItemUI)
        pop = cmds.popupMenu(p=textScroll, b=3)
        cmds.menuItem(p=pop, l='edit selected item', c=editItemUI)
        cmds.menuItem(p=pop, l='remove selected items', c=removeItems)
    cmds.formLayout(form, e=True, attachForm = [(txt, 'top', 5),(txt, 'bottom', 5), (txt, 'left', 5), (txt, 'right', 5)])
    # displays the window    
    cmds.showWindow('editRemoveItems')

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
            # add menu item
            menuItem = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand, sourceType=sourceType)
            # remove old otem
            SETTINGS.remove(item.keys()[0])
            # add fresh one
            SETTINGS.add(menuItem, [itemName, itemCommand, sourceType])

def createItem(none=None):
    """ create/add the custom item to the shelf and save the item to the settings file """
    itemName = cmds.textFieldGrp('create_customname', q=True, text=True)
    itemCommand = cmds.textFieldGrp('create_customCommand', q=True, text=True)
    value = cmds.radioButtonGrp('create_customSourceRadioButton', q=True, select=True)
    if not itemName or not itemCommand or not value:
        raise UserWarning('You need to fill all the fields!')
    if value == 1:
        sourceType = 'python'
    else:
        sourceType = 'mel'
    cmds.deleteUI(WINDOWNAME, window=True)
    # create the custom item
    item = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand, sourceType=sourceType)
    SETTINGS.add(item, [itemName, itemCommand, sourceType])

def addItemUI():
    """ create the ui that asks for the name, command and source type of the custom item """
    deleteWindow(WINDOWNAME)
    cmds.window(WINDOWNAME, t='add custom item', s=False)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('create_customname', label='name', text='')
    cmds.textFieldGrp('create_customCommand', label='command', text='')
    cmds.radioButtonGrp('create_customSourceRadioButton',label='source:', nrb=2, l1='python', l2='mel', select=1)
    cmds.separator('create_customSeparator', style='in')
    cmds.button(l='add', command=createItem)
    # displays the window
    cmds.showWindow(WINDOWNAME)

def addItem():
    """
     main function that displays the ui asking for the
     name, command and source type of the new custom item.
    """
    addItemUI()

