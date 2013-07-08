import maya.cmds as cmds
import maya.mel as mel
import os

from dmptools.setup.items import shelfItems as SHELF_ITEMS

# globals
ICONSPATH = '!MAYA_SHELF!'
SHELF_NAME = 'dmptools'
SHELF_FILE = cmds.internalVar(userShelfDir=True)+'shelf_dmptools'

def createShelf():
    # delete the shelf is already exists
    if cmds.shelfLayout(SHELF_NAME, ex=True):
        fullname = cmds.shelfLayout('dmptools', fpn=True, q=True)
        cmds.deleteUI(fullname)
    # create the shelf
    shelfParent = cmds.shelfTabLayout('ShelfLayout', fpn=True, q=True)
    shelf = cmds.shelfLayout(SHELF_NAME, p=shelfParent)
    # add shelf buttons
    for item in SHELF_ITEMS:
        if item['name'] == 'separator':
            addSeparator(shelf)
        else:
            addButton(item, shelf)
    # select the last created shelf
    i = cmds.shelfTabLayout(shelfParent, numberOfChildren=True, q=True)
    cmds.shelfTabLayout(shelfParent, selectTabIndex=i, e=True)
    # save the shelf
    cmds.saveShelf(SHELF_NAME, SHELF_FILE)

def addSeparator(shelf):
    """ add a vertical separator to the shelf """
    cmds.separator(horizontal=False, style="out", parent=shelf)

def addButton(item, parent):
    """ add button to the shelf """
    # create the button itself
    button = cmds.iconTextButton(parent=parent, enable=True, w=35, h=35,
                annotation=item['annotation'],
                image1=item['icon'],
                command=item['command'])
    # add right click popup items if exists
    if item['menu']:
        popMenu = cmds.popupMenu(parent=button, b=3)
        for menuI in item['menuItems']:
            cmds.menuItem(p=popMenu, l=menuI[0], command=menuI[1])

def main():
    print '- creating dmptools shelf...'
    if os.path.exists(SHELF_FILE+'.mel'):
        print ' -removing old shelf...', SHELF_FILE+'.mel'
        os.remove(SHELF_FILE+'.mel')
    createShelf()
    print '> done.'

if __name__ == '__main__':
    main()