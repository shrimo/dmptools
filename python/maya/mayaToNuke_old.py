#========================================================
#
# Generates a Nuke .nk file from Maya (animated) objects cameras and locators 
# michael-ha@moving-picture.com
#
# __name__ = 'dmptools.mayaToNuke'
#
#=========================================================

import maya.cmds as cmds
import os
import time
import commands as cmd

MAYA_PATH = '!MAYA_PATH!'
MAYA_SHARE = '!MAYA_SHARE!'

class Infos:
    def __init__(self):

        if os.name == 'nt':
            self.infofile = MAYA_PATH+'/mayaToNuke.preset'
        else:
            self.infofile = '/tmp/mayaToNuke.preset'            

    def setPresets(self, dic):

        print 'setting preset...'
        FILE = open(self.infofile, 'w')
        FILE.write(str(dic))
        FILE.close()

    def getPresets(self):
        
        print 'gathering preset...'
        FILE = open(self.infofile, 'r')
        line = FILE.readline()
        dic = eval(line)
        FILE.close()

        return dic

    def getHubData(self, camera):
        try:
            exrData = str(cmds.getAttr(camera+".exrData"))
            hubVersion = exrData.split('v')[-1]
            hubStart = int(cmds.getAttr(camera+".hubStartFrameRange"))
            hubEnd = int(cmds.getAttr(camera+".hubEndFrameRange"))
            hubData = True
        except:
            hubVersion= None
            hubStart = None
            hubEnd= None
            hubData = False
            
        return hubData, hubVersion, hubStart, hubEnd  
        
class OptionPanel:	
    def __init__(self):
        
        self.originalSel = cmds.ls(sl = True)
        cmds.select(hi = True)
        self.sel = [str(item) for item in cmds.ls(sl = True)]
        
    def doublePaneLayout(self):
            
        form = cmds.formLayout("optionsForm")

        # build helpLine
        helpline = self.helpLine()
        cmds.setParent('..')
        
        # main frame layout
        frameL = cmds.frameLayout("optionsMainFrameL", label = '-Stuff that are going to be exported:', cll = False, cl = False, bv = True)
        
        # create double paneLayout
        paneLayout = cmds.paneLayout("doublePaneLayout", configuration='vertical2', paneSize=[[1,0,100],[2,100,100]])
        
        leftPanel = self.passesLayout() # left
        rightPanel = self.selFrameLayout() # right

        cmds.paneLayout("doublePaneLayout", edit=True, setPane = [ leftPanel, 1])
        cmds.paneLayout("doublePaneLayout", edit=True, setPane = [ rightPanel, 2])
                
        cmds.formLayout(form, edit = True, attachForm = [
                                            (frameL, "left", 5),
                                            (frameL, "right", 5),
                                            (frameL, "top", 5),
                                            (helpline, "left", 5),
                                            (helpline, "right", 5),
                                            (helpline, "bottom", 2)
                                            ])
        
        cmds.formLayout(form, edit = True, attachControl = [
                                            (frameL, "bottom", 5, helpline)
                                            ])
        
        return form
    
    def passesLayout(self):
        
        # pass scroll layout on the left side of the pane layout
        
        passesL = cmds.formLayout("passForm")
        colLayout = cmds.columnLayout(adj = True)
        cmds.setParent('..')
        
        # tkl = TicklePass()
        # passes = tkl.getAllPass()
        passes = ['']
        passList = cmds.textScrollList(append = passes, sii = True, ams = True)
        cmds.setParent('..')

        cmds.formLayout(passesL, edit = True,	attachForm = [
                                            (passList, "left", 5),
                                            (passList, "right", 5),
                                            (passList, "top", 15),
                                            (passList, "bottom", 5)
                                            ])
        
        return passesL
    
    def selFrameLayout(self):
        
        #frame layouts on the right side of the pane layout
        
        # framelayoutTitle
        form = self.frameTitle()

        selFrameL = cmds.scrollLayout("scrollRightPanel", hst = True, cr = True)
        colLayout = cmds.columnLayout("columnRightPanel", adj = True)
        
        # get items lists
        objects, cameras, locators, lights = ExportMayaToNuke().filterSelection(self.sel)

        frmLayout = cmds.frameLayout(label = str(len(objects))+' objects:', cll = True, cl = True if not objects else False, bv = False, annotation = 'Valid objects to export')
        self.editableFrameLayout(objects)
        cmds.setParent('..')
        
        frmLayout = cmds.frameLayout(label = str(len(cameras))+' cameras:', cll = True, cl = True if not cameras else False, bv = False, annotation = 'Valid cameras to export')
        self.editableFrameLayout(cameras)
        cmds.setParent('..')
        
        frmLayout = cmds.frameLayout(label = str(len(locators))+' locators:', cll = True, cl = True if not locators else False, bv = False, annotation = 'Valid locators to export')
        self.editableFrameLayout(locators)
        cmds.setParent('..')
        
        frmLayout = cmds.frameLayout(label = str(len(lights))+' lights:', cll = True, cl = True if not lights else False, bv = False, annotation = 'Valid lights to export')
        self.editableFrameLayout(lights)
        cmds.setParent('..')
        
        cmds.formLayout(form, edit = True, attachForm = [
                                            (selFrameL, "top", 15),
                                            (selFrameL, "left", 5),
                                            (selFrameL, "right", 5),
                                            (selFrameL, "bottom", 5)
                                            ])
        
        return form
    
    def frameTitle(self):
        
        form = cmds.formLayout("titleForm")
        
        frm0 = cmds.frameLayout(labelVisible = False, borderStyle = "out", w = 24, h =  16)
        cmds.setParent('..')
        
        frameName = cmds.frameLayout(labelVisible = False, borderStyle = "out", h = 16)
        cmds.text(align = "left", label = " Item Name ", font = "smallPlainLabelFont")
        cmds.setParent('..')
        
        frameAnim = cmds.frameLayout(labelVisible = False, borderStyle = "out", w = 24, h = 16)
        cmds.text(align = "right", label = " Anim ", font = "smallPlainLabelFont")
        cmds.setParent('..')
        
        cmds.formLayout(form, edit = True, attachForm = [
                                            (frm0, "left", 1),
                                            (frameAnim, "right", 32)
                                            ],
                                    attachControl = [
                                            (frameName, "left", 1, frm0),
                                            (frameAnim, "left", 1, frameName),
                                            ],		
                                    attachPosition = [
                                            (frameName, "right", 5, 90),
                                            (frameAnim, "left", 5, 10)
                                            ])
        
        return form

    
    def editableFrameLayout(self, items):
        
        form = cmds.formLayout("itemForm")
        txt = cmds.text(al = "left", label = ExportMayaToNukeUI().strFromList(items)[1])
        cmds.setParent('..')
        
        '''
        col = cmds.columnLayout(adj = True)
        
        for item in items:
            txt = cmds.text(al = "left", label = item)
            check = cmds.checkBox(label = ' ', value = False)
        cmds.formLayout(form, edit = True, attachForm = [
                                            (col, "right", 5),
                                            (col, "left", 5)
                                            ])
        
        '''
        return form
    
    def helpLine(self):
        
        form = cmds.formLayout("formHelpLine")
        frame = cmds.frameLayout(borderVisible = False, labelVisible = False, h = 20)
        cmds.helpLine(h = 10)
        cmds.setParent('..')
        
        cmds.formLayout(form, edit = True, attachForm = [
                                            (frame, 'left', 0),
                                            (frame, 'right', 0),
                                            (frame, 'top', 0),
                                            (frame, 'bottom', 0)
                                            ])
        
        return form
    
class ExportMayaToNuke:
    def __init__(self, filePath=None):
        
        # get selection
        self.originalSel = cmds.ls(sl = True)
        cmds.select(hi = True)
        self.sel = [str(item) for item in cmds.ls(sl = True)]
        
        self.path = filePath
        self.sysOs = os.name
        
        # get playback time
        self.currentFrame = int(cmds.currentTime(q = True))
        self.firstFrame = int(cmds.playbackOptions(q = True, min = True))
        self.lastFrame = int(cmds.playbackOptions(q = True, max = True))
        self.frames = int((self.lastFrame - self.firstFrame) + 1)
        
        # get time
        self.currTime = time.strftime('%d%m%y_%H%M%S')
        self.timeStr = str(time.strftime('%d/%m/%y at %H:%M:%S'))
        
        # display data
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

    def startExport(self):
        # get the file extension
        try:
            ext = self.path.split('.')[-1]
        except:
            ext = ''
            pass
        if ext == 'nk':
            if os.name == 'nt':
                pyFile = "c:/tmp/"+self.path.split('/')[-1].split('.')[-2]+"_"+self.currTime+".py"
            else:
                pyFile = "/tmp/"+self.path.split('/')[-1].split('.')[-2]+"_"+self.currTime+".py"
                        
            # get display values
            self.getDisplay()
            
            #set display off
            self.setDisplayOff()
            
            # writing header of the python file
            self.filePy = open(pyFile, "a")
            
            self.filePy.write("# this python file is generated automatically by the 'mayaToNuke.py' tool.\n")
            self.filePy.write("# it will be processed by mayapy and will create a .nk file.\n\n")
            self.filePy.write("# name of the python file: "+pyFile+"\n")
            self.filePy.write("# name of the maya file: "+self.path+"\n")
            self.filePy.write("# generated the : "+self.timeStr+"\n\n")
            self.filePy.write('import nuke\n\n')
            self.filePy.write('nuke.root().knob("first_frame").setValue('+str(self.firstFrame)+')\n')
            self.filePy.write('nuke.root().knob("last_frame").setValue('+str(self.lastFrame)+')\n\n')
            
            # generate and write data from selection
            objects, cameras, locators, lights = self.filterSelection(self.sel)
            
            if objects:
                print "-exporting "+str(len(objects))+" objects:"
                self.writeObjectsToPyFile(objects, self.filePy)
            
            if cameras:
                print "-exporting "+str(len(cameras))+" cameras:"
                self.writeCamerasToPyFile(cameras, self.filePy)

            if locators:
                print "-exporting "+str(len(locators))+" locators:"
                self.writeLocatorsToPyFile(locators, self.filePy)
                
            self.filePy.write('\n')
            self.filePy.write('nuke.frame('+str(self.currentFrame)+')\n\n')				
            self.filePy.write('nuke.scriptSave("'+self.path+'")\n\n\n')	
            self.filePy.close()
            
            # if there is something to export, generate the nuke script file (.nk) from the python script
            if objects or cameras or locators or lights:
                try:
                    # wait loop
                    print " > generating and saving the nuke script ..."
                    t = 0
                    if os.path.exists(self.path):
                        os.remove(self.path)
                    while not os.path.exists(self.path):
                        print ' > time spent: '+str(t)+' second(s)...'
                        
                        # generating the nuke script in the first iteration of the wait loop
                        if t == 0:
                            if os.name == 'nt':
                                eval(nukeexe+' -t '+pyFile+'')
                            else:
                                os.system('nuke -t '+pyFile+' &')

                        # check if the nuke script is generated. else pause 1 second and go again in the wait loop
                        if os.path.exists(self.path):
                            break
                        else:
                            time.sleep(1)
                            t += 1
                    if os.path.exists(self.path):
                        print "export successfully: "+self.path
                        print "os.system('scite "+pyFile+" &')"
                        print "nuke "+self.path
                        print "os.system('nuke "+self.path+" &')"

                        cmds.confirmDialog(t = 'Success !', m = 'The nuke script has been generated.\nSee script editor for more informations.')
                    else:
                        print 'failed to save the file...'
                        print "os.system('scite "+pyFile+" &')"
                        
                        cmds.confirmDialog(t = 'Error !', m = 'The nuke script has NOT been generated.\nSee script editor for more informations.')
                except:
                    print 'failed to save the file...'
                    print "os.system('scite "+pyFile+" &')"
                    
                    cmds.confirmDialog(t = 'Error !', m = 'The nuke script has NOT been generated.\nSee script editor for more informations.')
            else:
                cmds.confirmDialog(t = 'Warning', m = 'There is nothing to export !')          
        else:
            cmds.confirmDialog(t = 'Error', m = 'The output file is not correct.\nex: /<path>/nukefile.nk')
        
        #set display back on
        self.setDisplayOn()
        
        # set playback at the original frame
        cmds.currentTime(self.currentFrame)

        #select original selection
        if self.originalSel:
            cmds.select(self.originalSel, r = True)
        else:
            pass
        
        #end
        print "----------------| end |----------------"
        
    def filterSelection(self, selection):
    
        objects = []
        cameras = []
        locators = []
        lights = []

        for node in selection:
            if cmds.nodeType(node) == "camera":
                cameras.append(cmds.listRelatives(node, p = True)[0])
            
            if cmds.nodeType(node) == "mesh":
                objects.append(cmds.listRelatives(node, p = True)[0])
                
            if cmds.nodeType(node) == "locator":
                locators.append(cmds.listRelatives(node, p = True)[0])
            
            if cmds.nodeType(node) == "light":
                lights.append(cmds.listRelatives(node, p = True)[0])
        
        return objects, cameras, locators, lights
        
    def writeObjectsToPyFile(self, objects, filePy):
        
        print objects
        
        # load objExport plugin if not already loaded
        loaded = False
        
        if not "objExport" in cmds.pluginInfo( query=True, listPlugins=True ):
            objExportPlugin = cmd.getstatusoutput('echo $SOFTWARE/maya/$MAYA_MAJOR_VERSION/"$UNAME"."$DIST"."$SARCH"/bin/plug-ins/objExport.so ')[1]
            if os.path.exists(objExportPlugin):
                print cmds.loadPlugin(objExportPlugin, quiet = True)
                loaded = cmds.pluginInfo( "objExport", l = True, query = True)
                if not loaded:
                    print 'objExport plugin not loaded !'
                    cmds.confirmDialog(t = 'Warning', m = 'You need to load the objExport plugin.\ngoto Window>Settings Preferences>Plug-in Manager')
                    loaded = False
        else:
            print 'objExport already loaded...'
            loaded = True
            
        if loaded:

            # search for animated meshes
            animMeshes = []
            deformedMeshes = []
            staticMeshes = []
            
            for object in objects:
            
                objTx = '%s.tx' % object
                objTy = '%s.ty' % object
                objTz = '%s.tz' % object
                objRx = '%s.tx' % object
                objRy = '%s.ty' % object
                objRz = '%s.tz' % object
                objSx = '%s.tx' % object
                objSy = '%s.ty' % object
                objSz = '%s.tz' % object
                objVisible = '%s.visibility' % object

                if cmds.connectionInfo( objTx, isDestination=True) or\
                    cmds.connectionInfo( objTy, isDestination=True) or\
                    cmds.connectionInfo( objTz, isDestination=True) or\
                    cmds.connectionInfo( objRx, isDestination=True) or\
                    cmds.connectionInfo( objRy, isDestination=True) or\
                    cmds.connectionInfo( objRz, isDestination=True) or\
                    cmds.connectionInfo( objSx, isDestination=True) or\
                    cmds.connectionInfo( objSy, isDestination=True) or\
                    cmds.connectionInfo( objSz, isDestination=True) or\
                    cmds.connectionInfo( objVisible, isDestination=True):
                    
                    deformedMeshes.append(object)
                else:
                    staticMeshes.append(object)
            
            #print '--animated: '+str(animMeshes)
            print '--deformed: '+str(deformedMeshes)
            print '--static: '+str(staticMeshes)
            
            # mesh path
            meshPath = os.path.dirname(self.path)+'/'+os.path.basename(self.path).split('.')[-0]+'/'
            if not os.path.exists(meshPath):
                os.makedirs(meshPath)

            #############
            # static meshes ###
            #############
            
            if staticMeshes:

                filePy.write('# creating readGeos \n\n')

                for mesh in staticMeshes:
                    
                    print 'exporting: '+mesh
                    
                    filePy.write('# creating "'+mesh+'" \n')

                    cmds.select(mesh, r = True)
                    
                    meshname = meshPath+mesh.replace(":", "_")+'.obj'
                    rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
                    meshRot = cmds.getAttr(mesh.replace(":", "_")+".rotateOrder")
                    meshRotationOrder = rotList[meshRot]
                    
                    cmds.file(meshname, pr = 1, typ = "OBJexport", es = 1, op = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=1")

                    # write to pyFile
                    filePy.write('readGeo = nuke.createNode("ReadGeo")\n')
                    filePy.write('readGeo.knob("file").setValue("'+meshname+'")\n')
                    filePy.write('readGeo.setName("'+mesh.replace(":", "_")+'")\n')
                    filePy.write('readGeo.knob("selected").setValue(False)\n')
                    filePy.write('readGeo.knob("rot_order").setValue("'+meshRotationOrder+'")\n\n')
                    
            #############
            # deformed meshes #
            #############
            
            if deformedMeshes:
                
                for mesh in deformedMeshes:
                    
                    print 'exporting animated/deformed: '+mesh
                    
                    filePy.write('# creating "'+mesh+'" \n')

                    cmds.select(mesh, r = True)
                    meshname = meshPath+mesh.replace(":", "_")+'.####.obj'
                    
                    # get maya attributes
                    rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
                    meshRot = cmds.getAttr(mesh+".rotateOrder")
                    meshRotationOrder = rotList[meshRot]
                    
                    # write to pyFile
                    filePy.write('readGeo = nuke.createNode("ReadGeo")\n')
                    filePy.write('readGeo.knob("file").setValue("'+meshname+'")\n')
                    filePy.write('readGeo.setName("'+mesh.replace(":", "_")+'")\n')
                    filePy.write('readGeo.knob("selected").setValue(False)\n')
                    filePy.write('readGeo.knob("rot_order").setValue("'+meshRotationOrder+'")\n\n')

                
                for frame in range(self.firstFrame, self.lastFrame+1):
                    
                    cmds.currentTime(frame)
                    
                    for mesh in deformedMeshes:
                        cmds.select(mesh, r = True)
                        meshname = meshPath+mesh.replace(":", "_")+'.'+str(int(frame))+'.obj'
                        print meshname
                        cmds.file(meshname, f = True, pr = 1, typ = "OBJexport", es = 1, op = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=1")

    def writeCamerasToPyFile(self, cameras, filePy):
            
        for camera in cameras:
            
            filePy.write('# creating "'+camera+'" \n')

            cmds.select(camera, r = True)
            cameraShape = cmds.listRelatives(camera)[0]

            # get maya attributes			
            rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
            camRot = cmds.getAttr(camera+".rotateOrder")
            cameraRotationOrder = rotList[camRot]
            nearClip = float(cmds.getAttr(cameraShape+".nearClipPlane"))
            farClip = float(cmds.getAttr(cameraShape+".farClipPlane"))
            
            # try to get hub data
            
            #hubData, hubVersion, hubStart, hubEnd = Infos.getHubData(cameraShape)
            hubData, hubVersion, hubStart, hubEnd = '','','',''
            
            # write to pyFile
            filePy.write('camera = nuke.createNode("Camera2")\n')
            filePy.write('camera.setName("'+camera+'")\n')
            filePy.write('camera.knob("selected").setValue(False)\n')
            filePy.write('camera.knob("rot_order").setValue("'+cameraRotationOrder+'")\n\n')
            filePy.write('camera.knob("near").setValue('+str(nearClip)+')\n')
            filePy.write('camera.knob("far").setValue('+str(farClip)+')\n')
            
            if hubData:
                label = str(hubStart)+"-"+str(hubEnd)+" : v"+hubVersion
                filePy.write('camera.knob("label").setValue("'+label+'")\n\n')
            
        for frame in range(self.firstFrame, self.lastFrame+1):
            
            filePy.write('nuke.frame('+str(int(frame))+')\n')
            cmds.currentTime(frame)
            
            #print 'processing frame: '+str(frame)
            
            for camera in cameras:
                
                cameraShape = cmds.listRelatives(camera)[0]
                
                # get worldspace attributes
                xformT = cmds.xform(camera, t = True, ws=True, q = True)
                xformR = cmds.xform(camera, ro = True, ws=True, q = True)
                xformS = cmds.xform(camera, s = True, r = True, q = True)
                
                focal = float(cmds.getAttr(cameraShape+".focalLength"))
                hap = float(cmds.getAttr(cameraShape+".horizontalFilmAperture"))/ 0.0393700787
                vap = float(cmds.getAttr(cameraShape+".verticalFilmAperture"))/ 0.0393700787

                filePy.write('cameraToAnimate = nuke.toNode("'+camera+'")\n')
                
                #set translate
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[0]))+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[1]))+', '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[2]))+', '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("translate").setKeyAt('+str(frame)+')\n')
                
                #set rotate					
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[0]))+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[1]))+', '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[2]))+', '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("rotate").setKeyAt('+str(frame)+')\n')
                
                # set scale
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[0]))+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[1]))+', '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[2]))+', '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("scaling").setKeyAt('+str(frame)+')\n')
                
                #set focal hap and vap
                filePy.write('cameraToAnimate.knob("focal").setValueAt('+str(focal)+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("focal").setKeyAt('+str(frame)+')\n')
                filePy.write('cameraToAnimate.knob("haperture").setValueAt('+str(hap)+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("haperture").setKeyAt('+str(frame)+')\n')
                filePy.write('cameraToAnimate.knob("vaperture").setValueAt('+str(vap)+', '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("vaperture").setKeyAt('+str(frame)+')\n')
                
        
        
    def writeLocatorsToPyFile(self, locators, filePy):

        print locators
        
        animLocators = []
        staticLocators = []
        
        # check if animated
        
        for locator in locators:
        
            locTx = '%s.tx' % locator
            locTy = '%s.ty' % locator
            locTz = '%s.tz' % locator
            locRx = '%s.tx' % locator
            locRy = '%s.ty' % locator
            locRz = '%s.tz' % locator
            locSx = '%s.tx' % locator
            locSy = '%s.ty' % locator
            locSz = '%s.tz' % locator
            locVisible = '%s.visibility' % locator

            if cmds.connectionInfo( locTx, isDestination=True) or\
                cmds.connectionInfo( locTy, isDestination=True) or\
                cmds.connectionInfo( locTz, isDestination=True) or\
                cmds.connectionInfo( locRx, isDestination=True) or\
                cmds.connectionInfo( locRy, isDestination=True) or\
                cmds.connectionInfo( locRz, isDestination=True) or\
                cmds.connectionInfo( locSx, isDestination=True) or\
                cmds.connectionInfo( locSy, isDestination=True) or\
                cmds.connectionInfo( locSz, isDestination=True) or\
                cmds.connectionInfo( locVisible, isDestination=True):
                animLocators.append(locator)
            else:
                staticLocators.append(locator)
        
        #print '--animated: '+str(animMeshes)
        print '--animated: '+str(animLocators)
        print '--static: '+str(staticLocators)

        tmp = True

        if tmp: # ______________________ TMP_______ export animated locator even it's not____________

            # creating all locators
            
            for locator in locators:
                
                filePy.write('# creating "'+locator+'" \n')

                cmds.select(locator, r = True)

                # get maya attributes			
                rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
                locRot = cmds.getAttr(locator+".rotateOrder")
                locatorRotationOrder = rotList[locRot]
                
                # write to pyFile
                filePy.write('locator = nuke.createNode("Axis")\n')
                filePy.write('locator.setName("'+locator+'")\n')
                filePy.write('locator.knob("selected").setValue(False)\n')
                filePy.write('locator.knob("rot_order").setValue("'+locatorRotationOrder+'")\n\n')
            
            # animating all locators
            
            for frame in range(self.firstFrame, self.lastFrame+1):
                
                filePy.write('nuke.frame('+str(int(frame))+')\n')
                cmds.currentTime(frame)
                
                #print 'processing frame: '+str(frame)
                
                for locator in locators:
                    
                    # get worldspace attributes
                    xformT = cmds.xform(locator, t = True, ws=True, q = True)
                    xformR = cmds.xform(locator, ro = True, ws=True, q = True)
                    xformS = cmds.xform(locator, s = True, r = True, q = True)
                    
                    filePy.write('locatorToAnimate = nuke.toNode("'+locator+'")\n')
                    
                    #set translate
                    filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[0]))+', '+str(float(frame))+', 0)\n')
                    filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[1]))+', '+str(float(frame))+', 1)\n')
                    filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[2]))+', '+str(float(frame))+', 2)\n')
                    filePy.write('locatorToAnimate.knob("translate").setKeyAt('+str(frame)+')\n')
                    
                    #set rotate					
                    filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[0]))+', '+str(float(frame))+', 0)\n')
                    filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[1]))+', '+str(float(frame))+', 1)\n')
                    filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[2]))+', '+str(float(frame))+', 2)\n')
                    filePy.write('locatorToAnimate.knob("rotate").setKeyAt('+str(frame)+')\n')
                    
                    # set scale
                    filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[0]))+', '+str(float(frame))+', 0)\n')
                    filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[1]))+', '+str(float(frame))+', 1)\n')
                    filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[2]))+', '+str(float(frame))+', 2)\n')
                    filePy.write('locatorToAnimate.knob("scaling").setKeyAt('+str(frame)+')\n')
                    
    def getDisplay(self):
        panels = cmds.getPanel(allPanels = True)
        for panel in panels:
            try:
                self.panelsDisplay[panel] = {}
                for object in self.modelPanelObjects:
                    self.panelsDisplay[panel][object] = eval("cmds.modelEditor('"+panel+"', query = True, "+object+" = True)")
            except:
                pass
        
    def setDisplayOn(self):
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = "+str(value)+")")
    
    def setDisplayOff(self):
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = False)")
                
class ExportMayaToNukeUI:
    def __init__(self):
        
        try:
            global nukeexe
            dic = Infos().getPresets()
            nukeexe = dic['nukeexe']
        except:
            global nukeexe
            nukeexe = cmds.fileDialog2(cap='Please give the path of NukeX.X.exe', dir='c:/Program Files/*.exe',ff='NukeX.X.exe (*.exe)', fm=1)

        self.originalSel = cmds.ls(sl = True)
        cmds.select(hi = True)
        self.sel = [str(item) for item in cmds.ls(sl = True)]
        tkl = TicklePass()
        # self.activePass = tkl.getActivePass()
        # self.allPasses = tkl.getAllPass()
        self.activePass = ''
        self.allPasses = ['']
        print self.activePass, self.allPasses
        
        self.username = os.environ['USER']
        try:
            self.job = os.environ['JOB']
        except:
            self.job = 'n/a'
        try:
            self.shot = os.environ['SHOT']
        except:
            self.shot = 'n/a'
        try:
            self.scene = os.environ['SCENE']
        except:
            self.scene = 'n/a'
        try:
            self.discipline = os.environ['DISCIPLINE']			
        except:
            self.discipline = 'n/a'
        
        self.header = self.username+' - '+self.discipline+' - '+self.job+' '+self.shot+' - active pass: '+self.activePass+' frame range: '+str(ExportMayaToNuke().firstFrame)+'-'+str(ExportMayaToNuke().lastFrame)
        
        self.info = '/tmp/'+self.username+'/mayaToNukeInfos_'
        
        nukePath = '/jobs/'+self.job+'/'+self.shot+'/nuke/scene/'
        nukeUserPath = '/jobs/'+self.job+'/'+self.shot+'/nuke/scene/'+self.username+'/'
        mayaUserCompPath = '/jobs/'+self.job+'/'+self.shot+'/maya/comp/'+self.username+'/'
        
        self.outputPath = nukeUserPath
        
        if not os.path.exists(nukeUserPath):
            self.outputPath = mayaUserCompPath
            if not os.path.exists(mayaUserCompPath):
                self.outputPath = nukePath
        
    def strFromList(self, inputlist):
        
        return ''.join(inputlist), '    - '+'\n    - '.join(inputlist)
    
    def selectOutputFile(self, textfield):
        
        textfieldValue = cmds.textField(textfield, q = True)
        if textfieldValue:
            directoryMask = os.path.dirname(textfieldValue+"/*.nk")
        else:
            directoryMask = self.outputPath+"/*.nk"
            
        outputFile = cmds.fileDialog(m = 1, dm  = directoryMask)
        
        """
        if outputFile:
            if os.path.exists(outputFile):
                try:
                    os.remove(outputFile)
                except:
                    print 'cannot remove '+outputFile
        """
        
        cmds.textField(textfield, e = True, text = outputFile)

    def menuBar(self):
        
        cmds.menu( label='File', allowOptionBoxes = False )
        
        #cmds.menuItem(label = 'Export to Nuke', c = '')
        #cmds.menuItem(ob = True, c = '')
        
        exitC = 'import maya.cmds as cmds;cmds.deleteUI("exportMayaToNukeWindow", window = True);cmds.windowPref("exportMayaToNukeWindow", remove = True)'
        cmds.menuItem(label = 'Exit', c = exitC)
        
        cmds.menu(label = 'Help', helpMenu = True)
        helpC = 'import os;os.system("firefox http://intranet.mpc.local/film/film-departments/3d-dmp-environment/environment-software/maya-to-nuke/ &")'
        cmds.menuItem(label = 'Intranet Help', c = helpC)
        
        fun1C = 'import os;os.system("firefox http://www.google.com/images?q=mecha &")'
        cmds.menuItem(label = 'Bonus: Mechas !!', c = fun1C)
        
        fun2C = 'import os;os.system("firefox http://www.google.com/images?q=kittens &")'
        cmds.menuItem(label = 'Bonus: Kittens !!', c = fun2C)
        
        aboutC = 'import maya.cmds as cmds;cmds.confirmDialog(title = "about", message = "version v1.0", button = "OK")'
        cmds.menuItem(label = 'About', c = aboutC)


    def UI(self):
        
        if cmds.window("exportMayaToNukeWindow", exists = True):
            
            # set presets and delete ui
            Infos().setPresets(
                                {
                                    'fileInput' : str(cmds.textField("fileInput", q = True, text = True)),
                                    'doublePaneLayout' : cmds.paneLayout("doublePaneLayout", q = True, ps = True),
                                    'nukePath' : nukePath,
                                }
                              )
            cmds.deleteUI("exportMayaToNukeWindow", window = True)
        
        win = cmds.window("exportMayaToNukeWindow", title = "Maya To Nuke Interface", mb= True, w = 650, h = 300)	
            
        # build menu bar
        self.menuBar()
        
        mainform = cmds.formLayout("mainForm")
        
        # build helpLine
        #helpline = self.helpLine()
        #cmds.setParent('..')
        
        header = cmds.text(label = self.header)
        textField = cmds.textField('fileInput')
        cmds.textField('fileInput', e = True, text = self.outputPath, annotation = 'This is the output file')
        separator1 = cmds.separator()
        separatorTop = cmds.separator()
        separatorBottom = cmds.separator()
        txtOutput = cmds.text(label = "nuke script:")
        
        outputButton = cmds.button(label = " ... ", c = "mayaToNuke.ExportMayaToNukeUI().selectOutputFile('"+textField+"')")
        exportButton = cmds.button(label = "Export", c = "import maya.cmds as cmds;mayaToNuke.ExportMayaToNuke(cmds.textField('"+textField+"', q = True, text = True)).startExport()")
        closeButton = cmds.button(label = "Close", c = "import maya.cmds as cmds;import maya.cmds as cmds;mayaToNuke.Infos().setPresets({'fileInput' : "'str(cmds.textField("fileInput", q = True, text = True))'", 'doublePaneLayout' : "'cmds.paneLayout("doublePaneLayout", q = True, ps = True)'"});cmds.deleteUI('exportMayaToNukeWindow')")
        reloadButton = cmds.iconTextButton(label = "Refresh", st = 'iconOnly', i = MAYA_SHARE+'/refresh.jpg', c = "import maya.cmds as cmds;mayaToNuke.Infos().setPresets({'fileInput' : "'str(cmds.textField("fileInput", q = True, text = True))'", 'doublePaneLayout' : "'cmds.paneLayout("doublePaneLayout", q = True, ps = True)'"});reload(mayaToNuke);mayaToNuke.mayaToNuke();")
        
        cmds.button(exportButton, e = True, annotation = 'Generate Nuke script from selected items')
        cmds.button(closeButton, e = True, annotation = 'Close the mayaToNuke interface - Have a nice day -')
        cmds.iconTextButton(reloadButton, e = True, annotation = 'Refresh the UI with the current selection')
        cmds.button(outputButton, e = True, annotation = 'Browse for a Nuke file - please type the .nk extension')
        
        # build options panel
        pane = OptionPanel().doublePaneLayout()
            
        # organize layout
        # attachForm
        cmds.formLayout(mainform, edit = True, attachForm = [
                                            (reloadButton, "top", 5),
                                            (reloadButton, "right", 5),
                                            (header, "left", 5),
                                            (header, "top", 5),
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
                                            (pane, "left", 5),
                                            (pane, "right", 5)
                                            ])

        # attachControl
        cmds.formLayout(mainform, edit = True, attachControl = [
                                            (separator1, "top", 5, reloadButton),
                                            (txtOutput, "top", 5, separator1),
                                            (txtOutput, "top", 5, separator1),
                                            (textField, "left", 5, txtOutput),
                                            (textField, "right", 5, outputButton),
                                            (outputButton, "top", 4, separator1),
                                            (textField, "top", 5, separator1),
                                            (separatorTop, "top", 5, textField),
                                            (separatorBottom, "bottom", 5, exportButton),
                                            (pane, "top", 4, separatorTop),
                                            (pane, "bottom", 5, separatorBottom)
                                            ])
        
        # attachPosition
        cmds.formLayout(mainform, edit = True, attachPosition = [
                                            (exportButton, "right", 5, 50),
                                            (closeButton, "left", 5, 50)
                                            ])
        
        # set previous values
        try:
            dic = Infos().getPresets()
            cmds.textField("fileInput", e = True, text = dic['fileInput'])
            val1, val2 = dic['doublePaneLayout'][0], dic['doublePaneLayout'][2]
            cmds.paneLayout("doublePaneLayout", e = True, ps = [[1, val1, 100], [2, val2, 100]])

        except:
            print 'failed to apply presets'
            
        cmds.showWindow("exportMayaToNukeWindow")

def mayaToNuke():   
    print "\n----------------| "+__name__+" |----------------"
    if not os.path.exists('c:/tmp'):
        os.mkdirs('c:/tmp')
    mayaToNukeLaunch = ExportMayaToNukeUI()
    mayaToNukeLaunch.UI()

if __name__ == '__main__':
    mayaToNuke()