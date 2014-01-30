"""
    list of items  used in marking menu, hotkeys, and shelf
"""

from dmptools.settings import SettingsManager

# strings to be generated by the install
ICONSPATH = '!MAYA_SHELF!'
HELP_PAGE = '!HELP_PAGE!'

def appendSettingsItems(SHELF_ITEMS):
    """
    returns a list of setting items if they exists 
    """
    itemsToCrop = SHELF_ITEMS[0:3]
    croppedList = SHELF_ITEMS[4:]

    menuList = []
    for setting in SettingsManager('maya_main').getAllSettingsFiles():
        if setting:
            if not '~' in setting:
                menuList.append((setting.replace('_', ' '), 'import dmptools.setup.settingsWindow as settingsWindow;\
                            reload(settingsWindow);\
                            settingsWindow.main("'+setting+'")'))

    if menuList:
        item = {
                'name':'Settings',
                'command':'print "settings - right click for full list", ',
                'icon':ICONSPATH+'/options.png',
                'annotation':'Settings for various dmptools modules',
                'menu':True,
                'menuItems':menuList
            }
        itemSeparator = {
            'name':'separator_options'
            }
        itemsToCrop.append(item)
        itemsToCrop.append(itemSeparator)

    itemsToCrop.extend(croppedList)

    return itemsToCrop

# markingMenu items list
markingMenuItems = [
    #==========================#
    #       COMPASS MENU       #
    #==========================#
    {
        'name':'Combine',
        'subMenu':False,
        'position':'N',
        'command':'import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.combine()',
    },
    {
        'name':'Separate',
        'subMenu':False,
        'position':'NE',
        'command':'import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.faceSeparate()',
    },
    {
        'name':'Symmetry',
        'subMenu':False,
        'position':'NW',
        'command':'import dmptools.tools.symmetry as symmetry;\
            reload(symmetry);symmetry.main()',
    },
    {
        'name':'Split edge',
        'subMenu':False,
        'position':'W',
        'command':'import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.oldSplitEdge()',
    },

    #============================#
    #         MAIN MENU          #
    #============================#
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
        'name':'separator',
        'subMenu':None,
        'position':None,
        'command':None
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
        'name':'UV tile Manager',
        'subMenu':False,
        'position':False,
        'command':'import dmptools.tools.uvManager as uvManager;reload(uvManager);uvManager.main();\
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
            reload(hotkeys);hotkeys.showHotkeysList(dockable=False);\
            import dmptools.setup.markingMenu as mm;mm.deleteMarkingMenu()',
    },
]

# hotkeys list

hotkeysItems = [
    {
        'name':'_____________________________MAIN______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'dmptools_marking_menu',
        'help':'Shows the dmptools marking menu.', 
        'key':'j',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.setup.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.createMenu()");',
        'releaseCommand':'python("import dmptools.setup.markingMenu as markingMenu;\
            reload(markingMenu);markingMenu.deleteMarkingMenu()");',
    },
    {
        'name':'reassign_dmptools_hotkeys',
        'help':'Reassign the dmptools hotkeys.', 
        'key':'H',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.setup.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.main()");',
    },
    {
        'name':'show_hotkeys_ist',
        'help':'Opens the dmptools hotkeys summary window',
        'key':'H',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.setup.hotkeys as hotkeys;\
            reload(hotkeys);hotkeys.showHotkeysList()");',
    },
    #=====================================================================#
    #                      MODELING SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________MODELING______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'align_selected_vertices_minX',
        'help':'Align selected component vertices to the minimal X axis value.', 
        'key':'4',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(True, False, False, False, False, False)");',
    },
    {
        'name':'align_selected_vertices_maxX',
        'help':'Align selected component vertices to the maximal X axis value.', 
        'key':'6',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(False, True, False, False, False, False)");',
    },
    {
        'name':'align_selected_vertices_minY',
        'help':'Align selected component vertices to the minimal Y axis value.', 
        'key':'2',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(False, False, True, False, False, False)");',
    },
    {
        'name':'align_selected_vertices_maxY',
        'help':'Align selected component vertices to the maximal Y axis value.', 
        'key':'8',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(False, False, False, True, False, False)");',
    },
    {
        'name':'align_selected_vertices_minZ',
        'help':'Align selected component vertices to the minimal Z axis value.', 
        'key':'7',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(False, False, False, False, True, False)");',
    },
    {
        'name':'align_selected_vertices_maxZ',
        'help':'Align selected component vertices to the maximal Z axis value.', 
        'key':'9',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignVertices(False, False, False, False, False, True)");',
    },
    {
        'name':'align_selected_UVs_up',
        'help':'Align selected UVs to the maximal V axis value.', 
        'key':'up',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignUVs(False, False, True, False)");',
    },
    {
        'name':'align_selected_UVs_down',
        'help':'Align selected UVs to the minimal V axis value.', 
        'key':'down',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignUVs(False, False, True, True)");',
    },
    {
        'name':'align_selected_UVs_left',
        'help':'Align selected UVs to the minimal U axis value.', 
        'key':'left',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignUVs(True, True, False, False)");',
    },
    {
        'name':'align_selected_UVs_right',
        'help':'Align selected UVs to the maximal U axis value.', 
        'key':'right',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.alignUVs(True, False, False, False)");',
    },
    {
        'name':'symmetry_tool',
        'help':'Opens the dmptools symmetry tool.',
        'key':'s',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.tools.symmetry as symmetry;\
            reload(symmetry);symmetry.main()");',
    },
    {
        'name':'create_uv_proj_from_camera',
        'help':'Creates a uv proj on selected mesh from the current camera.',
        'key':'P',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.createCameraUVProj()");',
    },
    {
        'name':'soften_harden_edge',
        'help':'Smooth selected edges with default value (180) or the one stored in dmptools settings.',
        'key':'n',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.softEdgeSelection()");',
    },
    {
        'name':'unlock_harden_edge',
        'help':'Unlock and harden selected edges.',
        'key':'N',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.unlockAndHarden()");',
    },
    {
        'name':'advance_move',
        'help':'Enters the advance move selection mode.',
        'key':'A',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMove()");',
        'releaseCommand':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveRelease()");',
    },
    {
        'name':'advance_move_multi',
        'help':'Enters the advance move multi component selection mode.',
        'key':'a',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveMulti()");',
        'releaseCommand':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveRelease()");',
    },
    {
        'name':'advance_extrude_multi',
        'help':'Enters the extrude multi component mode. *need to update with multiple selection*',
        'key':'q',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveMultiExtrude()");',
        'releaseCommand':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveRelease()");',
    },
    {
        'name':'split_edge_tool',
        'help':'Split edge tool.',
        'key':'Q',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.oldSplitEdge()");',
        'releaseCommand':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.advanceMoveRelease()");',
    },
    {
        'name':'split_edge_ring_tool',
        'help':'Split edge ring tool.',
        'key':'Q',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.splitEdgeRing()");',
    },
    {
        'name':'merge_vertices',
        'help':'Merge selected vertices with default value (0.1) or the one stored in dmptools settings.',
        'key':'m',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.mergeVertex()");',
    },
    {
        'name':'merge_uvs',
        'help':'Merge selected UVs with default value (0.1) or the one stored in dmptools settings.',
        'key':'X',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.modeling as modeling;\
            reload(modeling);modeling.mergeUVs()");',
    },
    #=====================================================================#
    #                      DISPLAY SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________DISPLAY______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'set_default_renderer',
        'help':'Set the viewport display to the default renderer.',
        'key':'1',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultRenderer()");',
    },
    {
        'name':'set_hardware_renderer',
        'help':'Set the viewport display to the hardware renderer.',
        'key':'2',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setHardwareRenderer()");',
    },
    {
        'name':'set_viewport2.0_renderer',
        'help':'Set the viewport display to the viewport2.0 renderer.',
        'key':'3',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setViewport2Renderer()");',
    },
    {
        'name':'toggle_vertex_color_display',
        'help':'Toggle vertex color display on selected obejcts.',
        'key':'C',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleVertexColorDisplay()");',
    },
    {
        'name':'toggle_normals',
        'help':'Toggle normal display on selected object.',
        'key':'n',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleNormals()");',
    },
    {
        'name':'toggle_wireframe',
        'help':'Toggle wireframe on shaded.',
        'key':'w',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setWireframe()");',
    },
    {
        'name':'toggle_backface_culling',
        'help':'Toggle backface culling.',
        'key':'B',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setBackfaceCulling()");',
    },
    {
        'name':'toggle_default_material',
        'help':'Toggle default material.',
        'key':'d',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
    },
    {
        'name':'toggle_all_lights',
        'help':'Toggle between default lights and all lights.',
        'key':'l',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchLight()");',
    },
    {
        'name':'toggle_highlighted_selection',
        'help':'Toggle highlighted selection.',
        'key':'f',
        'alt':True,
        'ctrl':False,'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchHighlightedSelection()");',
    },
    {
        'name':'camera_pan_tool',
        'help':'Enters the camera pan tool.',
        'key':'z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraPanTool()");',
    },
    {
        'name':'camera_zoom_tool',
        'help':'Enters the camera zoom tool.',
        'key':'Z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraZoomTool()");',
    },
    {
        'name':'reset_pan_zoom',
        'help':'Reset camera pan zoom tool.',
        'key':'Z',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.resetPanZoom()");',
    },
    {
        'name':'isolate_selection',
        'help':'Toggle isolate selection.',
        'key':'h',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.isolateSelection()");',
    },
    #=====================================================================#
    #                      WINDOWS SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________WINDOWS______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'namespace_editor',
        'help':'Opens the namespace editor.',
        'key':'n',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openNamespaceEditor()");',
    },
    {
        'name':'hypershade',
        'help':'Opens the hypershade.',
        'key':'0',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openHypershade()");',
    },
    {
        'name':'uv_texture_editor',
        'help':'Opens the uv texture editor.',
        'key':'.',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openUvTextureEditor()");',
    },
    #=====================================================================#
    #                      SELECTION SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________SELECTION______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'freeze_delete_history',
        'help':'Freeze transforms and delete history.',
        'key':'F',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeHistory()");',
    },
    {
        'name':'freeze_delete_history_pivot',
        'help':'Freeze transforms, delete history and center pivot.',
        'key':'F',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeCenterPivot()");',
    },
    {
        'name':'center_pivot',
        'help':'Center pivot of selected objects.',
        'key':'F',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.centerPivot()");',
    },
    {
        'name':'toggle_visibility',
        'help':'Toggle visibility of selected objects.',
        'key':'h',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.hideSelSwitch()");',
    },
    {
        'name':'invert_selection',
        'help':'Invert selection.',
        'key':'I',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.invertSelection()");',
    },
    {
        'name':'select_ngones',
        'help':'Select polygon with more than 4 edges.',
        'key':'q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectNgones()");',
    },
    {
        'name':'selectTriangles',
        'help':'Select triangles.',
        'key':'p',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
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
    #=====================================================================#
    #                              MISC SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________MISC______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
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
        'name':'switchObjectTumble',
        'key':'Q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchObjectTumble()");',
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
        'name':'setNamespace',
        'key':'N',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.utils.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setNamespace()");',
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
    #=====================================================================#
    #                              FRAMESTORE SECTION    #
    #=====================================================================#
    {
        'name':'_____________________________FRAMESTORE______________________________________',
        'help':'',
        'key':'-',
        'alt':'',
        'ctrl':'',
        'release':False,
        'command':'print "separator"',
    },
    {
        'name':'setPreviousRenderVersion',
        'help':'setPreviousRenderVersion',
        'key':'[',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;reload(fbkUtils);fbkUtils.setPreviousVersion(\'render\', True, True)");',
    },
    {
        'name':'setNextRenderVersion',
        'help':'setNextRenderVersion',
        'key':']',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;reload(fbkUtils);fbkUtils.setNextVersion(\'render\', True, True)");',
    },
    {
        'name':'setPreviousRenderDisplayVersion',
        'help':'setPreviousRenderDisplayVersion',
        'key':'{',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;reload(fbkUtils);fbkUtils.setPreviousVersion(\'render\', False, True)");',
    },
    {
        'name':'setNextRenderDisplayVersion',
        'help':'setNextRenderDisplayVersion',
        'key':'}',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;reload(fbkUtils);fbkUtils.setNextVersion(\'render\', False, True)");',
    },
    {
        'name':'setLatestVersion',
        'help':'setLatestVersion',
        'key':']',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;reload(fbkUtils);fbkUtils.setLatestVersion(\'render\', False, False)");',
    },
    {
        'name':'switchFbkResolution',
        'help':'switchFbkResolution',
        'key':'G',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools_misc.framestore.maya.fbkUtils as fbkUtils;\
            reload(fbkUtils);fbkUtils.switchAnimRender()");',
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
        'menuItems':[
            ('Initialize dmptools', 'import dmptools.setup.init'),
            ('divider2', ''),
            ('Open maya command port', 'import dmptools.setup.mayaSettings as mayaSettings;mayaSettings.openCommandPort()'),
            ('Set Custom Settings', 'import dmptools.setup.mayaSettings as ms;ms.setCustomSettings()'),
            ('Set Default Settings', 'import dmptools.setup.mayaSettings as ms;ms.setDefaultSettings()'),
        ]
    },
    {
        'name':'separator_main'
    },
    {
        'name':'Help',
        'command':'print "right click for full list.", ',
        'icon':ICONSPATH+'/help.png',
        'annotation':'Help associated commands.',
        'menu':True,
        'menuItems':[
            ('Show dmptools shortcuts', 'import dmptools.setup.hotkeys as hotkeys;reload(hotkeys);hotkeys.showHotkeysList(dockable=False)'),
            ('divider2', ''),
            ('Open dmptools github page','import webbrowser;webbrowser.open("'+HELP_PAGE+'")'),
            ('Open Maya commands page','import webbrowser;webbrowser.open("http://download.autodesk.com/global/docs/maya2014/en_us/CommandsPython/index.html")'),
        ]
    },
    {
        'name':'separator_help'
    },
    {
        'name':'Terminator',
        'command':'print "right click for full list.", ',
        'icon':ICONSPATH+'/Console.xpm',
        'annotation':'Launch a Terminal.',
        'menu':True,
        'menuItems':[
            ('Terminal','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchTerminal()'),
            ('Windows console','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchConsole()'),
        ]
    },
    {
        'name':'Script/Code Editor',
        'command':'print "right click for full list.", ',
        'icon':'text.png',
        'annotation':'Script/Code Editor.',
        'menu':True,
        'menuItems':[
            ('script editor','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.openScriptEditor()'),
            ('charcoal editor','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.openCharcoalEditor()'),
            ('Sublime Text','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchSublimeText()'),
            ('custom script editor','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.newScriptEditor()'),
        ]
    },
    {
        'name':'Nuke',
        'command':'print "right click for full list.", ',
        'icon':ICONSPATH+'/Nuke.xpm',
        'annotation':'Launch Nuke.',
        'menu':True,
        'menuItems':[
            ('Launch Nuke','import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.launchNuke()'),
        ]
    },
# deprecated maya to nuke button. moved to the Utils menu item list
#    {
#        'name':'mayaToNuke',
#        'command':'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(False)',
#        'icon':ICONSPATH+'/MayaToNuke.xpm',
#        'annotation':'Maya to Nuke Exporter.',
#        'menu':True,
#        'menuItems':[
#            ('run dockable', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(dockable=True)'),
#            ('run undockable', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(dockable=False)')
#        ]
#    },
    {
        'name':'separator_utils'
    },
    {
        'name':'Utils',
        'command':'print "utils - right click for full list", ',
        'icon':ICONSPATH+'/utils.png',
        'annotation':'utils - right click for full list',
        'menu':True,
        'menuItems':[
            ('maya to nuke', 'import dmptools.tools.mayaToNuke.launcher as mayaToNukeLauncher;mayaToNukeLauncher.main(False)'),
            ('batch rename', 'import dmptools.tools.batchRename as batchRename;reload(batchRename);batchRename.main(False)'),
            ('display color', 'import dmptools.tools.displayColor as displayColor;reload(displayColor);displayColor.main()'),
            ('arc system', 'import dmptools.tools.arcSystem as arcSystem;reload(arcSystem);arcSystem.main()'),
            ('create rooftops', 'import dmptools.tools.createRooftops as createRooftops;reload(createRooftops);createRooftops.main()'),
            ('ratio calculator', 'import dmptools.tools.ratioCalculator as ratioCalculator;reload(ratioCalculator);ratioCalculator.main()'),
            ('run command', 'import dmptools.tools.runCommand as runCommand;reload(runCommand);runCommand.main(False)'),
            ('symmetry tool', 'import dmptools.tools.symmetry as symmetry;reload(symmetry);symmetry.main()'),
            ('uv tiles manager', 'import dmptools.tools.uvManager as uvManager;reload(uvManager);uvManager.main()'),
            ('floating output', 'import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.floatingOutputReporter()'),
            ('divider1', ''),
            ('bake udim tiles', 'import dmptools.tools.bakeUdimTiles as bakeUdimTiles;reload(bakeUdimTiles);bakeUdimTiles.main()'),
            ('fix clip planes', 'import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.fixClipPlanes()'),
            ('bake camera', 'import dmptools.tools.bakeCamera as bakeCamera;reload(bakeCamera);bakeCamera.main()'),
        ]
    },
    {
        'name':'Framestore utils',
        'command':'print "utils - right click for full list", ',
        'icon':ICONSPATH+'/framestore_logo.jpg',
        'annotation':'utils - right click for full list',
        'menu':True,
        'menuItems':[
            ('load fShambles...', 'import dmptools_misc.framestore.maya.jsonWrite as jsonWrite;jsonWrite.loadShambles()'),
            ('write fShambles...', 'import dmptools_misc.framestore.maya.jsonWrite as jsonWrite;jsonWrite.main()'),
            ('divider3', ''),
            ('get fd state', 'import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.getFdState()'),
            ('get fd list', 'import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.getLenFd(True)'),
            ('flush fd', 'import dmptools.utils.mayaCommands as mayaCommands;reload(mayaCommands);mayaCommands.flushFd()'),
        ]
    },
    {
        'name':'separator_customItems'
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
            # that's where the custom items created by the user are going to be placed.
        ]
    },
    {
        'name':'separator_end'
    }
  ]
