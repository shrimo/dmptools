import maya.cmds as cmds
import maya.mel as mel

WINDOWNAME = 'sym_window'

class Symmetry(object):
    def __init__(self):
        pass
        
    def mirrorGeo(self, axis):
        
        selection = cmds.ls(sl=True)
        selectionPointList = cmds.polyListComponentConversion(selection, tv=True)
        points = cmds.ls(selectionPointList, fl=True)

        xformP = cmds.xform(points[0], q=True, ws=True, t=True)

        minX = xformP[0]
        midX = xformP[0]
        maxX = xformP[0]

        minY = xformP[1]
        midY = xformP[1]
        maxY = xformP[1]
        
        minZ = xformP[2]
        midZ = xformP[2]
        maxZ = xformP[2]

        for p in points:
            pPos = cmds.xform(p, q=True, ws=True, t=True)

            if pPos[0] > maxX : maxX = pPos[0]
            if pPos[1] > maxY : maxY = pPos[1]
            if pPos[2] > maxZ : maxZ = pPos[2]
            
            if pPos[0] < minX : maxX = pPos[0]
            if pPos[1] < minY : minY = pPos[1]
            if pPos[2] < minZ : minZ = pPos[2]
            
            midX = ((midX+pPos[0])/2)
            midY = ((midY+pPos[1])/2)
            midZ = ((midZ+pPos[2])/2)
            
        if axis == '+X':
            flipPivots = maxX, midY, midZ
            scaleAxis = 'X'
        if axis == '+Y':
            flipPivots = midX, maxY, midZ
            scaleAxis = 'Y'
        if axis == '+Z':
            flipPivots = midX, midY, maxZ
            scaleAxis = 'Z'
        if axis == '-X':
            flipPivots = minX, midY, midZ
            scaleAxis = 'X'
        if axis == '-Y':
            flipPivots = midX, minY, midZ
            scaleAxis = 'Y'
        if axis == '-Z':
            flipPivots = midX, midY, minZ
            scaleAxis = 'Z'

        newSelection = []
        
        for item in selection:
            cmds.select(item)
            pivot = cmds.xform(item, q=True, ws=True, sp=True)
            print item, axis, scaleAxis, pivot, flipPivots
            # duplicate mesh
            dupItem = cmds.duplicate(rr=True, rc=True)[0]
            dupItemShape = cmds.listRelatives(dupItem)[0]
            cmds.makeIdentity(dupItem, apply=True, t=True, r=True, s=True, n=False)
            # set pivots
            cmds.xform(dupItem, ws=True, sp=flipPivots)
            # mirror
            cmds.setAttr(dupItem+'.scale'+scaleAxis, -1)
            cmds.polyNormal(dupItem, normalMode=0, ch=True)
            # set opposite
            cmds.setAttr(dupItemShape+'.opposite', not cmds.getAttr(dupItemShape+'.opposite'))
            # reapply pivots
            cmds.xform(item, ws=True, sp=pivot)
            cmds.xform(dupItem, ws=True, sp=pivot)
            # delete history center pivot
            cmds.makeIdentity(dupItem, apply=True, t=True, r=True, s=True, n=False)
            cmds.delete(dupItem, ch=True)
            cmds.select(dupItem)
            
            newSelection.append(dupItem)
            
        cmds.select(newSelection)
        
    def UI(self):
        if cmds.window(WINDOWNAME, exists=True):
            cmds.deleteUI(WINDOWNAME, window=True)

        window = cmds.window(WINDOWNAME, t='Mirror Geo: select Axis')
        cmds.columnLayout(adjustableColumn=True)
        bright, dark = 0.4, 0.3
        cmds.iconTextButton(style='textOnly',
                            label='+X',
                            h=40,
                            bgc=(bright, bright, bright),
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('+X'))
        cmds.iconTextButton(style='textOnly',
                            label='-X',
                            h=40,
                            bgc=(dark, dark, dark),      
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('-X'))
        cmds.iconTextButton(style='textOnly',
                            label='+Y',
                            h=40,
                            bgc=(bright, bright, bright),
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('+Y'))
        cmds.iconTextButton(style='textOnly',
                            label='-Y',
                            h=40,
                            bgc=(dark, dark, dark),      
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('-Y'))
        cmds.iconTextButton(style='textOnly',
                            label='+Z',
                            h=40,
                            bgc=(bright, bright, bright),
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('+Z'))
        cmds.iconTextButton(style='textOnly',
                            label='-Z',
                            h=40,
                            bgc=(dark, dark, dark),      
                            font='boldLabelFont',
                            command=lambda *args: Symmetry().mirrorGeo('-Z'))
        cmds.showWindow()
        
def main():
    symmetry = Symmetry()
    symmetry.UI()
    
if __name__ == '__main__':
    main()