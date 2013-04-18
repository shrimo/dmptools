import os
import sys
import time

import maya.cmds as cmds

import dmptools.mayaCommands as mayaCommands
from dmptools.settings import SettingsManager

SETTINGS = SettingsManager()

class Utils(object):
    """
        some utility methods for mayaToNuke tool
    """
    def __init__(self):
        # os infos
        self.os = os.name
        self.platform = sys.platform
        self.user = os.getenv('USERNAME')
        self.computer = os.getenv('COMPUTERNAME')
        self.tempPath = os.getenv('TEMP')
        self.nukePath = self.getNukeExe()
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
        SETTINGS.addSetting('os', self.os)
        SETTINGS.addSetting('platform', self.platform)
        
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
        framerange['current'] = int(cmds.currentTime(q = True))
        framerange['first'] = int(cmds.playbackOptions(q = True, min = True))
        framerange['last'] = int(cmds.playbackOptions(q = True, max = True))
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
        cmds.select(hi = True)
        selection = [str(item) for item in cmds.ls(sl = True)]

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
        panels = cmds.getPanel(allPanels = True)
        for panel in panels:
            try:
                self.panelsDisplay[panel] = {}
                for object in self.modelPanelObjects:
                    self.panelsDisplay[panel][object] = eval("cmds.modelEditor('"+panel+"', query = True, "+object+" = True)")
            except:
                pass
        
    def setDisplayOn(self):
        """
           show all the stuff in the viewport 
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = "+str(value)+")")
    
    def setDisplayOff(self):
        """
            hide all the stuff in the viewport
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = False)")

    def getNukeBin(self):
        # get nuke path on linux
        defaultNukePath = os.environ['NUKE_PATH']
        defaultNukePath = '/soft/nuke'

    def getNukeExe(self):
        # get nuke path on windows
        if self.os == 'nt':
            defaultNukePath = [
            'C:/Program Files/Nuke6.0v5/Nuke6.0.exe',
            'C:/Program Files/Nuke6.3v4/Nuke6.3.exe',
            'C:/Program Files (x86)/Nuke6.3v4/Nuke6.3.exe',
                                ]
            searchDir = 'C:\\Program Files\\'
            fileFilter = '*.exe'

        if self.os == 'posix':
            defaultNukePath = [
            '/software/nuke/6.3/bin/nuke6.0',
            '/software/nuke/7.0/bin/nukex',
                                ]
            searchDir = 'C:\\Program Files\\'
            fileFilter = '*'

        for path in defaultNukePath:
            if os.path.exists(path):
                SETTINGS.addSetting('nukePath', path)
        
        # get the nuke path setting if exists
        nukePath = SETTINGS.getSetting('nukePath')[0]
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
                    SETTINGS.addSetting('nukePath', nukePath)
                    return nukePath
                else:
                    raise UserWarning('No Nuke found !')
            else:
                raise UserWarning('No Nuke found !')

    def openScriptEditor(self):
        mayaCommands.openScriptEditor()