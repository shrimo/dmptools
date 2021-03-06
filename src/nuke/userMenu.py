"""
    user dmptools menu

"""

import nuke
import os
import random

import dmptools.tf2classes as tf2
import dmptools_misc.framestore.nuke as framestoreNuke

FRAMESTORE_NUKE_PATH = framestoreNuke.__path__[0]

# globals
NUKE_SHARE = '!NUKE_SHARE!'
TF2CLASSES = tf2.CLASSES

def buildMenu():

    # randomly get toolbar icon
    iconPrefix = TF2CLASSES.keys()[random.randint(0,len(TF2CLASSES)-1)]
    iconTooltip = TF2CLASSES[iconPrefix][random.randint(0,len(TF2CLASSES[iconPrefix])-1)]
    iconPath = NUKE_SHARE+'/tf2avatars/'+iconPrefix+'.jpg'
    # iconPath = NUKE_SHARE+'userIcon.png'

    print iconTooltip

    m = nuke.toolbar("Nodes").addMenu('dmptools/Misc', tooltip=iconTooltip, icon=iconPath)

    # 2D
    m.addCommand('2d/Nuke Image Converter...', 'import dmptools.tools.imageConverter as imageConverter");imageConverter.makeProxyUI()')
    m.addCommand('2d/Buf Clone', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.bclone()')
    m.addCommand('2d/Connect Selection ', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.connectSel()', "CTRL+Shift+Y")
    m.addCommand('2d/Clear Animation', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.clearAnim()')
    m.addCommand('2d/Show-Hide inputs', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.hideInputs()',"Alt+T")
    m.addCommand('2d/Set Selected or All Read Frame Range...', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setReadFrameRange()')
    m.addCommand('2d/Set frame range from selection', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setFrameRangeFromSel()', "Ctrl+Shift+R")
    m.addCommand('2d/Rename label according the dependance node', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.renameLabel()', "Ctrl+Alt+Shift+R")
    m.addCommand('2d/Switch crop format', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.switchCrop()', "Ctrl+Alt+Shift+O")
    m.addCommand('2d/Switch 0 - 1', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.switchUV_PROJ()', "Ctrl+Alt+Shift+S")
    m.addCommand('2d/Create read from write', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.createReadFromWrite()', "Ctrl+Alt+Shift+R")
    m.addCommand('2d/Toggle postage stamp on read nodes', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.togglePostageStamps()', "Ctrl+Alt+P")
    m.addCommand('2d/Bezier', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.switchNode()', "Ctrl+Alt+Shift+S")
    m.addCommand('2d/Write default', 'import nuke;nuke.createNode("Write")', "Shift+W")
    m.addCommand('2d/Switch node', 'nuke.tcl("Bezier")', "Shift+B")

    # 3D
    m.addCommand('3d/Shadow Generator', 'nuke.createNode("shadow_generator")')
    m.addCommand('3d/Connect Master Scene', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.connectMasterScene()', 'Ctrl+1')

    # other
    m.addCommand('Other/Centralize script...', 'execfile("/usr/people/michael-ha/python/centralizeNukeScript.py");makeLocalUI()')
    m.addCommand('Other/Archive script...', 'execfile("/usr/people/michael-ha/python/archive_v1.0.py");ai.interface()')
    m.addCommand('Other/Copy special', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.copySpecial()', "CTRL+SHIFT+C")
    m.addCommand('Other/list knobs', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.listKnobs()',"Ctrl+Alt+Shift+I")
    m.addCommand('Other/Play', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.nukePlay()', "Alt+V")
    m.addCommand('Other/Goto first frame', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.goToFirstFrame()', "Alt+Shift+V")
    m.addCommand('Other/Replace string in file knob...', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.replaceStringInFile()')
    m.addCommand('Other/Set selected Write the only active write', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setSelWriteActive()')
    m.addCommand('Other/How many nodes', 'nuke.message(str(len(nuke.allNodes()))+" nodes in comp.")', "Ctrl+Shift+Alt+A")
    m.addCommand('Other/Expression arrows', '_internal_expression_arrow_cmd()', "Alt+Shift+E")
    m.addCommand('Other/Unselect All', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.deselectAll();nukeCommands.closeAllControlPanel()', "Ctrl+Space")
    m.addCommand('Other/fNextRender', 'import dmptools.utils.nukeCommands as nukeCommands;reload(nukeCommands);nukeCommands.getNextRender();', "Alt+]")
    m.addCommand('Other/fPreviousRender', 'import dmptools.utils.nukeCommands as nukeCommands;reload(nukeCommands);nukeCommands.getPreviousRender();', "Alt+[")

    # misc
    m.addCommand('Execute', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.executeSelection()', "Alt+E")
    m.addCommand('Import exported file', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.importScript()', "Ctrl+Shift+I")
    m.addCommand('Open terminal from selection', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.openTerminal()', "Ctrl+Alt+X")
    m.addCommand('Start server', 'execfile("/usr/people/michael-ha/python/nukeserver.py");threaded_server()')
    m.addCommand('Set Shot FrameRange', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setShotFrameRange()')
    m.addCommand('Show modules...', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.showModules()')
    m.addCommand('Merge...', 'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.merge()', 'M')

    # framestore
    m.addCommand('Framestore/Refresh OCIO nodes...', 'import dmptools_misc.framestore.refreshOCIONodes as refreshOCIONodes;refreshOCIONodes.refreshOCIONodes()')
    m.addCommand('Framestore/Formater', 'nuke.nuke.nodePaste("'+FRAMESTORE_NUKE_PATH+'/formater.nk")')
    # aynik
    m.addCommand('Framestore/aynik/crop compensator', 'nuke.nuke.nodePaste("'+FRAMESTORE_NUKE_PATH+'/crop_compensator.nk")')
    m.addCommand('Framestore/aynik/srgb to linear', 'nuke.nuke.nodePaste("'+FRAMESTORE_NUKE_PATH+'/sRGB_to_Linear.nk")')

def main():
    """
        initiate nuke user menu
    """
    # main menu
    buildMenu()
    
if __name__ == '__main__':
    main()
