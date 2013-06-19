"""
    BAKE UDIM TILES

    ====================================================================================================================
    Description: Bake out multiple tiles using Batch Bake (Mental Ray).

    ====================================================================================================================
    Usage: Two methods. First is quick and simple but temporary. Second installs
           the script so you can use it regularly.

    ====================================================================================================================      
    Arguments: The command by default tries to figure out what camera to use as well as what
              shading group and bake set the selected object/s are connected to.
              The following arguments can be used to override the defaults:

                  camera = <name of camera transform> ie... persp, top, front, side, renderCam
                  shadingGroup = <name of shading group> ie... initialShadingGroup, lambert2ShadingGroup
                  bakeSet = <name of textureBakeSet> ie... initialTextureBakeSet, occlusionBakeSet

              For example...
                  
                  bakeTiles(camera='renderCam', shadingGroup='myShadingGroup', bakeSet='occlusionBakeSet')
"""     

from pymel.core import *
import math as m
import maya.mel as mel
import pymel.core.runtime as pyrt

def removeDuplicates(seq):
    # Not order preserving    
    myset = set(seq)
    return list(myset)

def processLightMaps(tiles, camera, bakeSet, bakeGroup, bakeObject):
    myBakeSet = ls(bakeSet, type='textureBakeSet')
    myBakeSet[0].uvRange.set(2)
    for i in tiles:
        rawid = i-1001
        tu = int (rawid % 10)
        tv = int (m.floor(rawid/10))
        myBakeSet[0].prefix.set('baked_%s' % str(i))
        myBakeSet[0].uMin.set(tu)
        myBakeSet[0].uMax.set(tu+1)
        myBakeSet[0].vMin.set(tv)
        myBakeSet[0].vMax.set(tv+1)
        mel.eval('convertLightmap -camera %s -bo %s %s %s' % (camera, bakeSet, bakeGroup, bakeObject))

def getTiles(bakeObject):
    udims = []
    select (bakeObject)
    sizeUVs = polyEvaluate (uv=True)
    pyrt.ConvertSelectionToUVs()
    getUVs = ls(sl=True, fl=True)
    removeUVs = getUVs
    
    while (sizeUVs > 0):
        select(removeUVs[0])
        pyrt.SelectUVShell()
        shellUVs = ls(sl=True, fl=True)
        UVs = polyEvaluate (bc2=True)
        SS = m.floor(UVs[0][0])
        TT = m.floor(UVs[1][0])
        TT = m.fabs(TT)
        udim = int(TT * 10 + SS + 1001)
        udims.append(udim)
        removeUVs = list(set(removeUVs) - set(shellUVs))
        sizeUVs = len(removeUVs)
    return removeDuplicates (udims)

def checkBakeSet(bakeSet):
    status = True
    if objExists(bakeSet) == False:
        print("Warning: no bakeset exists with that name!")
        status = False
    return status

def getBakeConnection(myObj):
    status = False
    lsShape = myObj.getShape()
    lsConnections = lsShape.outputs()
    for i in lsConnections:
        if i.type() == 'textureBakeSet':
            status = i.name()
    if status == False:
        print 'not connected to bake set'
    return status

def getSGConnection(myObj):
    status = False
    lsShape = myObj.getShape()
    lsConnections = lsShape.outputs()
    for i in lsConnections:
        if i.type() == 'shadingEngine':
            status = i.name()
    if status == False:
        print 'not connected to shading group'
    return status

def bakeTiles(camera='persp', shadingGroup=False, bakeSet=False):
    selectedObjects = ls(sl=True, fl=True)
    for myObj in selectedObjects:
        if bakeSet == False:
            bakeSet = getBakeConnection(myObj)
        if shadingGroup == False:
            shadingGroup = getSGConnection(myObj)
        if bakeSet != False or shadingGroup != False or checkBakeSet(bakeSet) != False:
            tiles = getTiles(myObj)
            processLightMaps(tiles, camera, bakeSet, shadingGroup, myObj)
    select (selectedObjects)

def main():
    bakeTiles('persp', False, False)

if __name__ == '__main__':
    main()