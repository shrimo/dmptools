import maya.cmds as cmds
import maya.mel as mel
import random

# for getArea()
from pymel.core import PyNode

# for faceSeparate()
import dmptools.utils.mayaCommands as mayaCommands

# polyExtrude construction history
HISTORY = False

def extrudeLedge(face):
    """ extrude the first ledge on rooftop """
    localScaleRDM = random.uniform(0.88, 0.98)
    localScale = (localScaleRDM, localScaleRDM, 1)
    cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=0, localScale=localScale)

    return face

def extrudeSimple(face):
    """ extrude a simple rooftop """
    localScaleRDM = random.uniform(0.88, 0.98)
    localScale = (localScaleRDM, localScaleRDM, 1)
    thickness = random.randint(30,65)
    cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=localScale)

    return face

def extrudeDouble(face):
    """ extrude a double iteration rooftop """
    iterations = 2
    s = 0.0
    t = 0
    for iteration in range(iterations):
        localScaleRDM = random.uniform(0.88-s, 0.98-s)
        localScale = (localScaleRDM, localScaleRDM, 1)
        thickness = random.randint(30,65)-t
        cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=localScale)
        s += 0.2
        t += 10

    return face

def extrudeRounded(face):
    """ extrude a rounded rooftop """
    iterations = 4
    localScale = 0.92
    thickness = random.randint(25,35)
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=[localScale, localScale, localScale])
        localScale -= 0.04
        thickness -= 5

    return face

def extrudePinched(face):
    """ extrude a pinched rooftop if the face has exactly 4 edges """
    iterations = 1
    localScaleX = 1
    localScaleY = 0
    localScaleZ = 1
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=[localScaleX, localScaleY, localScaleZ])

    return face

def extrudeConcave(face):
    """ extrude a concave rooftop """
    iterations = 3
    localScale = 0.85
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=[localScale, localScale, localScale])
        localScale += 0.04
        thickness += 5

    return face

def extrudeHole(face):
    """ extrude a rounded and  """
    iterations = 5
    localScale = 0.9
    thickness = 25
    for iteration in range(iterations):
        cmds.polyExtrudeFacet(face, ch=HISTORY, keepFacesTogether=False, thickness=thickness, localScale=[localScale, localScale, localScale])
        thickness -= 10
    
    return face

def extrudeDoubleHole(face):
    """ execute the holeExtrude twice to produce a double rooftop """    
    firstface = holeExtrude(face)
    secondface = holeExtrude(firstface)

    return secondface

def getFaceArea(face):
    """ from a face, return the area and the bounding box in a dict """
    faceArea = {}
    faceArea['face'] = face
    faceArea['faceArea'] = PyNode(face).getArea()
    faceArea['faceBB'] = cmds.polyEvaluate(face, bc=True)
    
    return faceArea

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

def getSections(selection):
    """ from a selection return a dict with sections, blocks, and faces ready to extrude """
    # main dict
    sections = {}
    for section in selection:
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
            sections[section][block]['averageArea'] = float(sum(faceAreas))/float(len(faceAreas))
            faceAreas.sort()
            sections[section][block]['minArea'] = faceAreas[0]
            sections[section][block]['maxArea'] = faceAreas[-1]
            # compare thr actual face by the average and put them in the main dict
            sections[section][block]['big'] = []
            sections[section][block]['small'] = []
            for face in sections[section][block]['topfaces']:
                if getFaceArea(face)['faceArea'] >= sections[section][block]['averageArea']:
                    sections[section][block]['big'].append(face)
                else:
                    sections[section][block]['small'].append(face)

    return sections

def main():
    selection = cmds.ls(sl=True)
    if selection:
        # get section from selection
        sections = getSections(selection)
        # extrude rooftops
        for section in sections:
            for block in sections[section]:
                for face in sections[section][block]['topfaces']:
                    if face in sections[section][block]['small']:
                        ledge = extrudeLedge(face)
                        simple = extrudeDouble(ledge)
                    if face in sections[section][block]['big']:
                        ledge = extrudeLedge(face)
                        rounded = extrudeRounded(ledge)
        return sections

if __name__ == '__main__':
    main()
