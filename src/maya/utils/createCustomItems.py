import maya.cmds as cmds

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('dmptoolsShelf')
PARENT = 'popup_custom'
WINDOWNAME = 'createCustomItem'

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
    cmds.menuItem(p=PARENT, l=itemName, command=itemCommand)
    SETTINGS.add(itemName, itemCommand)

def main():
    ui()
