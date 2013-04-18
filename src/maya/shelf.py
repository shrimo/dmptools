import maya.cmds as cmds
import maya.mel as mel
import os

import dmptools.items as items

# globals
CONFIGPATH = '!MAYA_SHELF!'
VERSION = '!VERSION!'
ICONSPATH = '!MAYA_SHELF!'
SHELF_ITEMS = items.shelfItems
SHELF_FILE = cmds.internalVar(userShelfDir=True)+'shelf_dmptools'

def createShelf():
    # delete the shelf is already exists
    if cmds.shelfLayout('dmptools', ex=True):
        fullname = cmds.shelfLayout('dmptools', fpn=True, q=True)
        cmds.deleteUI(fullname)
    # create the shelf
    shelfParent = cmds.shelfTabLayout('ShelfLayout', fpn=True, q=True)
    cmds.shelfLayout('dmptools', p=shelfParent)
    # create shelf buttons
    for item in SHELF_ITEMS:
        b = addButton(item)
    # select the last created shelf 
    i = cmds.shelfTabLayout(shelfParent, numberOfChildren=True, q=True)
    cmds.shelfTabLayout(shelfParent, selectTabIndex=i, e=True)
    # save the shelf
    cmds.saveShelf('dmptools', SHELF_FILE)

def addButton(item):
    # create dmptools shelf item
    b = cmds.shelfButton(item['name'],
                    enableCommandRepeat=True,
                    enable=True,
                    width=34,
                    height=34,
                    manage=True,
                    visible=True,
                    image1=ICONSPATH+'/'+item['icon'],
                    label=item['name'],
                    iol=item['iconLabel'],
                    style='iconOnly',
                    annotation=item['annotation'],
                    command=item['command'],
                    sourceType='python',
                    )
    return cmds.shelfButton(b, fpn=True, q=True)

def main():
    print '- creating dmptools shelf...'
    if os.path.exists(SHELF_FILE+'.mel'):
        print ' -removing old shelf...', SHELF_FILE+'.mel'
        os.remove(SHELF_FILE+'.mel')
    createShelf()
    print '> done.'

if __name__ == '__main__':
    main()