"""
dmptool modeling module

"""
# system modules
import time
# maya modules
from maya import cmds, mel
# dmptools modules
import dmptools.utils.mayaCommands as mayaCommands
from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('maya_modeling')

def alignVertices(minX, maxX, minY, maxY, minZ, maxZ):
    """
    align vertices in 3d
    """
    # get the selected vertices from current selection
    selectedItems = cmds.filterExpand(ex=False, sm=31) # 31 means vertices
    # get the 3d bounding box of selection
    bInfo = cmds.polyEvaluate(bc=True)
    xmin = bInfo[0][0]
    xmax = bInfo[0][1]
    ymin = bInfo[1][0]
    ymax = bInfo[1][1]
    zmin = bInfo[2][0]
    zmax = bInfo[2][1]
    
    if minX:
        cmds.move(xmin, moveX=True)
    if maxX:
        cmds.move(xmax, moveX=True)
    if minY:
        cmds.move(ymin, moveY=True)
    if maxY:
        cmds.move(ymax, moveY=True)
    if minZ:
        cmds.move(zmin, moveZ=True)
    if maxZ:
        cmds.move(zmax, moveZ=True)

def alignUVs(doU, minU, doV, inV):
    """
    align selected uvs based on the one most on top, bottom, left, right
    """
    # get the selected UVs from current selection
    selectedItems = cmds.filterExpand(ex=False, sm=35) # 35 means UVs
    uvMin = []
    uvMax = []
    # get the 3d bounding box of selection
    uvInfo = cmds.polyEvaluate(bc2=True)
    uvMin[0] = uvInfo[0]
    uvMin[1] = uvInfo[2]
    uvMax[0] = uvInfo[1]
    uvMax[1] = uvInfo[3]

    if doU:
        if minU:
            cmds.polyEditUV(r=False, u=uvMin[0])
        else:
            cmds.polyEditUV(r=False, u=uvMax[0])
    if doV:
        if minV:
            cmds.polyEditUV(r=False, v=uvMin[1])
        else:
            cmds.polyEditUV(r=False, v=uvMax[1])

def makeTube():
    """
    makes a simple tube mesh
    """
    mesh = cmds.polyTorus(r=2, sr=0.2,  sx=50, sy=4, tw=45)
    cmds.setAttr(mesh[0]+'.sy', 5)

def mergeVertex(defaultValue=0.1):
    """
    merge selected vertices
    """
    dist = SETTINGS.get('default_merge_distance')
    if dist == None:
        dist = defaultValue
        SETTINGS.add('default_merge_distance', dist)

    selection = cmds.ls(sl=True)
    if selection:
        try:
            for node in selection:
                cmds.select(node, r=True)
                cmds.polyMergeVertex(distance=dist, am=True, ch=True)
        except:
            pass
        cmds.select(selection, r=True)

def mergeUVs(defaultValue=1.0):
    """
    merge selected uvs **to translate to python**
    """
    dist = SETTINGS.get('default_mergeUVs_distance')
    if dist == None:
        dist = defaultValue
        SETTINGS.add('default_mergeUVs_distance', dist)

    mel.eval('polyPerformAction "polyMergeUV -d '+value+'" v 0;')
    mel.eval('changeSelectMode -component;')
    mel.eval('setComponentPickMask "Point" true;')
    mel.eval('selectType -ocm -alc false;')
    mel.eval('selectType -ocm -vertex true;')
    mel.eval('selectType -sf false -se false -suv false -cv false;')

def softEdgeSelection(defaultAngle=180, history=True):
    """
    unlock normals and soft edge 
    """
    normalAngle = SETTINGS.get('default_normal_angle')
    if normalAngle == None:
        normalAngle = angle
        SETTINGS.add('default_normal_angle', normalAngle)

    selection = cmds.ls(sl=True)
    for node in selection:
        # unlock
        cmds.polyNormalPerVertex(node, ufn=True)
        # soften
        cmds.polySoftEdge(node, angle=normalAngle, ch=history)

def averageNormals():
    """
    poly average normals
    """
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

def combine():
    """
    a cleaner combine
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
    a cleaner face separate
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
    """
    create a UVs projection based on the active camera
    """
    selection = cmds.ls(sl=True)
    for node in selection:
        if cmds.polyEvaluate(node, fc=True) == 0:
            cmds.select(node+'.f[*]', add=True)
    cmds.polyProjection(cmds.ls(sl=True), ch=True, type='Planar', ibd=True, kir=True, md='c')

def transferVertices(meshes=[], preserveUVs=True):
    """
    transfer vertex position from one obeject to another
    the 2 objects should have the same amount of vertices
    """
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

def tweakMultiComponents():
    """
    set select type to multicomponents
    """
    cmds.selectType(meshComponents=True)

def advanceMove():
    """
    enter a custom click and drag selection mode
    this is to be used with 'advanceMoveRelease'
    """
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

def advanceMoveMulti():
    """
    same as advanceMove but with multicomponents enable
    """
    cmds.selectMode(object=True)
    selection = cmds.ls(sl=True)
    cmds.selectMode(component=True)
    cmds.selectMode(object=True)
    cmds.selectMode(component=True)
    for node in selection:
        cmds.delete(node, ch=True)
        cmds.selectType(meshComponents=True)
        cmds.hilite(node)
        cmds.select(clear=True)
        #mel.eval('dR_selTypeChanged("meshComponents");')

    activePanel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(activePanel, e=True, manipulators=False)
    cmds.setToolTo('moveSuperContext')
    cmds.selectPref(clickDrag=True)

def advanceMoveMultiExtrude():
    """
    enter a mutlicomponents click and drag extrude mode
    """
    advanceMoveMulti()
    # enters extrude mode
    mel.eval('nexOpt -e manipType extrude;dR_updateCommandPanel();dR_addRepeatManip("extrude");')

def advanceMoveRelease():
    """
    release action of advanceMove
    """
    activePanel = cmds.getPanel(withFocus=True)
    cmds.modelEditor(activePanel, e=True, manipulators=True)
    cmds.setToolTo('moveSuperContext')
    cmds.selectPref(clickDrag=False)
    cmds.selectMode(component=True)
    cmds.selectMode(object=True)

def oldSplitEdge():
    """
    default edge split tool
    """
    mel.eval("SplitPolygonTool;")

def splitEdgeRing():
    """
    default edge ring tool
    """
    mel.eval("SplitEdgeRingTool;")
    
def splitEdgeRingRelease(flow=False, flowValue=0.5, smoothingAngle=35):
    """
    default edge ring tool release mode
    """
    # check for default values saved in preferences (settings)
    followFlow = SETTINGS.get('egde_split_flow')
    if not 'followFlow' in locals():
        followFlow = flow
        SETTINGS.add('egde_split_flow', followFlow)
    followFlowValue = SETTINGS.get('egde_split_flow_value')
    if not 'followFlowValue' in locals():
        followFlowValue = flowValue
        SETTINGS.add('egde_split_flow_value', followFlowValue)
    smoothingValue = SETTINGS.get('egde_split_smoothing_value')
    if not 'smoothingValue' in locals():
        smoothingValue = smoothingAngle
        SETTINGS.add('egde_split_smoothing_value', smoothingValue)

    if followFlow:
        cmds.polySplitRing(ch=True,
                        splitType=1,
                        weight=0.5,
                        smoothingAngle=smoothingValue,
                        fixQuads=True,
                        insertWithEdgeFlow=True,
                        adjustEdgeFlow=followFlowValue)
    else:
        cmds.polySplitRing(ch=True,
                        splitType=1,
                        weight=0.5,
                        smoothingAngle=smoothingValue,
                        fixQuads=True,
                        insertWithEdgeFlow=False)

    advanceMoveRelease()

def polySplitTool():
    """
    default poly split tool
    """
    polysplit = cmds.polySplitCtx()
    cmds.setToolTo(polysplit)
