import maya.cmds as cmds
import maya.mel as mel
import random

import dmptools.mayaCommands as mayaCommands

# polyExtrude construction history
HISTORY = False

def getFaceArea(face):
    faceArea = {}
    faceArea['face'] = face
    faceArea['facearea'] = cmds.polyEvaluate(face, area=True)
    faceArea['faceBB'] = cmds.polyEvaluate(face, bc=True)
    
    return faceArea

def roundedExtrude(face):
    """ extrude a rounded rooftop """
    iterations = 4
    localScale = 0.92
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, thickness=thickness, localScale=[localScale, localScale, localScale])
        localScale -= 0.04
        thickness -= 5

    return face

def pinchedExtrude(face):
    """ extrude a pinched rooftop if the face has exactly 4 edges """

    return face

def concaveExtrude(face):
    """ extrude a concave rooftop """

    return face

def convexExtrude(face):
    """ extrude a convex rooftop """

    return face

def holeExtrude(face):
    """ extrude a rounded and  """
    iterations = 5
    localScale = 0.85
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, thickness=thickness, localScale=[localScale, localScale, localScale])
        thickness -= 15
    
    return face

def doubleHoleExtrude(face):
    """ execute the holeExtrude twice to produce a double rooftop """    

    firstface = holeExtrude(face)
    secondface = holeExtrude(firstface)

    return secondface

def separateShells(selection):
    """ try to separate shells of a geo from a selection """

    shells = []
    try:
        sep = True
        while sep:
            try:
                cmds.select(selection+'.f[1]')
                mel.eval('polyConvertToShell;')
                # separate the selection from the mesh
                separation = mayaCommands.faceSeparate()
                shells.append(separation)
            except:
                sep = False
        if shells:
            cmds.delete(selection)
        else:
            shells = [selection]
    except:
        pass

    return shells

def extrudeRooftops_old(face):
    firstThickness = 0
    secondThickness = random.randint(30,65)
    thirdThickness = random.randint(20,55)
    firstRdm = random.uniform(0.88, 0.98)
    secondRdm = random.uniform(0.92, 0.95)
    thirdRdm = random.uniform(0.92, 0.95)
    while thirdRdm >= secondRdm:
        thirdRdm -= random.uniform(0.94, 0.99)

    firstLocalScale = (firstRdm, firstRdm, 1)
    secondLocalScale = (secondRdm, secondRdm, 1)
    thirdLocalScale = (secondRdm, secondRdm, 1)

    cmds.select(face, replace=True)            
    # first extrusion: offset only
    cmds.polyExtrudeFacet(ch=HISTORY, keepFacesTogether=False, thickness=0, localScale=firstLocalScale)
    # second extrusion
    cmds.polyExtrudeFacet(ch=HISTORY, keepFacesTogether=False, thickness=secondThickness, localScale=secondLocalScale)
    cmds.polyExtrudeFacet(ch=HISTORY, keepFacesTogether=False, thickness=thirdThickness, localScale=thirdLocalScale)

    return face

def getTopFaces(meshes):
    """ extrude top faces of given meshes """    

    blocks = {}
    for mesh in meshes:
        # rooftop faces dict
        blocks[mesh] = []
        cmds.select(mesh, r=True)
        meshFaces = cmds.ls(mesh+".f[*]")
        faces = cmds.ls(meshFaces, fl=True)
        
        # if the face normal is facing the sky, then fill the rooftop faces dict
        for face in faces:
            if float(cmds.polyInfo(face, fn=True)[0].split(' ')[-2]) >= 1.0:
                blocks[mesh].append(face)

    return blocks

def main():
    selection = cmds.ls(sl=True)
    for node in selection:
        # try to separate groups of shells from a selection
        shells = separateShells(node)
        # go through all the shells and get the rooftop faces
        rooftops = getTopFaces(shells)

        # go through all the shells and their rooftop faces
        for mesh in rooftops:
            for face in rooftops[mesh]:
                print face

    return rooftops

if __name__ == '__main__':
    main()

"""
faceArea = getFaceArea(face)

area = faceArea['facearea']
faceBBXMin = faceArea['faceBB'][0][1]
faceBBXMax = faceArea['faceBB'][0][0]
faceBBYMin = faceArea['faceBB'][1][0]
faceBBYMax = faceArea['faceBB'][1][1]
faceBBZMin = faceArea['faceBB'][2][0]
faceBBZMax = faceArea['faceBB'][2][1]

print "area:", area
print "bbox:", faceBBXMin, faceBBXMax, faceBBYMin, faceBBYMax, faceBBZMin, faceBBZMax
"""

