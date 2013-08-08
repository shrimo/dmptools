"""
    list of items  used in marking menu, hotkeys, and shelf
"""

ICONSPATH = '!MAYA_SHELF!'
HELP_PAGE = '!HELP_PAGE!'

# markingMenu items list
markingMenuItems = [
    {
        'name':'Combine',
        'subMenu':False,
        'position':'N',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.combine()',
    },
    {
        'name':'Separate',
        'subMenu':False,
        'position':'NE',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.faceSeparate()',
    },
    {
        'name':'Symmetry',
        'subMenu':False,
        'position':'NW',
        'command':'import dmptools.tools.symmetry as symmetry;\
            reload(symmetry);symmetry.main()',
    },
    {
        'name':'separator',
        'subMenu':None,
        'position':None,
        'command':None
    },
    {
        'name':'MayaToNuke',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.mayaToNuke.launcher as mtn;\
            mtn.main();import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Nuke',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchNuke();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Terminator',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'SublimeText',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchSublimeText();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'newScriptEditor',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.newScriptEditor();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'ratioCalculator',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.ratioCalculator as ratioCalculator;\
            ratioCalculator.main();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Camera Constraint',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.camConstraint as camC;\
            reload(camC);camC.main();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Run command',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.runCommand as runCommand;\
            reload(runCommand);runCommand.main(False);\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Arc System',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.arcSystem as arcSystem;\
            reload(arcSystem);arcSystem.main();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Batch Rename',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.batchRename as batchRename;\
            reload(batchRename);batchRename.main(False);\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Replace default persp',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.replaceDefaultPersp();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'HotkeysList',
        'subMenu':False,
        'position':False,
        'annotation':'Show the hotkeys list window',
        'command':'import dmptools.setup.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList();\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
]

# hotkeys list
hotkeysItems = [
    {
        'name':'dmptoolsMarkingMenu',
        'key':'n',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.setup.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.createMenu()");',
        'releaseCommand':'python("import dmptools.setup.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.deleteMarkingMenu()");',
    },
    {
        'name':'runCommand',
        'key':'e',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.tools.runCommand as runCommand;\
            reload(runCommand);runCommand.main(False)");',
    },
    {
        'name':'namespaceEditor',
        'key':'N',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openNamespaceEditor()");',
    },
    {
        'name':'openNodeEditor',
        'key':'3',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openNodeEditor()");',
    },
    {
        'name':'createCameraUVProj',
        'key':'P',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.createCameraUVProj()");',
    },
    {
        'name':'switchColors',
        'key':'c',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchColors()");',
    },
    {
        'name':'softEdgeSelection',
        'key':'N',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.softEdgeSelection()");',
    },
    {
        'name':'invertSelection',
        'key':'I',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.invertSelection()");',
    },
    {
        'name':'showHotkeysList',
        'key':'H',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.setup.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList()");',
    },
    {
        'name':'createHotkeys',
        'key':'H',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.setup.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.main()");',
    },
    {
        'name':'bufMove',
        'key':'a',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMove()");',
        'releaseCommand':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");',
    },
    {
        'name':'bufMoveMulti',
        'key':'q',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveMulti()");',
        'releaseCommand':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");',
    },
    {
        'name':'hideSelectionSwitch',
        'key':'h',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.hideSelSwitch()");',
    },
    {
        'name':'isolateSelection',
        'key':'h',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.isolateSelection()");',
    },
    {
        'name':'toggleNormals',
        'key':'n',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleNormals()");',
    },
    {
        'name':'setWireframe',
        'key':'w',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setWireframe()");',
    },
    {
        'name':'setBackfaceCulling',
        'key':'B',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setBackfaceCulling()");',
    },
    {
        'name':'setDefaultMaterial',
        'key':'d',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
    },
    {
        'name':'cameraPanTool',
        'key':'z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraPanTool()");',
    },
    {
        'name':'cameraZoomTool',
        'key':'Z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraZoomTool()");',
    },
    {
        'name':'resetPanZoom',
        'key':'Z',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.resetPanZoom()");',
    },
    {
        'name':'selectNgones',
        'key':'q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectNgones()");',
    },
    {
        'name':'selectTriangles',
        'key':'p',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
    },
    {
        'name':'switchLight',
        'key':'l',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchLight()");',
    },
    {
        'name':'switchHighlightedSelection',
        'key':'f',
        'alt':True,
        'ctrl':False,'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchHighlightedSelection()");',
    },
    {
        'name':'askFlushUndo',
        'key':'f',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.askFlushUndo()");',
    },
    {
        'name':'saveAs',
        'key':'S',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'SaveSceneAs;',
    },
    {
        'name':'freezeHistory',
        'key':'F',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeHistory()");',
    },
    {
        'name':'freezeHistoryCenterPivot',
        'key':'F',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeCenterPivot()");',
    },
    {
        'name':'centerPivot',
        'key':'F',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.centerPivot()");',
    },
    {
        'name':'setDefaultRenderer',
        'key':'1',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultRenderer()");',
    },
    {
        'name':'setHardwareRenderer',
        'key':'2',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setHardwareRenderer()");',
    },
    {
        'name':'setViewport2Renderer',
        'key':'3',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setViewport2Renderer()");',
    },
    {
        'name':'launchConsole',
        'key':'x',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()");',
    },
    {
        'name':'mergeVertex',
        'key':'m',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeVertex()");',
    },
    {
        'name':'openUvTextureEditor',
        'key':'2',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openUvTextureEditor()");',
    },
    {
        'name':'openHypershade',
        'key':'1',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openHypershade()");',
    },
    {
        'name':'proMode',
        'key':'F11',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.proMode()");',
    },
    {
        'name':'unselectAll',
        'key':'space',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.unselectAll()");',
    },
    {
        'name':'switchObjectTumble',
        'key':'Q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchObjectTumble()");',
    },
    {
        'name':'toggleVertexColorDisplay',
        'key':'C',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleVertexColorDisplay()");',
    },
    {
        'name':'shortestEdgePath',
        'key':'Q',
        'alt':True,
        'ctrl':True,
        'release':True,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePath()");',
        'releaseCommand':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePathRelease()");',
    },
    {
        'name':'mergeUVs',
        'key':'X',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeUVs()");',
    },
]

# shelf buttons list
shelfItems = [
    {
        'name':'dmptools shelf',
        'command':'import dmptools.setup.shelf as shelf;shelf.main()',
        'icon':ICONSPATH+'/refresh.png',
        'annotation':'Rebuild the dmptools shelf - right click for options.',
        'menu':True,
        'menuItems':[('initiate dmptools', 'import dmptools.setup.init'),
                     ('github page','import webbrowser;webbrowser.open("'+HELP_PAGE+'")')]
    },
    {
        'name':'separator1'
    },
    {
        'name':'HotkeysList',
        'command':'import dmptools.setup.hotkeys as hotkeys;reload(hotkeys);hotkeys.showHotkeysList(dockable=False)',
        'icon':ICONSPATH+'/hotkeys.png',
        'annotation':'Show the hotkeys list window',
        'menu':True,
        'menuItems':[('run dockable', 'import dmptools.setup.hotkeys as hotkeys;reload(hotkeys);hotkeys.showHotkeysList(dockable=True)'),
                     ('run undockable', 'import dmptools.setup.hotkeys as hotkeys;reload(hotkeys);hotkeys.showHotkeysList(dockable=False)')]
    },
    {
        'name':'separator2'
    },
    {
        'name':'Terminator',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchTerminal()',
        'icon':ICONSPATH+'/Console.xpm',
        'annotation':'Launch the Console2 terminal.',
        'menu':True,
        'menuItems':[('Terminal','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchTerminal()'),
                     ('Windows console','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchConsole()'),
                    ]
    },
    {
        'name':'SublimeText',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchSublimeText()',
        'icon':ICONSPATH+'/SublimeText.xpm',
        'annotation':'Launch the Sublime Text editor.',
        'menu':False,
    },
    {
        'name':'Nuke',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchNuke()',
        'icon':ICONSPATH+'/Nuke.xpm',
        'annotation':'Launch Nuke.',
        'menu':False,
    },
    {
        'name':'ScriptEditor',
        'command':'import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openScriptEditor()',
        'icon':'text.png',
        'annotation':'Script Editor.',
        'menu':True,
        'menuItems':[('script editor','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.openScriptEditor()'),
                     ('custom script editor','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.newScriptEditor()'),
                    ]
    },
    {
        'name':'mayaToNuke',
        'command':'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(False)',
        'icon':ICONSPATH+'/MayaToNuke.xpm',
        'annotation':'Maya to Nuke Exporter.',
        'menu':True,
        'menuItems':[('run dockable', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(dockable=True)'),
                     ('run undockable', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(dockable=False)')]
    },
    {
        'name':'ratioCalculator',
        'command':'import dmptools.tools.ratioCalculator as ratioCalculator;\
            ratioCalculator.main()',
        'icon':ICONSPATH+'/RatioCalculator.xpm',
        'annotation':'Camera-Image ratio calculator.',
        'menu':False,
    },
    {
        'name':'separator3'
    },
    {
        'name':'utils',
        'command':'print "utils - right click for full list"',
        'icon':ICONSPATH+'/utils.png',
        'annotation':'utils - right click for full list',
        'menu':True,
        'menuItems':[
            ('maya to nuke', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(False)'),
            ('batch rename', 'import dmptools.tools.batchRename as batchRename;batchRename.main(False)'),
            ('arc system', 'import dmptools.tools.arcSystem as arcSystem;arcSystem.main()'),
            ('create rooftops', 'import dmptools.tools.createRooftops as createRooftops;createRooftops.main()'),
            ('run command', 'import dmptools.tools.runCommand as runCommand;runCommand.main(False)'),
            ('ratio calculator', 'import dmptools.tools.ratioCalculator as ratioCalculator;ratioCalculator.main()'),
            ('symmetry tool', 'import dmptools.tools.symmetry as symmetry;symmetry.main()'),
            ('bake udim tiles', 'import dmptools.tools.bakeUdimTiles as bakeUdimTiles;bakeUdimTiles.main()'),
        ]
    },
    {
        'name':'separator4'
    },
    {
        'name':'custom',
        'command':'import dmptools.setup.customItems as customItems;reload(customItems);customItems.addItem()',
        'icon':ICONSPATH+'/create.png',
        'annotation':'create custom item with associated command - right click for full list',
        'menu':True,
        'menuItems':[
                ('add item', 'import dmptools.setup.customItems as customItems;reload(customItems);customItems.addItem()'),
                ('edit/remove item', 'import dmptools.setup.customItems as customItems;reload(customItems);customItems.editRemoveItemsUI()'),
                ('divider1', ''),
                ]
    },
    {
        'name':'separator5'
    }
  ]
