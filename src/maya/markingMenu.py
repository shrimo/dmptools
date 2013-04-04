"""
modeling memo for marking menu

    -preseve uvs
    -vertex color -> black
    -merge vertex
    -combine
    -sepeparate
    -symmetry
    -scale on axis
    -snap
    -select from camera
    -invert selection

"""
import maya.cmds as cmds
import maya.mel as mel
import os

import dmptools.items as items

MARKINGMENU_ITEMS = items.markingMenuItems
MARKINGMENU_FILE = cmds.internalVar(userMarkingMenuDir=True)+'menu_dmptools.mel'

def getParentPanel():
    """return the parent panel """
    upPanel = cmds.getPanel(up=True)
    if cmds.panel(upPanel, q=True, ex=True):
        upPanelLayout = cmds.layout(upPanel, q=True, p=True)
        while not cmds.paneLayout(upPanelLayout, q=True, ex=True):
            upPanelLayout = cmds.control(upPanelLayout, q=True, p=True)
        if cmds.paneLayout(upPanelLayout, q=True, ex=True):
            return upPanelLayout
    else:
        return "viewPanes"

def createMarkingMenu(item):
    # fill the marking menu items
    name = item['name']
    annotation = item['annotation']
    subMenu = item['subMenu']
    position = item['position']
    command = item['command']
    # create item
    if position:
        cmds.menuItem(
            label=name,
            subMenu=subMenu,
            command=command,
            altModifier=False,
            ctrlModifier=False,
            shiftModifier=False,
            optionBox=False,
            enable=True,
            data=0,
            radialPosition=position,
            enableCommandRepeat=True,
            image="commandButton.png",
            echoCommand=1, # 1=left click 2=middle click 3=rightclick
            annotation=annotation,
            italicized=False,
            boldFont=False,
            sourceType="python",
            )
    else:
        cmds.menuItem(
            label=name,
            subMenu=subMenu,
            command=command,
            altModifier=False,
            ctrlModifier=False,
            shiftModifier=False,
            optionBox=False,
            enable=True,
            data=0,
            enableCommandRepeat=True,
            image="commandButton.png",
            echoCommand=1, # 1=left click 2=middle click 3=rightclick
            annotation=annotation,
            italicized=False,
            boldFont=False,
            sourceType="python",
            )

def showMarkingMenu():
    if cmds.popupMenu('dmptoolsMarkingMenu', ex=True):
        cmds.deleteUI('dmptoolsMarkingMenu')
    # Create dmptools marking menu.
    dmptoolsMenu = cmds.popupMenu('dmptoolsMarkingMenu', b=1, mm=True, parent=getParentPanel())
    mel.eval('source \"'+MARKINGMENU_FILE+'"')

def deleteMarkingMenu():
    if cmds.popupMenu('dmptoolsMarkingMenu', ex=True):
        cmds.deleteUI('dmptoolsMarkingMenu')

def createMenu():
    print '- creating dmptools marking menu...'
    if os.path.exists(MARKINGMENU_FILE):
        os.remove(MARKINGMENU_FILE)
    dmptoolsMenu = cmds.popupMenu('dmptoolsMarkingMenu', b=1, mm=True, parent=getParentPanel())
    for item in MARKINGMENU_ITEMS:
        createMarkingMenu(item)
    # Save the menu to a file.
    cmds.saveMenu(dmptoolsMenu, 'menu_dmptools')
    print '> done.'
    #print ("The menu was saved in "+cmds.internalVar(userMarkingMenuDir=True)+dmptoolsMenuFile)
    showMarkingMenu()
