#================================================
#
# ArcSystem
# michael-ha@moving-picture.com
#
# With a given single curve, the script creates a curve system with several
# controls and a mesh system attached/skinned to the curves.
# 
#================================================

import maya.cmds as cmds
import math
import random
import os
import time

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('maya_arc_system')

# strings to be generated by the install
PLATFORM = '!PLATFORM!'
TEMPPATH = '!TEMPPATH!'
WINDOWNAME = "ArcMainWindow"

class CreateArcs(object):
    def __init__(self, *args):
        
        arcSystem = {}
        # arc generic values
        arcSystem["baseCurve"] = [cmds.textFieldButtonGrp("ArcCurveTxt", q=True, text=True)]
        arcSystem["MeshNumber"] = cmds.intFieldGrp("ArcNumberMesh", q = True, value = True)
        # arc values
        arcSystem["values"] = {}
        arcSystem["values"]["smooth"] = cmds.intFieldGrp("arc_values_smooth", q=True, value=True)
        arcSystem["values"]["numRounds"] = cmds.intFieldGrp("arc_values_numRound", q=True, value=True)
        arcSystem["values"]["radius"] = cmds.floatFieldGrp("arc_values_radius", q=True, value=True)
        arcSystem["values"]["profileScale"] = cmds.floatFieldGrp("arc_values_profil_scale", q=True, value=True)
        arcSystem["values"]["translate"] = [0, 0, -2]
        arcSystem["values"]["rotate"] = cmds.floatFieldGrp("arc_values_rotate", q=True, value=True)
        arcSystem["values"]["scale"] = cmds.floatFieldGrp("arc_values_scale", q=True, value=True)
        arcSystem["values"]["rotateWire"] = cmds.floatFieldGrp("arc_values_wire_rotation", q=True, value=True)
        arcSystem["values"]["dropoff"] = cmds.floatFieldGrp("arc_values_wire_dropoff", q=True, value=True)
        
        # store settings
        SETTINGS.add('arc_values_smooth', arcSystem["values"]["smooth"][0])
        SETTINGS.add('arc_values_numRound', arcSystem["values"]["numRounds"][0])
        SETTINGS.add('arc_values_radius', arcSystem["values"]["radius"][0])
        SETTINGS.add('arc_values_profil_scale', arcSystem["values"]["profileScale"][0])
        SETTINGS.add('arc_values_rotate', arcSystem["values"]["rotate"])
        SETTINGS.add('arc_values_scale', arcSystem["values"]["scale"])
        SETTINGS.add('arc_values_wire_rotation', arcSystem["values"]["rotateWire"][0])
        SETTINGS.add('arc_values_wire_dropoff', arcSystem["values"]["dropoff"][0])

        # build curves and meshes and add them in the main arcSystem
        arcs = self.setupArcs(arcSystem)
        arcSystem["arcs"] = arcs
        
        # organize arc system and create attibutes on the main group
        self.organizeSystem(arcSystem)
        
        # write log
        self.writeLog(arcSystem)

    def writeLog(self, arcSystem):
        prefix = arcSystem["baseCurve"][0]
        filepath = TEMPPATH
        
        # convert arcSystem dict to str
        arcSystemStr = "raw dict: "+str(arcSystem)+"\n"
        for key in arcSystem.keys():
            arcSystemStr += "-"+str(key)+":\n"
            try:
                for value in arcSystem[key]:
                    arcSystemStr += "\t-"+str(value)+": "+str([str(value) for value in arcSystem[key][value]])+"\n"
            except:
                for value in arcSystem[key]:
                    arcSystemStr += "\t"+str(value)+"\n"
                    
        print arcSystemStr
        
        # write log
        currTime = time.strftime('%d%m%y_%H%M%S')
        file = filepath+'/'+prefix+'_arcSystem_'+currTime+'.log'

        FILE = open(file, "w")
        FILE.write(arcSystemStr)
        FILE.close
        
        print "---------"
        print "scite "+file+" &"        
        print "os.system('scite "+file+" &')"        
        print "---------"
        
    def setupArcs(self, arcSystem):
        
        baseCurve = arcSystem["baseCurve"]
        meshes = arcSystem["MeshNumber"][0]
        numRounds = arcSystem["values"]["numRounds"][0]
        radius = arcSystem["values"]["radius"][0]
        profileScale = arcSystem["values"]["profileScale"][0]
        translate = arcSystem["values"]["translate"]
        rotate = arcSystem["values"]["rotate"]
        scale = arcSystem["values"]["scale"]
        rotateWire = arcSystem["values"]["rotateWire"][0]
        dropoff = arcSystem["values"]["dropoff"][0]
        
        arcs = {}
        
        # create animated arcs
        for arc in range(meshes):
            
            # generate spiral curve around the base curve
            arcCurve, arcCurveGroup = self.createSpiralCurve(baseCurve[0], numRounds, abs(radius), profileScale)
            baseCurve = arcCurve
            
            # generate animated mesh attached to the spiral curve
            mesh, blendshape, wireMeshcurve, smooth = self.createArcAnimation(arcCurve, arcCurveGroup, translate, rotate, scale, rotateWire, dropoff)
            
            arcs[mesh] = [mesh, arcCurveGroup, blendshape[0], wireMeshcurve, smooth[0]]
            
            numRounds += random.randint(-1, 2)
            radius += random.uniform(-0.5, 1.5)
        
        return arcs
    
    def organizeSystem(self, arcSystem):
        
        smooth = arcSystem["values"]["smooth"][0]
        translate = arcSystem["values"]["translate"]
        rotate = arcSystem["values"]["rotate"]
        scale = arcSystem["values"]["scale"]
        rotateWire = arcSystem["values"]["rotateWire"][0]
        
        # create group of all the arc elements
        cmds.select(None, r = True)
        for mesh in arcSystem["arcs"]:
            cmds.select(arcSystem["arcs"][mesh][0], add = True)
            cmds.select(arcSystem["arcs"][mesh][1], add = True)
        
        arcSystemGroup = cmds.group(n = "arcSystem_GRP")
        arcExpression = "// arcs expression\n"
        
        # add global smooth attribute
        cmds.addAttr(arcSystemGroup, longName='globalSmooth', at="long", defaultValue=smooth, min=0, max=6)
        # add global translate attribute
        cmds.addAttr(arcSystemGroup, longName='globalSlide', defaultValue=translate[2], min=-40, max=40)
        # add global rotate attribute
        cmds.addAttr(arcSystemGroup, longName='globalRotate', attributeType = "double3" )
        cmds.addAttr(arcSystemGroup, longName='rX', attributeType="double", parent='globalRotate')
        cmds.addAttr(arcSystemGroup, longName='rY', attributeType="double", parent='globalRotate')
        cmds.addAttr(arcSystemGroup, longName='rZ', attributeType="double", parent='globalRotate')
        cmds.setAttr(arcSystemGroup+".globalRotate", rotate[0], rotate[1], rotate[2], type="double3")
        # add global scale attribute
        cmds.addAttr(arcSystemGroup, longName='globalScale', attributeType = "double3" )
        cmds.addAttr(arcSystemGroup, longName='sX', attributeType="double", parent='globalScale')
        cmds.addAttr(arcSystemGroup, longName='sY', attributeType="double", parent='globalScale')
        cmds.addAttr(arcSystemGroup, longName='sZ', attributeType="double", parent='globalScale')
        cmds.setAttr(arcSystemGroup+".globalScale", scale[0], scale[1], scale[2], type="double3")
        
        cmds.addAttr(arcSystemGroup, longName='globalRotateWire', defaultValue=rotateWire)
        
        for mesh in arcSystem["arcs"]:
            
            wireGroup = [wireGroup for wireGroup in cmds.listConnections(cmds.listRelatives(mesh)) if cmds.nodeType(wireGroup) == "groupId"][0]
            wireNode = [wireNode for wireNode in cmds.listConnections(wireGroup) if cmds.nodeType(wireNode) == "wire"][0]
            
            # add visibility attr
            cmds.addAttr(arcSystemGroup, longName=mesh+'Visibility', nn="Visibility", at="bool", defaultValue=True)
            # add attributes per mesh translateAttr
            cmds.addAttr(arcSystemGroup, longName=mesh+'Slide', defaultValue=translate[2], min=-40, max=40)
            # rotateAttr
            cmds.addAttr(arcSystemGroup, longName=mesh+'Rotate', attributeType="double3")
            cmds.addAttr(arcSystemGroup, longName=mesh+'rX', attributeType="double", parent=mesh+'Rotate')
            cmds.addAttr(arcSystemGroup, longName=mesh+'rY', attributeType="double", parent=mesh+'Rotate')
            cmds.addAttr(arcSystemGroup, longName=mesh+'rZ', attributeType="double", parent=mesh+'Rotate')
            
            # scaleAttr
            cmds.addAttr(arcSystemGroup, longName=mesh+'Scale', attributeType="double3")
            cmds.addAttr(arcSystemGroup, longName=mesh+'sX', attributeType="double", parent=mesh+'Scale')
            cmds.addAttr(arcSystemGroup, longName=mesh+'sY', attributeType="double", parent=mesh+'Scale')
            cmds.addAttr(arcSystemGroup, longName=mesh+'sZ', attributeType="double", parent=mesh+'Scale')
            
            # add expression  to link meshes to the arc group
            arcExpression += arcSystem['arcs'][mesh][4]+".divisions = "+arcSystemGroup+".globalSmooth;\n"
            arcExpression += wireNode+".rotation = "+arcSystemGroup+".globalRotateWire;\n"
            arcExpression += mesh+".translateZ = "+arcSystemGroup+".globalSlide + "+arcSystemGroup+"."+mesh+"Slide;\n"
            arcExpression += mesh+".rotateX = "+arcSystemGroup+".rX + "+arcSystemGroup+"."+mesh+"rX;\n"
            arcExpression += mesh+".rotateY = "+arcSystemGroup+".rY + "+arcSystemGroup+"."+mesh+"rY;\n"
            arcExpression += mesh+".rotateZ = "+arcSystemGroup+".rZ + "+arcSystemGroup+"."+mesh+"rZ;\n"
            arcExpression += mesh+".scaleX = "+arcSystemGroup+".sX + "+arcSystemGroup+"."+mesh+"sX;\n"
            arcExpression += mesh+".scaleY = "+arcSystemGroup+".sY + "+arcSystemGroup+"."+mesh+"sY;\n"
            arcExpression += mesh+".scaleZ = "+arcSystemGroup+".sZ + "+arcSystemGroup+"."+mesh+"sZ;\n"
            arcExpression += mesh+".visibility = "+arcSystemGroup+"."+mesh+"Visibility;\n"
            
        # set expression
        globalSlideExpr = cmds.expression(n = arcSystemGroup+"_expression", s = arcExpression)
        
        cmds.cycleCheck(e = False)
        
    def createSpiralCurve(self, baseCurve, numRounds, radius, profileScale):

        surfaceCV = float(numRounds+2)*(float(numRounds+2)/2.0)
        
        # duplicate curve and get the maxValue
        cmds.select(baseCurve, r=True)
        curveMaxValue = cmds.getAttr(baseCurve+".maxValue")
        cmds.rebuildCurve(ch=0, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=0, d=3)
        # create a circle profile
        profile = cmds.circle(nr=[0, 1, 0], c=[0, 0, 0], r=radius)
        # put it at the start of the baseCurve
        cmds.pathAnimation(profile, fm=True, f=True, fa="y", ua="x", wut=4, wu=[0, 1, 0], c=baseCurve)
        # extrude the profile
        extrudesurface = cmds.extrude(profile[0], baseCurve, et=2, sc=profileScale)
        # curve on surface
        curveonsurface = cmds.curveOnSurface(extrudesurface, append=False, uv=(0, 0))
        
        y = 0.0
        for i in range(int(surfaceCV)):
            y += curveMaxValue/surfaceCV
            x = math.fmod(y*2*surfaceCV/curveMaxValue, 8)
            #print x, y
            cmds.curveOnSurface(curveonsurface, append=True, uv=(x, y))
            
        # duplicate the created curve
        cmds.duplicateCurve(ch = False)
        cmds.rename("duplicated_"+baseCurve)
        spiralCurve = cmds.ls(sl = True)
        cmds.rebuildCurve(ch=0, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=0, d=3)
        # create wire
        #cmds.wire(spiralCurve, dds = [(0, 100)], gw = True, en = 1.0, ce = 0.0, li = 0.0, w = baseCurve)
        #cmds.pickWalk(d = "up")
        cmds.select(spiralCurve, r = True)
        arcCurveGroup = cmds.group(n = "spiralCurveWire"+baseCurve+"___GRP")
        
        #delete unused nodes
        cmds.delete(profile)
        cmds.delete(extrudesurface[0])    
        
        #print "spiral curve created."
    
        return spiralCurve, arcCurveGroup
        
    def createArcAnimation(self, baseCurve, arcCurveGroup, translate, rotate, scale, rotateWire, dropoff):
        
        mesh = cmds.polyPlane(n="arcSystem_"+baseCurve[0]+"_card", w=24, h=24, sx=4, sy=20)[0]
        cmds.delete(ch = True)
        
        # create new curve and hide it
        wireMeshCurve = cmds.curve(d=3, p=[(0, 0, -12), (0, 0, -6), (0, 0, 0), (0, 0, 6), (0, 0, 12)])
        cmds.setAttr(wireMeshCurve+".v", False)
        
        # rebuild curve
        cmds.rebuildCurve(wireMeshCurve, baseCurve, ch=1, rpo=1, rt=2, end=1, kr=0, kcp=0, kep=1, kt=0, s=26, d=3, tol = 0.01)
        cmds.select(mesh, r=True)
        # smooth the mesh
        smooth = cmds.polySmooth(dv=0)
        cmds.select(mesh, r=True)
        
        # create wire of the mesh on the new curve
        wire = cmds.wire(mesh, gw=True, en=1.0, ce=0.0, li=0.0, w=wireMeshCurve)
        cmds.pickWalk(d="up")
        wireGroup = cmds.ls(sl=True)
        # parent to the spiral curve
        cmds.parent(wireGroup, arcCurveGroup)
        # set wire values
        cmds.setAttr(wire[0]+".dropoffDistance[0]", dropoff)
        cmds.setAttr(wire[0]+".rotation", rotateWire)
        
        # create blendshape of the new curve on the base curve
        blendshape = cmds.blendShape(baseCurve, wireMeshCurve)
        cmds.setAttr(blendshape[0]+"."+baseCurve[0], 1)
        
        # tranform a bit the mesh
        cmds.setAttr(mesh+".tz", translate[0])
        cmds.setAttr(mesh+".rz", rotate[0])
        cmds.setAttr(mesh+".sz", scale[0])
        
        return mesh, blendshape, wireMeshCurve, smooth
    
def getSetCurve(mode='get'):
    
    selection = [node for node in cmds.ls(sl = True) if cmds.nodeType(cmds.listRelatives(node)[0]) == 'nurbsCurve']
    if selection:
        baseCurve = selection[0]
        print baseCurve
    else:
        cmds.warning("!select a curve!")
        baseCurve = "!select a curve!"
        
    if mode == 'set':
        try:
            cmds.textFieldButtonGrp("ArcCurveTxt", e=True, text=baseCurve)
        except:
            pass
    if mode == 'get':
        try:
            cmds.textFieldButtonGrp("ArcCurveTxt", e=True, text=baseCurve)
        except:
            pass
    return baseCurve

def arcSystemUI():
    baseCurve = getSetCurve('get')

    if cmds.window(WINDOWNAME, exists=True):
        cmds.deleteUI(WINDOWNAME, window=True)
    
    cmds.window(WINDOWNAME, w=415, h=365, title="Arc System", sizeable=False)
    cmds.formLayout("ArcMainForm")
    
    # arc general form
    cmds.formLayout("ArcObjectsForm")
    cmds.frameLayout("ArcObjectFrameLayout", l="General Values")
    cmds.textFieldButtonGrp("ArcCurveTxt", label="Base Curve ", text=baseCurve, buttonLabel="<<", buttonCommand=getSetCurve)
    cmds.intFieldGrp("ArcNumberMesh", numberOfFields=1, label="Number of Arcs ", value1=4)
    cmds.setParent("..")
    cmds.setParent("..")
    
    # arc values form
    # get default values
    arc_values_smooth = SETTINGS.get('arc_values_smooth')
    if arc_values_smooth == None:
        arc_values_smooth = 2

    arc_values_numRound = SETTINGS.get('arc_values_numRound')
    if arc_values_numRound == None:
        arc_values_numRound = 3

    arc_values_radius = SETTINGS.get('arc_values_radius')
    if arc_values_radius == None:
        arc_values_radius = 5.0

    arc_values_profil_scale = SETTINGS.get('arc_values_profil_scale')
    if arc_values_profil_scale == None:
        arc_values_profil_scale = 1.0

    arc_values_wire_rotation = SETTINGS.get('arc_values_wire_rotation')
    if arc_values_wire_rotation == None:
        arc_values_wire_rotation = 0.8

    arc_values_wire_rotation = SETTINGS.get('arc_values_wire_rotation')
    if arc_values_wire_rotation == None:
        arc_values_wire_rotation = 0.8

    arc_values_scale = SETTINGS.get('arc_values_scale')
    if arc_values_scale == None:
        arc_values_scale = [2.0, 1.0, 0.5]

    arc_values_rotate = SETTINGS.get('arc_values_rotate')
    if arc_values_rotate == None:
        arc_values_rotate = [0.0, 0.0, 90.0]

    cmds.formLayout("ArcValuesForm")
    cmds.frameLayout("ArcValuesFrameLayout", l="Arc Values")
    cmds.intFieldGrp("arc_values_smooth", numberOfFields=1, label="Arc Smooth", value1=arc_values_smooth)
    cmds.intFieldGrp("arc_values_numRound", numberOfFields=1, label="Number of Rounds", value1=arc_values_numRound)
    cmds.floatFieldGrp("arc_values_radius", numberOfFields=1, label="Radius", value1=arc_values_radius)
    cmds.floatFieldGrp("arc_values_profil_scale", numberOfFields=1, label="Profile Scale", value1=arc_values_profil_scale)
    cmds.floatFieldGrp("arc_values_wire_rotation", numberOfFields=1, label="Wire Rotate", value1=arc_values_wire_rotation)
    cmds.floatFieldGrp("arc_values_wire_dropoff", numberOfFields=1, label="Wire Dropoff", value1=1000000.0)
    cmds.floatFieldGrp("arc_values_rotate", numberOfFields=3, label="Arc Rotate", value1=arc_values_rotate[0],
                                                                                  value2=arc_values_rotate[1],
                                                                                  value3=arc_values_rotate[2])
    cmds.floatFieldGrp("arc_values_scale", numberOfFields=3, label="Arc Scale", value1=arc_values_scale[0],
                                                                                  value2=arc_values_scale[1],
                                                                                  value3=-arc_values_scale[2])
    
    cmds.button("ArcCreateArcSystem", l="create arc system", c=CreateArcs)
    
    cmds.setParent("..")

    # attach objects form and values form
    cmds.formLayout("ArcMainForm", e=True, attachForm=[
                                            ("ArcObjectsForm", "top", 10), 
                                            ("ArcObjectsForm", "left", 5), 
                                            ("ArcObjectsForm", "right", 5),
                                            ("ArcValuesForm", "left", 5), 
                                            ("ArcValuesForm", "right", 5), 
                                            ])
    cmds.formLayout("ArcMainForm", e=True, attachControl=[
                                            ("ArcValuesForm", "top", 8, "ArcObjectsForm"),
                                            ])

    cmds.showWindow(WINDOWNAME)

def main():
    # launch ui
    arcSystemUI()
        
if __name__ == "__main__":
    main()
    