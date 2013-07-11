"""
    main dmptools menu

"""

# system modules
import os
import sys

# nuke modules
import nuke
import nukescripts

# dmptools nuke commands modules
import dmptools.utils.nukeCommands as nukeCommands
from dmptools.tools.scanlineRenderManager import ScanlineRenderManager
from dmptools.tools.runCommand import RunCommand
from dmptools.tools.webBrowser import WebBrowser
import dmptools.scripts as dmptoolsScripts

from dmptools.output import defaultPrint, successPrint, errorPrint

VERSION = '!VERSION!'
NUKE_SHARE = '!NUKE_SHARE!'
GIZMO_PATH = dmptoolsScripts.__path__[0]

def buildMenu():
    """
        build dmptools menu
    """

    #============================
    #   DEFAULT STARTUP TOOLS 
    #============================
    
    # default Nuke settings
    nukeCommands.defaultSettings()

    # create default favorite dirs
    nukeCommands.createFavoriteDirs()

    # add a frame range override on write node creation for the alfredRender tool
    # nukeCommands.addFrameRangeOverride()

    # auto check alpha on write node creation 
    nukeCommands.autoCheckAlpha()
    
    # create a tex converter on write nodes
    nukeCommands.addTexConverter()

    # auto check gl_light on viewers 
    nukeCommands.viewerSettings()

    # adds a backup button for fRenderTarget nodes
    nukeCommands.addfRenderTargetBackup()

    # add a latestAutosave menu item 
    nuke.menu("Nuke").addCommand('File/Recent Files/Latest autosave',
        'import dmptools.utils.nukeCommands as nukeCommands;nuke.scriptOpen(nukeCommands.getLatestAutosave())')

    #========================
    #   BUILD THE TOOLBAR 
    #========================

    # create 3ddmp toolbar
    toolbar = nuke.toolbar("Nodes").addMenu('dmptools', icon=NUKE_SHARE+'/toolbar.png')

    # toolbar menus
    toolbar.addMenu('Tools', icon=NUKE_SHARE+'/tools.png')
    toolbar.addMenu('Nodes', icon=NUKE_SHARE+'/nodes.png')
    toolbar.addMenu('Nodes/2d')
    toolbar.addMenu('Nodes/3d')
    toolbar.addMenu('Macros', icon=NUKE_SHARE+'/macros.png')
    toolbar.addMenu('Macros/2d')
    toolbar.addMenu('Macros/3d')

    #===================
    #    TOOLS MENU
    #===================

    #export nuke to maya
    toolbar.addCommand('Tools/Nuke to Maya...',
        'import dmptools.tools.nukeToMaya as nukeToMaya;reload(nukeToMaya);nukeToMaya.main()',
        icon=NUKE_SHARE+'/nukeToMaya.png')

    # psd to nuke 
    toolbar.addCommand('Tools/Psd to Nuke...',
        'import dmptools.tools.psdToNuke as psdToNuke;reload(psdToNuke);psdToNuke.main()',
        icon=NUKE_SHARE+'/psdToNuke.png')

    # ratio calculator
    toolbar.addCommand('Tools/Ratio calculator...',
        'import dmptools.tools.ratioCalculator as ratioCalculator;reload(ratioCalculator);ratioCalculator.main()',
        icon=NUKE_SHARE+'/ratioCalculator.png')

    # bake camera projections into uv textures
    toolbar.addCommand('Tools/Bake projection to UV...',
        'import dmptools.tools.bakeProjToUV as bakeProjToUV;reload(bakeProjToUV);bakeProjToUV.main()',
        icon=NUKE_SHARE+'/bake.png')

    # scanline render manager
    sc = ScanlineRenderManager()
    pane = nuke.menu("Pane")
    pane.addCommand("ScanlineRender Manager", sc.addToPane)
    nukescripts.registerPanel('ScanlineRenderManager', sc.addToPane)
    toolbar.addCommand('Tools/ScanlineRender Manager', sc.show, icon=NUKE_SHARE+'/scanline.png')

    # converts the selected node(s) and create a new read
    toolbar.addCommand('Tools/Image Converter...',
        'import dmptools.tools.imageConverter as imageConverter;reload(imageConverter);imageConverter.main()')

    # imgage converter dev
    toolbar.addCommand('Tools/Image Converter dev...',
        'import dmptools.tools.imageConverter_dev as imageConverter;reload(imageConverter);i = imageConverter.ImageConverter();i.show()')

    # mosaicer
    toolbar.addCommand('Tools/Mosaicer...',
        'import dmptools.tools.mosaicer as mosaicer;reload(mosaicer);mosaicer.main()')

    # demosaicer
    toolbar.addCommand('Tools/Demosaicer...',
        'import dmptools.tools.demosaicer as demosaicer;reload(demosaicer);demosaicer.main()')

    # run command
    run = RunCommand()
    pane = nuke.menu("Pane")
    pane.addCommand("Run Command", run.addToPane)
    nukescripts.registerPanel('RunCommand', run.addToPane)
    toolbar.addCommand('Tools/Run Command...', run.show)

    # web browser
    web = WebBrowser()
    nukescripts.panels.registerWidgetAsPanel(WebBrowser, 'Web Browser','Web Browser')
    toolbar.addCommand('Tools/Web Browser...', web.show)

    #===================
    #    NODES MENU
    #===================

    #2D
    # coverage map
    toolbar.addCommand('Nodes/2d/Coverage Map', 'nuke.createNode("coverageMap")')
    # apply lut
    toolbar.addCommand('Nodes/2d/Apply Lut', 'nuke.createNode("ApplyLUT")')

    # 3D
    # create projection camera from render camera
    toolbar.addCommand('Nodes/3d/Bake-Create Camera',
        'import dmptools.nodes.bakeCamera as bakeCamera;bakeCamera.BakeCamera()')
    # 3d image plane
    toolbar.addCommand('Nodes/3d/Image plane',
        'nuke.createNode("imagePlane")')
    # populate geo on 3d selection
    toolbar.addCommand('Nodes/3d/Populate 3d Geo ...',
        'import dmptools.tools.populate as populate;populate.main()')
    # sequence manager (dev)
    toolbar.addCommand('Nodes/3d/Sequence Manager',
        'nuke.nodePaste("'+GIZMO_PATH+'/sequenceManager.nk")')

    #===================
    #   MACROS MENU
    #===================

    # 2D
    # set the colorspace of the selected read nodes
    toolbar.addCommand('Macros/2d/Set colorspace...',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setColorspace()')
    # try to reload the selected nodes
    toolbar.addCommand('Macros/2d/Reload selected nodes',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.reloadReadNodes()', "Shift+Alt+R")
    # flip the viewer
    toolbar.addCommand('Macros/2d/Flip',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.flipViewer()', "`")
    # flop the viewer
    toolbar.addCommand('Macros/2d/Flop',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.flopViewer()', "Alt+`")
    # align nodes in the nodegraph
    toolbar.addCommand('Macros/2d/Align Up',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.upAlignSelectedNodes()')
    toolbar.addCommand('Macros/2d/Align Center',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.centerAlignSelectedNodes()')
    toolbar.addCommand('Macros/2d/Align Down',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.downAlignSelectedNodes()')
    # search and replace string in file knob
    toolbar.addCommand('Macros/2d/Search and replace string in file knob...',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.replaceStringInFile()')
    # show the path of all or selected read nodes
    toolbar.addCommand('Macros/2d/Show paths of all or selected Read nodes...',
        'import dmptools.tools.getFilePath as getFilePath;getFilePath.printPath()')
    # deselect and close all nodes control panel
    toolbar.addCommand('Macros/2d/Close all the nodes control panel',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.closeAllControlPanel()')
    # create viewerinput node check
    toolbar.addCommand('Macros/2d/Viewerinput Check node',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.createViewerInput()', "CTRL+ALT+X")

    # 3D
    # toggle visibility of 3d nodes
    toolbar.addCommand('Macros/3d/toggle camera and geo display',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.toggleCamGeoDisplay()',"Ctrl+Alt+Shift+C")
    # go through wireframe, shaded, textured and textured+wireframe
    toolbar.addCommand('Macros/3d/Wireframe',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setDisplayWireframe()', "Ctrl+Alt+4")
    toolbar.addCommand('Macros/3d/Shaded',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setDisplayShaded()', "Ctrl+Alt+5")
    toolbar.addCommand('Macros/3d/Textured',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setDisplayTextured()', "Ctrl+Alt+6")
    toolbar.addCommand('Macros/3d/Textured+Lines',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.setDisplayTexturedLines()', "Ctrl+Alt+7")
    # toggle default lighting on/off
    toolbar.addCommand('Macros/3d/Enable-Disable gl lighting',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.gl_lighting()', "Ctrl+Alt+0")

    # intranet help
    toolbar.addCommand('Help !',
        'import dmptools.utils.nukeCommands as nukeCommands;nukeCommands.helpButton()',
        icon=NUKE_SHARE+'/help.png')

def main():
    """
        initiate nuke dmptools menu
    """
    try:
        defaultPrint('loading dmptools...')
        # main menu
        buildMenu()        
        print " > done."

    except:
        errorPrint('failed to load dmptools!')

if __name__ == '__main__':
    main()
