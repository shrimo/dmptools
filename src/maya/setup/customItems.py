import maya.cmds as cmds

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('dmptoolsShelf')
PARENT = 'popup_custom'
WINDOWNAME = 'createCustomItem'

def removeItemsUI():
    win = cmds.window(title='remove custom items')
    form = cmds.formLayout()
    txt = cmds.textScrollList('item_list', allowMultiSelection=True, deleteKeyCommand=removeItems)
    for item in SETTINGS.getAll():
        name = cmds.menuItem(item.keys(), q=True, label=True)
        command = cmds.menuItem(item.keys(), q=True, command=True)
        cmds.textScrollList('item_list', e=True, append=name+' - '+command)

    cmds.formLayout(form, e=True, attachForm = [(txt, 'top', 5),(txt, 'bottom', 5), (txt, 'left', 5), (txt, 'right', 5)])
    cmds.showWindow(win)

def removeItems(none=None):
    items = cmds.textScrollList('item_list', q=True, si=True)
    cmds.textScrollList('item_list', e=True, ri=items)
    for item in items:
        print 'removing', item
        cmds.deleteUI(item, mi=True)
        SETTINGS.remove(item)

def checkSavedItems():
    pass

def ui():
    cmds.window(WINDOWNAME)
    cmds.formLayout()
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('customname', label='name', text='')
    cmds.textFieldGrp('customCommand', label='command', text='')
    cmds.button(l='ok', command=createItem)
    cmds.showWindow(WINDOWNAME)

def createItem(none=None):
    itemName = cmds.textFieldGrp('customname', q=True, text=True)
    itemCommand = cmds.textFieldGrp('customCommand', q=True, text=True)
    cmds.deleteUI(WINDOWNAME, window=True)
    item = cmds.menuItem(parent=PARENT, label=itemName, command=itemCommand)
    SETTINGS.add(item, [itemName, itemCommand])

def addItem():
    ui()

