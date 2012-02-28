import maya.cmds as cmds

import dmptools.presets as presets
import dmptools.mayaToNuke.exporter as exporter
import dmptools.mayaToNuke.utils as utils

WINDOW_NAME = 'exportMayaToNukeWindow'
UTILS = utils.Utils()

class MayaToNukeUI(object):
    def __init__(self):
        """ get all the necessary values """
        # stuff
        self.stuff = {}
        # get selection
        self.originalSel = cmds.ls(sl=True)
        # framerange info
        self.framerange = {}
        self.framerange['currentFrame'] = UTILS.getFramerange()[0]
        self.framerange['first'] = UTILS.getFramerange()[1]
        self.framerange['last'] = UTILS.getFramerange()[2]

    def buildUI(self):
        """ build the interface UI """
        # destroy the mayaToNuke windows if exists
        if cmds.window(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME, window=True)
        # create the main window
        self.win = cmds.window(WINDOW_NAME, title="Maya To Nuke Interface", mb=True, w=650, h=300)
        # build menu bar
        self.menuBar()
        # create the main master form
        mainform = cmds.formLayout("mainForm")
        # create the header of the interface
        self.header = cmds.text(label='header')
        # create the text field where to put the nuke output script
        txtOutput = cmds.text(label="nuke script:")
        self.textField = cmds.textField('fileInput')
        cmds.textField('fileInput', e=True, text='c:/tmp', annotation='This is the output file')
        # open filedialog button
        outputButton = cmds.button(label = " ... ", c=self.selectOutputFile)
        cmds.button(outputButton, e=True, annotation='Browse for a Nuke file - please type the .nk extension')
        # separators
        separator1 = cmds.separator()
        separatorTop = cmds.separator()
        separatorBottom = cmds.separator()
        # export, close and refresh buttons
        exportButton = cmds.button(label="Export", c=self.export)
        cmds.button(exportButton, e=True, annotation='Generate Nuke script from selected items')
        closeButton = cmds.button(label="Close", c=self.closeUI)
        cmds.button(closeButton, e=True, annotation='Close the mayaToNuke interface - Have a nice day -')
        reloadButton = cmds.iconTextButton(label="Refresh", st='iconOnly', i='refresh.png', c=self.refreshUI)
        cmds.iconTextButton(reloadButton, e=True, annotation='Refresh the UI with the current selection')
        # build options panel (create left and right panes)
        paneForm = self.doublePane()
        # attachForm
        cmds.formLayout(mainform,
                        edit = True,
                        attachForm = 
                        [
                            (reloadButton, "top", 5),
                            (reloadButton, "right", 5),
                            (self.header, "left", 5),
                            (self.header, "top", 5),
                            (txtOutput, "left", 5),
                            (outputButton, "right", 5),
                            (exportButton, "bottom", 5),
                            (exportButton, "left", 5),
                            (closeButton, "bottom", 5),
                            (closeButton, "right", 5),
                            (separator1, "left", 5),
                            (separator1, "right", 5),
                            (separatorTop, "left", 5),
                            (separatorTop, "right", 5),
                            (separatorBottom, "left", 5),
                            (separatorBottom, "right", 5),
                            (paneForm, "left", 5),
                            (paneForm, "right", 5)
                        ]
                    )
        # attachControl
        cmds.formLayout(mainform,
                        edit=True,
                        attachControl = 
                        [
                            (separator1, "top", 5, reloadButton),
                            (txtOutput, "top", 5, separator1),
                            (txtOutput, "top", 5, separator1),
                            (self.textField, "left", 5, txtOutput),
                            (self.textField, "right", 5, outputButton),
                            (outputButton, "top", 4, separator1),
                            (self.textField, "top", 5, separator1),
                            (separatorTop, "top", 5, self.textField),
                            (separatorBottom, "bottom", 5, exportButton),
                            (paneForm, "top", 4, separatorTop),
                            (paneForm, "bottom", 5, separatorBottom)
                        ])
        # attachPosition
        cmds.formLayout(mainform, edit=True,
                        attachPosition = 
                        [
                            (exportButton, "right", 5, 50),
                            (closeButton, "left", 5, 50)
                        ]
                    )
        cmds.showWindow(WINDOW_NAME)
        
    def doublePane(self):
        """build the double pane layout for the selection display"""
        # create the main form
        form = cmds.formLayout("optionsForm")
        # build bottom helpLine
        helpline = self.helpLine()
        cmds.setParent('..')
        # main frame layout
        frameL = cmds.frameLayout("optionsMainFrameL",
                                label = 'Items good for export:',
                                cll = False,
                                cl = False,
                                bv = True)
        # create double paneLayout and its default separation value
        paneLayout = cmds.paneLayout("doublePaneLayout",
                                    configuration='vertical2',
                                    paneSize=[[1,0,100],[2,100,100]])
        # build the left panelayout
        leftPanel = self.leftPane()
        # build the right panelayout
        rightPanel = self.rightPane()
        # set the panes on their good position
        cmds.paneLayout("doublePaneLayout", edit=True, setPane = [ leftPanel, 1])
        cmds.paneLayout("doublePaneLayout", edit=True, setPane = [ rightPanel, 2])
        # attatch the forms
        cmds.formLayout(form,
                        edit = True,
                        attachForm = 
                            [
                                (frameL, "left", 5),
                                (frameL, "right", 5),
                                (frameL, "top", 5),
                                (helpline, "left", 5),
                                (helpline, "right", 5),
                                (helpline, "bottom", 2)
                            ]
                        )
        cmds.formLayout(form,
                        edit = True,
                        attachControl = 
                            [
                                (frameL, "bottom", 5, helpline)
                            ]
                        )
        return form
    
    def leftPane(self):
        """obsolete pane but maybe useful"""
        # pass scroll layout on the left side of the pane layout
        passesL = cmds.formLayout("passForm")
        colLayout = cmds.columnLayout(adj = True)
        cmds.setParent('..')
        # fill with stuff
        passes = ['infos']
        passList = cmds.textScrollList(append = passes, sii = True, ams = True)
        cmds.setParent('..')
        # attach form
        cmds.formLayout(passesL, edit = True,   attachForm = [
                                            (passList, "left", 5),
                                            (passList, "right", 5),
                                            (passList, "top", 15),
                                            (passList, "bottom", 5)
                                            ])
        return passesL
    
    def rightPane(self):
        """main layout where the selection is displayed"""
        # framelayoutTitle
        form = cmds.formLayout("titleForm")
        selFrameL = cmds.scrollLayout("scrollRightPanel", hst = True, cr = True)
        colLayout = cmds.columnLayout("columnRightPanel", adj = True)
        # get items lists
        self.stuff['objects'] = UTILS.filterSelection()[0]
        self.stuff['cameras'] = UTILS.filterSelection()[1]
        self.stuff['locators'] = UTILS.filterSelection()[2]
        self.stuff['lights'] = UTILS.filterSelection()[3]
        # create objects framelayout
        self.objectsfrmLayout = cmds.frameLayout(label = str(len(self.stuff['objects']))+' objects:',
                                    cll = True,
                                    cl = True if not self.stuff['objects'] else False,
                                    bv = False,
                                    annotation = 'Valid objects to export')
        self.objectsTxt = self.editableFrameLayout(self.stuff['objects'])
        cmds.setParent('..')
        # create cameras framelayout
        self.camerasfrmLayout = cmds.frameLayout(label = str(len(self.stuff['cameras']))+' cameras:',
                                    cll = True,
                                    cl = True if not self.stuff['cameras'] else False,
                                    bv = False,
                                    annotation = 'Valid cameras to export')
        self.camerasTxt = self.editableFrameLayout(self.stuff['cameras'])
        cmds.setParent('..')
        # create locators framelayout
        self.locatorsfrmLayout = cmds.frameLayout(label = str(len(self.stuff['locators']))+' locators:',
                                    cll = True,
                                    cl = True if not self.stuff['locators'] else False,
                                    bv = False,
                                    annotation = 'Valid locators to export')
        self.locatorsTxt = self.editableFrameLayout(self.stuff['locators'])
        cmds.setParent('..')
        # create lights framelayout        
        self.lightsfrmLayout = cmds.frameLayout(label = str(len(self.stuff['lights']))+' lights:',
                                    cll = True,
                                    cl = True if not self.stuff['lights'] else False,
                                    bv = False,
                                    annotation = 'Valid lights to export')
        self.lightsTxt = self.editableFrameLayout(self.stuff['lights'])
        cmds.setParent('..')
        
        cmds.formLayout(form, edit = True, attachForm = [
                                            (selFrameL, "top", 15),
                                            (selFrameL, "left", 5),
                                            (selFrameL, "right", 5),
                                            (selFrameL, "bottom", 5)
                                            ])
        return form
    
    def editableFrameLayout(self, items):
        """name of the object"""
        form = cmds.formLayout("itemForm")
        txt = cmds.text(al = "left", label = UTILS.strFromList(items)[1])
        cmds.setParent('..')
        return txt

    def helpLine(self):
        """bottom interactive helpline"""
        # form that contains the framelayout
        form = cmds.formLayout("formHelpLine")
        # framelayout that contains the helpline
        frame = cmds.frameLayout(borderVisible = False, labelVisible = False, h = 20)
        # create helpline
        cmds.helpLine(h = 10)
        cmds.setParent('..')
        # attach the stuff
        cmds.formLayout(form, edit = True, attachForm = [
                                            (frame, 'left', 0),
                                            (frame, 'right', 0),
                                            (frame, 'top', 0),
                                            (frame, 'bottom', 0)
                                            ])
        return form

    def menuBar(self):
        """create the top menubar"""
        cmds.menu( label='File', allowOptionBoxes = False )
        # add items
        exitC = 'import maya.cmds as cmds;cmds.deleteUI('+WINDOW_NAME+', window = True)'
        cmds.menuItem(label = 'Exit', c = exitC)
        
        cmds.menu(label = 'Help', helpMenu = True)
        helpC = 'print HELP!'
        cmds.menuItem(label = 'Intranet Help', c = helpC)
        
        fun1C = 'import os;os.system("firefox http://www.google.com/images?q=mecha &")'
        cmds.menuItem(label = 'Bonus: Mechas !!', c = fun1C)
        
        fun2C = 'import os;os.system("firefox http://www.google.com/images?q=kittens &")'
        cmds.menuItem(label = 'Bonus: Kittens !!', c = fun2C)
        
        aboutC = 'import maya.cmds as cmds;cmds.confirmDialog(title = "about", message = "version v1.0", button = "OK")'
        cmds.menuItem(label = 'About', c = aboutC)

    def selectOutputFile(self, none=None):
        """opens a file dialog to point to the output path"""
        textfieldValue = cmds.textField(self.textField, text=True, q=True)
        if textfieldValue:
            directoryMask = os.path.dirname(textfieldValue+"/*.nk")
        else:
            directoryMask = "/*.nk"
            
        filedialog = cmds.fileDialog2(cap='Where to save the nuke script?',
                                    fm=0,
                                    ff='*.nk',
                                    dir=directoryMask,
                                    )
        if filedialog:
            outputpath = filedialog[0]
            cmds.textField(self.textField, e=True, text=outputFile)

    def textfieldValidator(self, inputText=''):
        """check if the input has an nk extension"""
        if inputText:
            outputFile = str(inputText)
            try:
                ext = outputFile.split('.')[-1]
            except:
                ext = ''
                pass
            if ext == 'nk':
                return outputFile
            else:
                return None
        else:
            print 'nothing found'
            return None

    def refreshUI(self):
        """method to refresh the interface from a new selection"""
        # get the new selection
        self.originalSel = cmds.ls(sl=True)
        self.stuff['objects'] = UTILS.filterSelection()[0]
        self.stuff['cameras'] = UTILS.filterSelection()[1]
        self.stuff['locators'] = UTILS.filterSelection()[2]
        self.stuff['lights'] = UTILS.filterSelection()[3]
        # refresh objects ui
        cmds.text(self.objectsTxt, e=True, label = UTILS.strFromList(self.stuff['objects'])[1])
        cmds.frameLayout(self.objectsfrmLayout,
                            e=True,
                            label = str(len(self.stuff['objects']))+' objects:',
                            cll = True,
                            cl = True if not self.stuff['objects'] else False,
                            bv = False,
                            annotation = 'Valid objects to export')
        # refresh cameras ui
        cmds.text(self.camerasTxt, e=True, label = UTILS.strFromList(self.stuff['cameras'])[1])
        cmds.frameLayout(self.camerasfrmLayout,
                            e=True,
                            label = str(len(self.stuff['cameras']))+' cameras:',
                            cll = True,
                            cl = True if not self.stuff['cameras'] else False,
                            bv = False,
                            annotation = 'Valid cameras to export')
        # refresh locators ui
        cmds.text(self.locatorsTxt, e=True, label = UTILS.strFromList(self.stuff['locators'])[1])
        cmds.frameLayout(self.locatorsfrmLayout,
                            e=True,
                            label = str(len(self.stuff['locators']))+' locators:',
                            cll = True,
                            cl = True if not self.stuff['locators'] else False,
                            bv = False,
                            annotation = 'Valid locators to export')
        # refresh lights ui
        cmds.text(self.lightsTxt, e=True, label = UTILS.strFromList(self.stuff['lights'])[1])
        cmds.frameLayout(self.lightsfrmLayout,
                            e=True,
                            label = str(len(self.stuff['lights']))+' lights:',
                            cll = True,
                            cl = True if not self.stuff['lights'] else False,
                            bv = False,
                            annotation = 'Valid lights to export')

    def closeUI(self, none=None):
        """delete the main window"""
        cmds.deleteUI(WINDOW_NAME, window = True)

    def export(self, selection):
        """start the export procedure"""
        if self.stuff:
            # get display values
            UTILS.getDisplayItems()
            #set display off
            UTILS.setDisplayOff()
            # get the output path from the textfield
            outputFile = self.textfieldValidator(cmds.textField(self.textField, text=True, q=True))
            if outputFile:
                # generate the nuke script
                EXPORTER = exporter.Exporter(self.stuff, outputFile, self.framerange)
                EXPORTER.startExport()
            else:
                cmds.confirmDialog(t = 'Error', m = 'The output file is not correct.\nex: /<path>/nukefile.nk')
            #set display back on
            UTILS.setDisplayOn()
            # set playback at the original frame
            cmds.currentTime(self.framerange['currentFrame'])
            #select original selection
            cmds.select(self.originalSel, r = True)
        else:
            cmds.confirmDialog(t = 'Error', m = 'There is nothing to export!')
