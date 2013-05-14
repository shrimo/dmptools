import os
import sys
import time

import maya.cmds as cmds

import dmptools.mayaCommands as mayaCommands
from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('mayaToNuke')

class Utils(object):
    """
        some utility methods for mayaToNuke tool
    """
    def __init__(self):
        # os infos
        self.os = os.name
        self.platform = sys.platform
        self.user = os.getenv('USERNAME')
        self.computer = os.getenv('HOST') if os.getenv('COMPUTERNAME') is None else "None"
        self.tempPath = self.getTempPath()
        self.nukePath = self.getNukePath()
        self.nonEditableFields = ['user', 'os', 'platform', 'computer']
        # maya display infos
        self.panelsDisplay = {}
        self.modelPanelObjects = [
                    'cameras', 'deformers',
                    'dimensions', 'dynamics',
                    'fluids', 'follicles',
                    'hairSystems', 'handles',
                    'hulls', 'ikHandles',
                    'joints', 'lights',
                    'locators', 'manipulators',
                    'nCloths', 'nParticles',
                    'nRigids', 'nurbsCurves',
                    'nurbsSurfaces', 'pivots',
                    'planes', 'polymeshes',
                    'strokes', 'subdivSurfaces',
                    ]
        # set settings
        SETTINGS.addSetting('user', self.user)
        SETTINGS.addSetting('computer', self.computer)
        SETTINGS.addSetting('os', self.os)
        SETTINGS.addSetting('platform', self.platform)

    def getTempPath(self):
        tempPath = os.getenv('TEMP')
        if not tempPath:
            tempPath = '/tmp'
        return tempPath

    def getTime(self):
        # get time
        timeInfo = {}
        timeInfo['current'] = time.strftime('%d%m%y_%H%M%S')
        timeInfo['str'] = str(time.strftime('%d/%m/%y at %H:%M:%S'))

        return timeInfo

    def getFramerange(self):
        """
            return the actual frame, first and last frame.
        """
        framerange = {}
        framerange['current'] = int(cmds.currentTime(q=True))
        framerange['first'] = int(cmds.playbackOptions(q=True, min=True))
        framerange['last'] = int(cmds.playbackOptions(q=True, max=True))
        framerange['frames'] = int((framerange['last'] - framerange['first']) + 1)

        return framerange

    def strFromList(self, inputlist=[]):
        """
            return two from a given list.
            [0] is a straight string line
            [1] is a string with break lines.
        """
        return ''.join(inputlist), '    - '+'\n    - '.join(inputlist)

    def filterSelection(self):
        """
            from a raw list of items, returns 1 dict containing:
            {[meshes], [cameras], [locators], [lights]}
        """
        # get current selection
        cmds.select(hi=True)
        selection = [str(item) for item in cmds.ls(sl=True)]

        # fill the items dict from the raw selection
        items = {}
        # meshes
        items['meshes'] = [cmds.listRelatives(node, p=True, fullPath=True)[0] \
                    for node in selection if cmds.nodeType(node) == "mesh"]
        # cameras
        items['cameras'] = [cmds.listRelatives(node, p=True, fullPath=True)[0] \
                    for node in selection if cmds.nodeType(node) == "camera"]
        # locators
        items['locators'] = [cmds.listRelatives(node, p=True, fullPath=True)[0] \
                    for node in selection if cmds.nodeType(node) == "locator"]
        # lights
        items['lights'] = [cmds.listRelatives(node, p=True, fullPath=True)[0] \
                    for node in selection if 'Light' in cmds.nodeType(node)]

        return items

    def getDisplayItems(self):
        """
            fill self.panelsDisplay with the all panels found
            and the state value of all the items in them.
        """
        panels = cmds.getPanel(allPanels=True)
        for panel in panels:
            try:
                self.panelsDisplay[panel] = {}
                for object in self.modelPanelObjects:
                    self.panelsDisplay[panel][object] = eval("cmds.modelEditor('"+panel+"', query=True, "+object+"=True)")
            except:
                pass
        
    def setDisplayOn(self):
        """
           show all the stuff in the viewport 
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit=True, "+object+"="+str(value)+")")
    
    def setDisplayOff(self):
        """
            hide all the stuff in the viewport
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit=True, "+object+"=False)")

    def openScriptEditor(self):
        mayaCommands.openScriptEditor()
    
    def getNukePath(self):
        nukePath = mayaCommands.nukePathFinder()
        SETTINGS.addSetting('nukePath', nukePath)

        return nukePath