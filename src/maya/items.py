# markingMenu items list
markingMenuItems = [
    {
        'name':'separator',
        'annotation':None,
        'subMenu':None,
        'position':None,
        'command':None
    },
    {
        'name':'MayaToNuke',
        'annotation':'Launch Maya to Nuke bridge.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.mayaToNuke.launcher as mtn;\
            mtn.main();import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Nuke',
        'annotation':'Launch Nuke.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchNuke();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Terminator',
        'annotation':'Launch the Console2 terminal.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'SublimeText',
        'annotation':'Launch the Sublime Text editor.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchSublimeText();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'newScriptEditor',
        'annotation':'New Script Editor.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.newScriptEditor();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'ratioCalculator',
        'annotation':'Camera-Image ratio calculator.',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.ratioCalculator as ratioCalculator;\
            ratioCalculator.main();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'HotkeysList',
        'subMenu':False,
        'position':False,
        'annotation':'Show the hotkeys list window',
        'command':'import dmptools.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList();\
            import dmptools.markingMenu as mm;mm.deleteMarkingMenu()',
    },
    {
        'name':'Combine',
        'annotation':'Combine clean.',
        'subMenu':False,
        'position':'N',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.combine()',
    },
    {
        'name':'Separate',
        'annotation':'Separate clean.',
        'subMenu':False,
        'position':'NE',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.faceSeparate()',
    },
    {
        'name':'Symmetry',
        'annotation':'Symmetry.',
        'subMenu':False,
        'position':'NW',
        'command':'import dmptools.symmetry as symmetry;\
            reload(symmetry);symmetry.main()',
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
        'command':'python("import dmptools.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.createMenu()");',
        'releaseCommand':'python("import dmptools.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.deleteMarkingMenu()");',
    },
    {
        'name':'openNodeEditor',
        'key':'3',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openNodeEditor()");',
    },
    {
        'name':'createCameraUVProj',
        'key':'P',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.createCameraUVProj()");',
    },
    {
        'name':'switchColors',
        'key':'c',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchColors()");',
    },
    {
        'name':'softEdgeSelection',
        'key':'N',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.softEdgeSelection()");',
    },
    {
        'name':'invertSelection',
        'key':'I',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.invertSelection()");',
    },
    {
        'name':'showHotkeysList',
        'key':'H',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList()");',
    },
    {
        'name':'createHotkeys',
        'key':'H',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.main()");',
    },
    {
        'name':'bufMove',
        'key':'a',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMove()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");',
    },
    {
        'name':'bufMoveMulti',
        'key':'q',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveMulti()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");',
    },
    {
        'name':'hideSelectionSwitch',
        'key':'h',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.hideSelSwitch()");',
    },
    {
        'name':'isolateSelection',
        'key':'h',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.isolateSelection()");',
    },
    {
        'name':'toggleNormals',
        'key':'n',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleNormals()");',
    },
    {
        'name':'setWireframe',
        'key':'w',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setWireframe()");',
    },
    {
        'name':'setBackfaceCulling',
        'key':'B',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setBackfaceCulling()");',
    },
    {
        'name':'setDefaultMaterial',
        'key':'d',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
    },
    {
        'name':'cameraPanTool',
        'key':'z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraPanTool()");',
    },
    {
        'name':'cameraZoomTool',
        'key':'Z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraZoomTool()");',
    },
    {
        'name':'resetPanZoom',
        'key':'Z',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.resetPanZoom()");',
    },
    {
        'name':'selectNgones',
        'key':'q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectNgones()");',
    },
    {
        'name':'selectTriangles',
        'key':'p',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
    },
    {
        'name':'switchLight',
        'key':'l',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchLight()");',
    },
    {
        'name':'switchHighlightedSelection',
        'key':'f',
        'alt':True,
        'ctrl':False,'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchHighlightedSelection()");',
    },
    {
        'name':'askFlushUndo',
        'key':'f',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
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
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeHistory()");',
    },
    {
        'name':'freezeHistoryCenterPivot',
        'key':'F',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeCenterPivot()");',
    },
    {
        'name':'centerPivot',
        'key':'F',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.centerPivot()");',
    },
    {
        'name':'setDefaultRenderer',
        'key':'1',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultRenderer()");',
    },
    {
        'name':'setHardwareRenderer',
        'key':'2',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setHardwareRenderer()");',
    },
    {
        'name':'setViewport2Renderer',
        'key':'3',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setViewport2Renderer()");',
    },
    {
        'name':'launchConsole',
        'key':'x',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()");',
    },
    {
        'name':'mergeVertex',
        'key':'m',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeVertex()");',
    },
    {
        'name':'openUvTextureEditor',
        'key':'2',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openUvTextureEditor()");',
    },
    {
        'name':'openHypershade',
        'key':'1',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openHypershade()");',
    },
    {
        'name':'proMode',
        'key':'F11',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.proMode()");',
    },
    {
        'name':'unselectAll',
        'key':'space',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.unselectAll()");',
    },
    {
        'name':'switchObjectTumble',
        'key':'Q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchObjectTumble()");',
    },
    {
        'name':'toggleVertexColorDisplay',
        'key':'C',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleVertexColorDisplay()");',
    },
    {
        'name':'shortestEdgePath',
        'key':'Q',
        'alt':True,
        'ctrl':True,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePath()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePathRelease()");',
    },
    {
        'name':'mergeUVs',
        'key':'X',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeUVs()");',
    },
]

# shelf buttons list
shelfItems = [
    {
        'name':'HotkeysList',
        'iconLabel':'hotkey',
        'command':'import dmptools.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList()',
        'icon':'pythonFamily.png',
        'annotation':'Show the hotkeys list window'
    },
    {
        'name':'Terminator',
        'iconLabel':'',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()',
        'icon':'Console.xpm',
        'annotation':'Launch the Console2 terminal.'
    },
    {
        'name':'SublimeText',
        'iconLabel':'',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchSublimeText()',
        'icon':'SublimeText.xpm',
        'annotation':'Launch the Sublime Text editor.'
    },
    {
        'name':'Nuke',
        'iconLabel':'',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchNuke()',
        'icon':'Nuke.xpm',
        'annotation':'Launch Nuke.'
    },
    {
        'name':'newScriptEditor',
        'iconLabel':'',
        'command':'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.newScriptEditor()',
        'icon':'text.png',
        'annotation':'New Script Editor.'
    },
    {
        'name':'mayaToNuke',
        'iconLabel':'',
        'command':'import dmptools.mayaToNuke.launcher as mayaToNukeLauncher;\
            mayaToNukeLauncher.main()',
        'icon':'MayaToNuke.xpm',
        'annotation':'Maya to Nuke Exporter.'
    },
    {
        'name':'ratioCalculator',
        'iconLabel':'',
        'command':'import dmptools.ratioCalculator as ratioCalculator;\
            ratioCalculator.main()',
        'icon':'RatioCalculator.xpm',
        'annotation':'Camera-Image ratio calculator.'
    },
  ]
