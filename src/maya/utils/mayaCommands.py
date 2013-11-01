import maya.cmds as cmds
import maya.mel as mel
import os
import time
import subprocess
import fnmatch
import math

from dmptools.settings import SettingsManager

# globals
SETTINGS = SettingsManager('maya')
normalAngle = 35
perspNear = 1
perspFar = 200000

PLATFORM = '!PLATFORM!'

SETTINGS.add('default_normalAngle', normalAngle)
SETTINGS.add('default_perspNear', perspNear)
SETTINGS.add('default_perspFar', perspFar)

def openCharcoalEditor():
    mel.eval('charcoalEditor;')

def openHypergraph():
    mel.eval('HypergraphDGWindow;')

def openOutliner():
    mel.eval('OutlinerWindow;')

def openNamespaceEditor():
    mel.eval('NamespaceEditor;')

def openScriptEditor():
    mel.eval("ScriptEditor;")

def openNodeEditor():
    mel.eval('NodeEditorWindow;')

def createNodeWindow():
    mel.eval('CreateNodeWindow;')

def openUvTextureEditor():
    mel.eval('TextureViewWindow;')

def openHypershade():
    mel.eval('HypershadeWindow;')

def alignUVsUP():
    # to top
    mel.eval("alignUV 0 0 1 0;")

def alignUVsDown():
    # to bottom
    mel.eval("alignUV 0 0 1 1;")

def alignUVsLeft():
    # to left
    mel.eval("alignUV 1 1 0 0;")

def alignUVsRight():
    # to right
    mel.eval("alignUV 1 0 0 0;")

def checkOverlappingObjects(selection):
    xforms = []
    wrongXforms = []
    for node in selection:
        nodeM = cmds.xform(node, ws=True, m=True, q=True)
        if nodeM in xforms:
            wrongXforms.append(node)
        else:
            xforms.append(nodeM)
    if wrongXforms:
        return wrongXforms
    else:
        return None

def getActiveCamera():
    pane = cmds.getPanel(wf=True)
    activeCamera = cmds.modelPanel(pane, camera=True, q=True)

    return activeCamera

def fixClipPlanes():
    activeCamera = getActiveCamera()
    activeCameraShape = cmds.listRelatives(activeCamera, shapes=True)[0]
    cmds.setAttr(activeCameraShape+'.nearClipPlane', 10)
    cmds.setAttr(activeCameraShape+'.farClipPlane', 1000000)

def getNamespace():
    selection = cmds.ls(sl=True)
    root = ':'
    if selection:
        node = selection[0]
        if '|' in node:
            node = node.split('|')[-1]
    
        nsSplit = node.split(':')[:-1]    
        ns = root+root.join(nsSplit)+root
        return ns
    else:
        return ':'

def udimFromNode(node):
    uPos, vPos = cmds.polyEditUV(node+'.map[1]', q=True)
    uTile = int(math.floor(uPos))
    vTile = int(math.floor(vPos))
    udim = 1000+(uTile+1)+(vTile*10)
    
    return udim, uTile, vTile

def uvFromUdim(udim):
    v = (udim-1000-1)/10
    u = (udim-1000-1-(v*10))
    
    return u, v

def setNamespace():
    ns = getNamespace()
    print 'set namespace to: "'+ns+'"',

    return cmds.namespace(set=ns)

def getNodeType(node=cmds.ls(sl=True, long=True)):
    if node:
        nodeShape = cmds.listRelatives(node[0], shapes=True, f=True)[0]
        return cmds.nodeType(nodeShape)
    else:
        cmds.warning('Please select a node')
        return None

def openFile(filename, software='gedit', shell=True):
    """ open a given file with a given software """
    if not os.path.exists(filename):
        raise UserWarning("This file doesn't exists...")
    if not software:
        raise UserWarning("Software not specified...")
    command = software+' '+filename+' &'
    popObj = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = popObj.communicate()
    
    return out[0]

def replaceDefaultPersp():
    """ delete the default persp and recreate a new fresh one """
    # find the default startup persp and delete it
    defaultPersp = mel.eval('findStartUpCamera( "persp");')
    cmds.camera(defaultPersp, e=True, sc=False)
    cmds.delete(defaultPersp)
    # create new persp, hide it and set it as default startup persp
    newPersp = cmds.camera(n='persp', hc="viewSet -p %camera")
    cmds.setAttr(newPersp[0]+'.visibility', False)
    cmds.rename(newPersp[0], 'persp')
    cmds.camera('persp', e=True, sc=True)

def texmaker(inputfile, outputfile):
    """
        convert exr input file to tex file
    """
    cmd = 'txmake -resize up -smode black -tmode black '+inputfile+' '+outputfile
    print '> converting', inputfile, outputfile
    popObj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = popObj.communicate()
    return out[0]

def combine():
    """
    clean combine

    """
    selection = cmds.ls(sl=True, type='mesh', dag=True)
    if not selection or selection < 2:
        cmds.warning('Please select at least 2 meshes!')

    # get full path
    meshFull = cmds.listRelatives(selection[0], p=True, f=True)
    # get parent
    meshParent = cmds.listRelatives(meshFull, p=True, f=True)
    meshInWorld = []
    if meshParent:
        meshParent0 = meshParent[0]
        meshInWorld.append(cmds.parent(meshFull, world=True)[0])
    else:
        meshInWorld = meshFull
    # replace 1st mesh in sel by mesh in world
    selection[0] = meshInWorld[0]
    # get pivots
    pivots = cmds.xform(meshInWorld[0], q=True, ws=True, a=True, rotatePivot=True)
    # combine & rename
    newMesh = cmds.polyUnite(selection, o=True)
    newMeshName = cmds.rename(newMesh[0], meshInWorld[0])
    # set pivot
    cmds.xform(newMeshName, rotatePivot=pivots)
    # reparent
    if meshParent:
        newMeshName = cmds.parent(newMeshName, meshParent, a=True)

    # delete history
    cmds.delete(newMeshName, ch=True, hi='none')

def faceSeparate():
    """
    clean separate

    """
    faces = cmds.ls(sl=True, fl=True)
    temp = faces[0].split('.')

    if not faces or len(temp) == 1 or len(faces) == cmds.polyEvaluate(f=True):
        cmds.error('Select at lease one face and not the entire mesh!')
    
    temp = faces[0].split('.')
    mesh = temp[0]
    temp = cmds.duplicate(mesh, n=mesh, rr=True)
    newMesh = temp[0]
    new = cmds.ls(newMesh+'.f[*]', fl=True)

    ii = 0
    newFaceDelete = []

    for face in new:
        hit = False
        temp = new[ii].split('.')
        newFace = temp[1]
        o = 0
        for f in faces:
            temp = faces[o].split('.')
            oldFace = temp[1]
            o = o+1
            if newFace == oldFace:
                hit = True
                break
        if not hit:
            newFaceDelete.append(new[ii])
        ii = ii+1
    cmds.delete(newFaceDelete)
    cmds.delete(faces)
    cmds.select(newMesh)
    cmds.xform(cp=True)

    return newMesh

def createCameraUVProj():
    sel = cmds.ls(sl=True)
    if sel:
        for node in sel:
            if cmds.polyEvaluate(node, fc=True) == 0:
                cmds.select(node+'.f[*]', add=True)
        cmds.polyProjection(cmds.ls(sl=True), ch=True, type='Planar', ibd=True, kir=True, md='c')

def averageNormals():
    try:
        cmds.polyNormalPerVertex(ufn=True)
        cmds.polyAverageNormal(
                                prenormalize=False,
                                allowZeroNormal=False,
                                postnormalize=True,
                                distance=0.1,
                                replaceNormalXYZ=(1,0,0))
    except:
        cmds.polyAverageNormal(
                                prenormalize=False,
                                allowZeroNormal=False,
                                postnormalize=True,
                                distance=0.1,
                                replaceNormalXYZ=(1,0,0))
       
def setPerspSetting():
    if cmds.ls('perspShape'):
        cmds.setAttr('perspShape.nearClipPlane', perspNear)
        cmds.setAttr('perspShape.farClipPlane', perspFar)
    else:
        cmds.warning('Cannot find the persp camera!')

def selectObjectsFromShader(shader):
    """
    select objects with lambert1 assigned
    """
    cmds.hyperShade(objects=shader)

def setUserSetting():
    
    # ask for a Setting name
    result = cmds.promptDialog(
                    title='Save selection',
                    message='Enter Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
    
    if result == 'OK':
        inputText = cmds.promptDialog(query=True, text=True)
        SETTINGS.add(inputText, cmds.ls(sl=True))
        print SETTINGS.get('faceSelection')

def getUserSetting():
    allSettings = SETTINGS.gets()
    lines = []
    for item in allSettings:
        lines.append(item.keys()[0])
    
    if cmds.window('settingsWindow', exists=True):
        cmds.deleteUI('settingsWindow', window=True)

    window = cmds.window('settingsWindow')
    cmds.paneLayout()
    cmds.textScrollList('settingsList',
                        numberOfRows=8,
                        allowMultiSelection=True,
                        append=lines,
                        dcc=selectSetting)
    
    cmds.showWindow('settingsWindow')

def selectSetting():
    settingText = cmds.textScrollList('settingsList',
                        q=True,
                        si=True)
    try:
        cmds.select(SETTINGS.get(settingText[0]))
    except:
        print 'failed to select setting...'

def makeTube():
    """
    makes a simple tube mesh
    """
    mesh = cmds.polyTorus(r=2, sr=0.2,  sx=50, sy=4, tw=45)
    cmds.setAttr(mesh[0]+'.sy', 5)

def softEdgeSelection(angle=normalAngle, history=True):
    """
    unlock normals and soft edge
    """
    sel = cmds.ls(sl=True)
    for node in sel:
        cmds.polyNormalPerVertex(node, ufn=True)
        cmds.polySoftEdge(node, angle=angle, ch=history)
        
def invertSelection():
    """invert selection"""
    mel.eval('invertSelection;')

def replaceXformSel():
    """duplicate the first object in selection and move it to the world space
        coordinates of the next object in selection.
    """
    source = cmds.ls(sl=True)[0]
    rest = cmds.ls(sl=True)[1:]
    for node in rest:
        dup = cmds.duplicate(source)[0]
        translate = cmds.xform(node, ws=True, t=True, q=True)
        rotation = cmds.xform(node, ws=True, ro=True, q=True)
        cmds.xform(dup, t=translate, ro=rotation)

def mergeUVs():
    """merge selected uvs"""
    mel.eval('polyPerformAction "polyMergeUV -d 1" v 0;')
    mel.eval('changeSelectMode -component;')
    mel.eval('setComponentPickMask "Point" true;')
    mel.eval('selectType -ocm -alc false;')
    mel.eval('selectType -ocm -vertex true;')
    mel.eval('selectType -sf false -se false -suv false -cv false;')

def selectInsideFaces():
    """select all the edges inside an object except the border."""
    sel = cmds.ls(sl=True)[0]
    cmds.select(sel+'.e[*]')
    mel.eval('polyConvertToShellBorder;')
    mel.eval('ConvertSelectionToFaces;')
    mel.eval('invertSelection')

def toggleVertexColorDisplay():
    """toggle the color vertex display"""
    sel = cmds.ls(sl=True)
    if sel:
        for node in sel:
            mel.eval('toggleShadeMode;')
    else:
        cmds.select(all=True)
        mel.eval('toggleShadeMode;')

def headsUpDisplayMessage(message):
    """function that displays a custom heads up display message"""
    cmds.headsUpMessage(message,
                    verticalOffset=350,
                    horizontalOffset=0)

def shortestEdgePath():
    """enter polyShortestPathCtx """
    polyPathContex = cmds.polyShortestPathCtx()
    cmds.setToolTo(polyPathContex)

def shortestEdgePathRelease():
    cmds.setToolTo('moveSuperContext')
    cmds.selectMode(component=True)
    cmds.selectType(eg=True)

def switchObjectTumble():
    headsUpDisplayMessage(message='Tumble object focus: '+str(not cmds.tumbleCtx('tumbleContext', objectTumble=True, q=True)))
    cmds.tumbleCtx('tumbleContext', ac=True,
        objectTumble=not cmds.tumbleCtx('tumbleContext', objectTumble=True, q=True),
        e=True)

def unfoldAndRotate(sel):
    # unfold horizontal
    cmds.unfold(sel+'.map[*]',
        i=5000,
        ss=0.001,
        gb=0.0,
        gmb=0.5,
        pub=False,
        ps= False,
        oa=2, # 1: vertical, 2:horizontal
        us=False)
    # unfold vertical
    cmds.unfold(sel+'.map[*]',
        i=5000,
        ss=0.001,
        gb=0.0,
        gmb=0.5,
        pub=False,
        ps= False,
        oa=1, # 1: vertical, 2:horizontal
        us=False)
    # rotate UVs
    cmds.polyEditUV(pivotU=0.5, pivotV=0.5, angle=90)
    
def unwrapTerrain(sel):
    # unwrap planar Y
    cmds.polyProjection(sel+'.f[*]',
                                    ch=False,
                                    type='Planar',
                                    ibd=True,
                                    isu=1,
                                    isv=1,
                                    md='y')
    # apply unfoldAndRotate x times
    for i in range(4):
        unfoldAndRotate(sel)

def proMode():
    """pro mode"""
    mel.eval('ToggleUIElements')

def freezeHistory():
    """freezeHistory"""
    mel.eval('delete -ch;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;')

def freezeCenterPivot():
    """freezeCenterPivot"""
    mel.eval('delete -ch;xform -cp;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;')

def centerPivot():
    """centerPivot"""
    mel.eval('xform -cp;')

def mergeVertex():
    """merge vertex"""
    sel = cmds.ls(sl=True)
    if sel:
        try:
            for node in sel:
                cmds.select(node, r=True)
                cmds.polyMergeVertex(distance=0.01, am=True, ch=True)
        except:
            pass
        cmds.select(sel, r=True)

def getVertexColor():
    selection = cmds.ls(sl=True)
    colors = {}
    for obj in selection:
        colors[obj] = {}
        for v in range(cmds.polyEvaluate(v=True)):
            cmds.select(obj+'.vtx['+str(v)+']', r=True)
            colors[obj][v] = cmds.polyColorPerVertex(query=True, g=True, b=True)
    return colors

def newScriptEditor():
    """new script editor test"""
    win = cmds.window(t='New Script Editor', menuBar= True, w = 650, h = 300)
    form = cmds.formLayout()
    pane = cmds.paneLayout(configuration='horizontal2', paneSize=[[1,100,40],[2,100,60]])
    # top layout
    formTop = cmds.formLayout()
    reporter = cmds.cmdScrollFieldReporter('reporter')
    cmds.setParent('..')
    cmds.formLayout(formTop, e=True,
            attachForm=\
                [
                    (reporter, "top", 5),
                    (reporter, "bottom", 5),
                    (reporter, "left", 5),
                    (reporter, "right", 5),
                ]
        )
    cmds.paneLayout(pane, edit=True, setPane = [formTop, 2])
    # bottom layout
    formBottom = cmds.formLayout()
    shelf = cmds.shelfTabLayout()
    tab1 = cmds.cmdScrollFieldExecuter('python1', sourceType="python")
    cmds.setParent('..')
    cmds.formLayout(formBottom, e=True,
            attachForm=\
                [
                    (shelf, "top", 5),
                    (shelf, "bottom", 5),
                    (shelf, "left", 5),
                    (shelf, "right", 5),
                ]
        )
    
    cmds.paneLayout(pane, edit=True, setPane = [formTop, 1])
    
    cmds.formLayout(form, e=True,
            attachForm=\
                [
                    (pane, "top", 5),
                    (pane, "bottom", 5),
                    (pane, "left", 5),
                    (pane, "right", 5),
                ]
        )
    
    cmds.showWindow()

def launchTerminal():
    cmd = 'gnome-terminal'
    popObj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = popObj.communicate()

def launchConsole():
    """launch console2 from maya"""
    
    # get the console path from default
    defaultConsolePath = [
        'C:/Program Files/Console2/Console.exe',
        'C:/Program Files (x86)/Console2/Console.exe',
        ]
    for path in defaultConsolePath:
        if os.path.exists(path):
            SETTINGS.add('terminator', path)

    consolePath = SETTINGS.get('terminator')
    if consolePath and os.path.exists(consolePath):
        # launch console
        subprocess.Popen(consolePath[0])
    else:
        # ask for the console exe path
        filedialog = cmds.fileDialog2(cap='Please give me the path of Console.exe !',
                        fm=1,
                        dir='C:\\Program Files\\',
                        ff='*.exe')
        if filedialog:
            consolePath = str(filedialog[0])
            if os.path.exists(consolePath):
                # setting Setting
                SETTINGS.add('terminator', consolePath)
                # launch console
                subprocess.Popen(consolePath)
        else:
            raise UserWarning('No exe found !')

def sublimeTextPathFinder():
    """launch sublime text from maya"""
    
    # get the sublime text path from default
    defaultSublimePath = [
        'C:/Program Files/sublime_text/sublime_text.exe',
        'C:/Program Files/Sublime Text 2/sublime_text.exe',
        'C:/Program Files (x86)/Sublime Text 2/sublime_text.exe',
        ]
    for path in defaultSublimePath:
        if os.path.exists(path):
            SETTINGS.add('sublime_text_path', path)

    sublimeTextPath = SETTINGS.get('sublime_text_path')
    if sublimeTextPath and os.path.exists(sublimeTextPath):
        # launch sublime text
        subprocess.Popen(sublimeTextPath[0])
    else:
        # ask for the sublime text exe path
        filedialog = cmds.fileDialog2(cap='Please give me the path of Sublime Text.exe !',
                        fm=1,
                        dir='C:\\Program Files\\',
                        ff='*.exe')
        if filedialog:
            sublimeTextPath = str(filedialog[0])
            if os.path.exists(sublimeTextPath):
                # setting Setting
                SETTINGS.add('sublime_text_path', sublimeTextPath)
                return sublimeTextPath
        else:
            raise UserWarning('No exe found !')

def launchSublimeText():
    path = sublimeTextPathFinder()
    subprocess.Popen(path)

def nukePathFinder():
    """
    get nuke exe/bin path
    """
    # windows
    if PLATFORM == 'Windows':
        defaultNukePath = [
        'C:/Program Files/Nuke7.0v4/Nuke7.0.exe',
                            ]
        searchDir = 'C:\\Program Files\\'
        fileFilter = '*.exe'
    # linux
    if PLATFORM == 'Linux':
        defaultNukePath = [
        os.getenv('NUKE')+'/nuke',
                            ]
        searchDir = '/'
        fileFilter = '*'

    # check if the default path exists 
    for path in defaultNukePath:
        if os.path.exists(path):
            SETTINGS.add('nukePath', path)
    
    # get the nuke path setting if exists
    nukePath = SETTINGS.get('nukePath')
    if nukePath:
        if os.path.exists(nukePath):
            return nukePath
        else:
            raise UserWarning('No exe found !')
    else:
        # ask for the sublime text exe path
        filedialog = cmds.fileDialog2(cap='Please give me the path of Nuke exe/bin !',
                        fm=1,
                        dir=searchDir,
                        ff=fileFilter)
        if filedialog:
            nukePath = str(filedialog[0])
            if os.path.exists(nukePath):
                # setting setting
                SETTINGS.add('nukePath', nukePath)
                return nukePath
            else:
                raise UserWarning('No Nuke found !')
        else:
            raise UserWarning('No Nuke found !')

def launchNuke():
    path = nukePathFinder()
    subprocess.Popen(path+" --nukex")

def setDefaultRenderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=False, displayLights='default', e=True)
    cmds.modelEditor(panel, rnm='base_OpenGL_Renderer', e=True)
    headsUpDisplayMessage('Default renderer')

def setHardwareRenderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=True, displayLights='default', e=True)
    cmds.modelEditor(panel, rnm='hwRender_OpenGL_Renderer', e=True)
    headsUpDisplayMessage('Hardware renderer')

def setViewport2Renderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=True, displayLights='default', e=True)
    cmds.modelEditor(panel, rnm='ogsRenderer', e=True)
    headsUpDisplayMessage('Viewport 2 renderer')

def assignSurfaceShader(name="", values=(0,0,0)):

    selection = cmds.ls(sl = True)
    print name, selection, values[0], values[1], values[2]
    
    if selection:
        # if the shader already exists
        if name in cmds.ls("*", type = "surfaceShader") and name+"SG" in cmds.ls("*", type = "shadingEngine"):
            for node in selection:
                try:
                    cmds.select(node, r = True)
                    cmds.sets(node, e = True, forceElement = name+"SG")
                except:
                    pass
                    
        # otherwise create the shader
        else:
            shader = cmds.shadingNode('surfaceShader', asShader = True, name = name)
            shadingGroup = cmds.sets(shader, renderable = True, noSurfaceShader = True, empty = True, name = name+"SG")
            cmds.connectAttr(shader+".outColor", shadingGroup+".surfaceShader", force = True)
            cmds.setAttr(shader+".outColor", values[0], values[1], values[2], type = "double3")
        
            for node in selection:
                try:
                    cmds.sets(node, e = True, forceElement = name+"SG")
                except:
                    pass
            
        cmds.select(selection, r = True)

def askFlushUndo():
    confirm = cmds.confirmDialog(t="flushUndo",
                                 m='Do you want to flush undo ?',
                                 ma="center",
                                 b=['Yes','No'],
                                 db='Yes',
                                 cb='No',
                                 ds='No')
                                
    if confirm == "Yes":
        print "flushUndo..."
        cmds.flushUndo()
    else:
        print "abort..."

def undoQueue(undos=100):
    # set the undo queue 
    cmds.undoInfo(state=True, infinity=False, length=undos)
    
def switchHighlightedSelection():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, edit=True, sel=not cmds.modelEditor(panel, query=True, sel=True))
    headsUpDisplayMessage('Selection highlight: '+str(cmds.modelEditor(panel, query=True, sel=True)))

def transferVertices(meshes=[], preserveUVs=True):
    
    dateStart = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    
    if len(meshes) == 2:
        verticesRange1 = int(cmds.ls(meshes[0]+".vtx[*]")[0].split(":")[-1][:-1])
        verticesRange2 = int(cmds.ls(meshes[1]+".vtx[*]")[0].split(":")[-1][:-1])
        if verticesRange1 == verticesRange2:
            for vertex in range(verticesRange1+1):
                vertexName1 = meshes[0]+".vtx["+str(vertex)+"]"
                vertexName2 = meshes[1]+".vtx["+str(vertex)+"]"
                xform1 = cmds.xform(vertexName1, q=True, ws=True, t=True)
                xform2 = cmds.xform(vertexName2, q=True, ws=True, t=True)
                #print " > moving", meshes[0], "vtx", vertex, "to", xform2
                cmds.select(vertexName1, r = True)
                cmds.move(xform2[0], xform2[1], xform2[2], ws=True, puv=preserveUVs)
        
        else:
            cmds.warning("The selection doesn't have the same vertex count !")
    else:
        cmds.warning("Please select 2 objects !")
        
    dateEnd = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    print " > Process started at", dateStart, "and ended at", dateEnd

def toggleNormals():
    #toggle normals
    cmds.polyOptions(r=True,
                    f=True,
                    dn=not cmds.polyOptions(q=True, dn=True))
    headsUpDisplayMessage('Polygon normal display: '+str(cmds.polyOptions(q=True, dn=True)))
    
def unselectAll():
    # unselect all
    cmds.selectMode(component=True)
    cmds.selectMode(object=True)
    cmds.select(clear=True)
    
def setWireframe():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel,
                    e=True,
                    wireframeOnShaded=not cmds.modelEditor(panel, query=True, wireframeOnShaded=True))
    headsUpDisplayMessage('Wireframe on shaded: '+str(cmds.modelEditor(panel, query=True, wireframeOnShaded=True)))

def setBackfaceCulling():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel,
                    e=True,
                    backfaceCulling=not cmds.modelEditor(panel, query=True, backfaceCulling=True))
    headsUpDisplayMessage('Backface culling: '+str(cmds.modelEditor(panel, query=True, backfaceCulling=True)))
    
def setDefaultMaterial():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, edit=True, useDefaultMaterial=not cmds.modelEditor(panel, query=True, useDefaultMaterial=True))
    headsUpDisplayMessage('Default material: '+str(cmds.modelEditor(panel, query=True, useDefaultMaterial=True)))

def tweakMultiComponents():
    cmds.selectType(meshComponents=True)

def bufMove():
    """enter the Buf move vertex mode"""
    cmds.selectMode(component=True)
    cmds.selectMode(object=True)
    sel = cmds.ls(sl=True)
    # enter the move mode and set on vertex
    if sel:
        shape = cmds.listRelatives(sel[0])
        if cmds.nodeType(shape) == 'nurbsCurve':
            try:
                cmds.delete(sel, ch=True)
                cmds.selectMode(component=True)
                activePanel = cmds.getPanel(withFocus=True)
                cmds.modelEditor(activePanel, e=True, manipulators=False)
                cmds.setToolTo('moveSuperContext')
                cmds.selectType(alc=0)
                cmds.selectType(controlVertex=1)
                cmds.selectPref(clickDrag=True)
            except:
                pass

        if cmds.nodeType(shape) == 'mesh':
            try:
                cmds.delete(sel, ch=True)
                cmds.selectMode(component=True)
                activePanel = cmds.getPanel(withFocus=True)
                cmds.modelEditor(activePanel, e=True, manipulators=False)
                cmds.setToolTo('moveSuperContext')
                cmds.selectType(alc=0)
                cmds.selectType(vertex=1)
                cmds.selectPref(clickDrag=True)
            except:
                pass
        else:
            try:
                cmds.delete(sel, ch=True)
                cmds.selectMode(component=True)
                activePanel = cmds.getPanel(withFocus=True)
                cmds.modelEditor(activePanel, e=True, manipulators=False)
                cmds.setToolTo('moveSuperContext')
                cmds.selectType(alc=0)
                cmds.selectType(vertex=1)
                cmds.selectPref(clickDrag=True)
            except:
                pass
        #cmds.selectPref(useDepth = True)

def bufMoveMulti():
    """enter the Buf move vertex mode"""
    try:
        cmds.selectMode(object=True)
        selection = cmds.ls(sl=True)
        cmds.selectMode(component=True)
        cmds.selectMode(object=True)
        cmds.selectMode(component=True)
        for node in selection:
            cmds.delete(node, ch=True)
            mel.eval('doMenuComponentSelection("'+node+'", "meshComponents");')

        activePanel = cmds.getPanel(withFocus=True)
        cmds.modelEditor(activePanel, e=True, manipulators=False)
        cmds.setToolTo('moveSuperContext')
        cmds.selectPref(clickDrag=True)
    except:
        pass

def bufMoveRelease():
    """release the Buf move vertex mode"""
    activePanel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(activePanel, e=True, manipulators=True)
    cmds.setToolTo('moveSuperContext')
    cmds.selectPref(clickDrag=False)
    cmds.selectMode(component=True)
    cmds.selectMode(object=True)
    #cmds.selectPref(useDepth = False)

def importScene():
    """import scene exported from nuke"""
    crosswalkFile = 'nukeToMaya.info'
    if os.path.exists(crosswalkFile):
        fileInfo = open(crosswalkFile, 'r')
        mayaFile = fileInfo.readlines()[-1].split('=')[-1][:-1]
        if os.path.exists(mayaFile):
            cmds.file(mayaFile, i = True, type = 'mayaAscii', ra = True)
        else:
            print mayaFile
            mel.eval('warning "File '+mayaFile+' not found !"')

def isolateSelection():
    """isolate selection toggle"""
    activePanel = cmds.getPanel(wf=True)
    mel.eval('isoSelectAutoAddNewObjs '+activePanel+' true;')
    mel.eval("enableIsolateSelect {0} {1};".format(activePanel, str(not cmds.isolateSelect(activePanel, q=True, state=True)).lower()))

def hideSel():
    
    sel = cmds.ls(sl=True)
    for node in sel:
        cmds.setAttr(node+'.visibility', 0)
        
def hideSelSwitch():
    
    sel = cmds.ls(sl=True)
    for node in sel:
        cmds.setAttr(node+'.visibility', not cmds.getAttr(node+'.visibility'))

def hideSelRelease():
    
    sel = cmds.ls(sl=True, dag=True)
    for node in sel:
        cmds.setAttr(node+'.visibility', 1)

def assignBlackShader():

    global switch
    activeModel = cmds.getPanel(wf=True)
    cmds.modelEditor(activeModel, e=True, udm=1)
    cmds.displayRGBColor( 'background', 0, 0, 0 )
    cmds.setAttr('lambert1.color', 0, 0, 0, type="double3")
    cmds.setAttr('lambert1.diffuse', 0)
    cmds.displayRGBColor('userDefined1', 1 ,1 ,1 )

    for node in cmds.ls(sl = True):
        cmds.color(ud = 1) # assign white wireframes
    switch = 1

def assignDefaultShader():

    global switch
    activeModel = cmds.getPanel(wf=True)
    cmds.modelEditor(activeModel, e=True, udm=0)
    cmds.displayRGBColor( 'background', 0.61, 0.61, 0.61 )
    cmds.setAttr('lambert1.color', 0.5, 0.5, 0.5, type="double3")
    cmds.setAttr('lambert1.diffuse', 0.5)
    for node in cmds.ls(sl=True):
        cmds.color() # assign default wireframes
    switch = 1

def switchShaders():

    global switchshader
    try:
        switchshader
    except:
        switchshader = 1

    if switchshader == 1:
        assignBlackShader()
        switchshader = 0
    elif switchshader == 0:
        assignDefaultShader()
        switchshader = 1

def getCam():
    sel = cmds.ls(sl = True)
    if sel:
        camShape = cmds.listRelatives(sel[0])[0]
        if cmds.nodeType(camShape) == 'camera':
            setRenderCamera(sel[0], camShape)

def cameraPanTool():
    headsUpDisplayMessage('Camera 2d pan mode')
    panContext = cmds.panZoomCtx(panMode=True)
    cmds.setToolTo(panContext)
    
def cameraZoomTool():
    headsUpDisplayMessage('Camera 2d zoom mode')
    zoomContext = cmds.panZoomCtx(zoomMode=True)
    cmds.setToolTo(zoomContext)

def resetPanZoom():
    panel = cmds.getPanel(wf=True)
    cameraNode = cmds.modelPanel(panel, q=True, camera=True)

    cmds.setAttr(cameraNode+".zoom", 1)
    cmds.setAttr(cameraNode+".horizontalPan", 0)
    cmds.setAttr(cameraNode+".verticalPan", 0)

def polySplitTool():
    polysplit = cmds.polySplitCtx()
    cmds.setToolTo(polysplit)

def selectNgones():
    panel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(panel, e=True, manipulators=False)
    cmds.selectMode(component=True)
    cmds.selectType(fc=1)
    cmds.polySelectConstraint(m=3, t=8, sz=3)
    
def selectNgonesRelease():
    panel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(panel, e=True, manipulators=True)
    cmds.select(clear=True)
    cmds.selectMode(object=True)
    cmds.polySelectConstraint(m=0)

def switchSelectNgones():
    global switchselectngones
    try:
        switchselectngones
    except:
        switchselectngones = 1

    if switchselectngones == 1:
        selectNgones()
        switchselectngones = 0
    elif switchselectngones == 0:
        selectNgonesRelease()
        switchselectngones = 1

def selectTriangles():
    panel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(panel, e=True, manipulators=False)
    cmds.selectMode(component=True)
    cmds.selectType(fc=1)
    cmds.polySelectConstraint(m=3, t=8, sz=1)

def selectTrianglesRelease():
    panel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(panel, e=True, manipulators=True)
    cmds.select(clear=True)
    cmds.selectMode(object=True)
    cmds.polySelectConstraint(m=0)

def switchSelectTriangles():
    global switchselecttriangles
    try:
        switchselecttriangles
    except:
        switchselecttriangles = 1

    if switchselecttriangles == 1:
        selectTriangles()
        switchselecttriangles=0
    elif switchselecttriangles == 0:
        selectTrianglesRelease()
        switchselecttriangles = 1

def setDefaultLight():
    activePanel = cmds.getPanel(wf=True)
    cmds.modelEditor(activePanel, e=True, dl="default")

def setAllLight():
    activePanel = cmds.getPanel(wf=True)
    cmds.modelEditor(activePanel, edit=True, displayLights='all')

def switchLight():
    global switchlight
    try:
        switchlight
    except:
        switchlight = 1

    if switchlight == 1:
        setDefaultLight()
        switchlight = 0
    elif switchlight == 0:
        setAllLight()
        switchlight = 1
   
def lockPickNodes(lock=True):
    for node in cmds.ls(sl=True):
        try:
            cmds.lockNode(node, lock=lock)
        except:
            cmds.warning("cannot lockPick this node: "+str(node))
            
