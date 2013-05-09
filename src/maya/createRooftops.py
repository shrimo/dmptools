import maya.cmds as cmds
import maya.mel as mel
import random

import dmptools.mayaCommands as mayaCommands

# polyExtrude construction history
HISTORY = False

def getFaceArea(face):
    """ from a face, return the area and the bounding box in a dict """
    faceArea = {}
    faceArea['face'] = face
    faceArea['faceArea'] = cmds.polyEvaluate(face, area=True)
    faceArea['faceBB'] = cmds.polyEvaluate(face, bc=True)
    
    return faceArea

def extrudeLedge(face):
    """ extrude the first ledge on rooftop """
    localScaleRDM = random.uniform(0.88, 0.98)
    localScale = (localScaleRDM, localScaleRDM, 1)
    cmds.polyExtrudeFacet(ch=HISTORY, keepFacesTogether=False, thickness=0, localScale=firstLocalScale)

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
    iterations = 1
    localScaleX = 1
    localScaleY = 0
    localScaleZ = 1
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, thickness=thickness, localScale=[localScaleX, localScaleY, localScaleZ])

    return face

def concaveExtrude(face):
    """ extrude a concave rooftop """
    iterations = 3
    localScale = 0.85
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, thickness=thickness, localScale=[localScale, localScale, localScale])
        localScale += 0.04
        thickness += 5

    return face

def holeExtrude(face):
    """ extrude a rounded and  """
    iterations = 5
    localScale = 0.9
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, thickness=thickness, localScale=[localScale, localScale, localScale])
        thickness -= 10
    
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
        separate = True
        while separate:
            try:
                cmds.select(selection+'.f[1]')
                mel.eval('polyConvertToShell;')
                # separate the selection from the mesh
                separation = mayaCommands.faceSeparate()
                shells.append(separation)
            except:
                shells.append(selection)
                separate = False
        if not shells:
            shells = [selection]
    except:
        pass

    return shells
"""
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
"""

def getTopFaces(mesh):
    """ extrude top faces of given meshes """    

    # rooftop faces
    topfaces = []
    cmds.select(mesh, r=True)
    meshFaces = cmds.ls(mesh+".f[*]")
    faces = cmds.ls(meshFaces, fl=True)
    
    # if the face normal is facing the sky, then fill the rooftop faces dict
    for face in faces:
        if float(cmds.polyInfo(face, fn=True)[0].split(' ')[-2]) >= 1.0:
            topfaces.append(face)

    return topfaces

def main():
    selection = cmds.ls(sl=True)
    # main dict
    sections = {}
    for section in selection:
        # create group of section
        # grouptmp = cmds.group(section)
        # cmds.rename(grouptmp, section)
        # try to separate groups of shells from a selection
        sections[section] = {}
        blocks = separateShells(section)
        # go through all the shells and get the rooftop faces
        for block in blocks:
            # get top faces
            sections[section][block] = {}
            sections[section][block]['topfaces'] = getTopFaces(block)
            # faces utils
            faceAreas = []
            # get the face area and put it in the main dict
            [faceAreas.append(getFaceArea(face)['faceArea']) for face in sections[section][block]['topfaces']]
            # get the average area
            faceAreasAverage = float(sum(faceAreas))/float(len(faceAreas))
            # print "average area for", block, "is", faceAreasAverage
            for face in sections[section][block]['topfaces']:
                # compare thr actual face by the average and put them in the main dict
                sections[section][block]['big'] = []
                sections[section][block]['small'] = []
                if getFaceArea(face)['faceArea'] >= faceAreasAverage:
                    sections[section][block]['big'].append(face)
                if getFaceArea(face)['faceArea'] <= faceAreasAverage:
                    sections[section][block]['small'].append(face)

    return sections

if __name__ == '__main__':
    main()

"""
for section in sections:
    print section
    for block in sections[section]:
        print block, sections[section][block]['topfaces']

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

for block in rooftops:
    for faces in rooftops[block]:
        cmds.select(rooftops[block][faces], add=True)

"""