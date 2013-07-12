import maya.cmds as cmds
import maya.mel as mel
import os

from dmptools.output import defaultPrint, successPrint

import dmptools.setup.customItems as customItems
import dmptools.setup.items as items
reload(items)
from items import shelfItems as SHELF_ITEMS

# globals
ICONSPATH = '!MAYA_SHELF!'
SHELF_NAME = 'dmptools'
SHELF_FILE = cmds.internalVar(userShelfDir=True)+'shelf_dmptools'

def createShelf():
    """ create the dmptools shelf """
    # delete the shelf is already exists
    if cmds.shelfLayout(SHELF_NAME, ex=True):
        fullname = cmds.shelfLayout('dmptools', fpn=True, q=True)
        cmds.deleteUI(fullname)
    # create the shelf
    shelfParent = cmds.shelfTabLayout('ShelfLayout', fpn=True, q=True)
    shelf = cmds.shelfLayout(SHELF_NAME, p=shelfParent)
    # add shelf buttons
    for item in SHELF_ITEMS:
        if 'separator' in item['name']:
            # defaultPrint(__name__+' : creating button '+item['name']+'...')
            addSeparator(item, shelf)
        else:
            # defaultPrint(__name__+' : creating button '+item['name']+'...')
            addButton(item, shelf)
    # select the last created shelf
    i = cmds.shelfTabLayout(shelfParent, numberOfChildren=True, q=True)
    cmds.shelfTabLayout(shelfParent, selectTabIndex=i, e=True)
    # save the shelf
    cmds.saveShelf(SHELF_NAME, SHELF_FILE)

def addSeparator(item, parent):
    """ add a vertical separator to the shelf """
    cmds.separator('dmptools_shelf_separator_'+item['name'], horizontal=False, style="out", parent=parent)

def addButton(item, parent):
    """ add button to the shelf """
    # create the button itself
    button = cmds.iconTextButton('dmptools_shelf_button_'+item['name'], parent=parent, enable=True, w=35, h=35,
                annotation=item['annotation'],
                image1=item['icon'],
                command=item['command'])
    # add right click popup items if exists
    if item['menu']:
        # create the popup menu with the name "popup_<name>"
        popMenu = cmds.popupMenu('dmptools_popup_'+item['name'], parent=button, b=3)
        for menuI in item['menuItems']:
            # add popup menu items
            if 'divider' in menuI[0]:
                cmds.menuItem('dmptools_popup_item_'+menuI[0], parent=popMenu, divider=True)
            else:
                cmds.menuItem(parent=popMenu, label=menuI[0], command=menuI[1])

def main():
    defaultPrint('creating dmptools shelf...')
    if os.path.exists(SHELF_FILE+'.mel'):
        os.remove(SHELF_FILE+'.mel')
    createShelf()
    # adds custom items if exists
    customItems.checkSavedItems()

if __name__ == '__main__':
    main()