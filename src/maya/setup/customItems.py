import maya.cmds as cmds

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('dmptoolsShelf')
PARENT = 'popup_custom'
WINDOWNAME = 'createCustomItem'

def removeItemsUI():
    """ ui that popup when the user right click on 'remove item' from the custom shelf
        it shows a list of the custom items created and saved in the settings file.
    """
    win = cmds.window(title='remove custom items')
    form = cmds.formLayout()
    txt = cmds.textScrollList('item_list', allowMultiSelection=True, deleteKeyCommand=removeItems)
    for item in SETTINGS.getAll():
        name = cmds.menuItem(item.keys(), q=True, label=True)
        command = cmds.menuItem(item.keys(), q=True, command=True)
        textScroll = cmds.textScrollList('item_list', e=True, append=name+' - '+command)
        pop = cmds.popupMenu(p=textScroll, b=3)
        cmds.menuItem(p=pop, l='remove selected items', c=removeItems)
    # form setup
    cmds.formLayout(form, e=True, attachForm = [(txt, 'top', 5),(txt, 'bottom', 5), (txt, 'left', 5), (txt, 'right', 5)])
    
    cmds.showWindow(win)

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
    pass

def createItem(none=None):
    """ create/add the custom item to the shelf and save the item to the settings file """
    itemName = cmds.textFieldGrp('customname', q=True, text=True)
    itemCommand = cmds.textFieldGrp('customCommand', q=True, text=True)
    cmds.deleteUI(WINDOWNAME, window=True)
    item = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand)
    SETTINGS.add(item, [itemName, itemCommand])

def ui():
    """ create the ui that asks for the name and command of the custom item """
    cmds.window(WINDOWNAME)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('customname', label='name', text='')
    cmds.textFieldGrp('customCommand', label='command', text='')
    cmds.button(l='ok', command=createItem)
    cmds.showWindow(WINDOWNAME)

def addItem():
    ui()

