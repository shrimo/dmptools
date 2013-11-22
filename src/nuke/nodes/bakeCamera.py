import nuke
import math

class BakeCamera():
    def __init__(self, createNewCam=True, usematrix=False):
        """ bake a selected camera """

        self.do_create = createNewCam
        self.usematrix = usematrix

        goodCameras = ['Camera', 'Camera2', 'hubCamera', 'fBakeCamera']
        try:
            basecamera = nuke.selectedNode()
        except:
            basecamera = None
            
        framerange = [int(nuke.root().knob('first_frame').getValue()), int(nuke.root().knob('last_frame').getValue())]
        
        if basecamera and basecamera.Class() in goodCameras:
            basecamera.knob('selected').setValue(False)
            self.cameraData = self.do_bake(basecamera, framerange)
            if self.do_create:
                projCamera = self.createCamera(basecamera, framerange, self.cameraData, self.usematrix)
        else:
            nuke.message("please select a render camera "+str(goodCameras))

    def do_bake(self, camera, framerange):
        cameraData = {}
        for frame in range(framerange[0], framerange[1]+1):
            cameraData[frame] = self.getCameraAttributes(camera, frame)
        
        return cameraData

    def getCameraAttributes(self, basecamera, frame):
        """ get the attributes values for a given frame """
        
        attributes = {}
        
        attributes['trOrder'] = basecamera.knob('xform_order').value()
        attributes['rotOrder'] = basecamera.knob('rot_order').value()
        attributes['focal'] = float(basecamera.knob('focal').getValueAt(frame))
        attributes['hap'] = float(basecamera.knob('haperture').getValueAt(frame))
        attributes['vap'] = float(basecamera.knob('vaperture').getValueAt(frame))
        attributes['near'] = float(basecamera.knob('near').getValueAt(frame))
        attributes['far'] = float(basecamera.knob('far').getValueAt(frame))
        attributes['win_translate'] = basecamera.knob('win_translate').getValueAt(frame)
        attributes['matrix'] = basecamera.knob('world_matrix').getValueAt(frame)
        attributes['translate'] = self.xformFromMatrix(basecamera, frame)[0]
        attributes['rotate'] = self.xformFromMatrix(basecamera, frame)[1]
        attributes['scaling'] = self.xformFromMatrix(basecamera, frame)[2]

        return attributes
        
    def xformFromMatrix(self, node, frame):
        """ used to transform matrix to translate, rotate, scale coord"""
        nuke.frame(frame)
        worldMatrix = node.knob('world_matrix')
        worldMatrixAt = node.knob('world_matrix').getValueAt(frame)
        
        matrix = nuke.math.Matrix4()

        worldMatrix = node.knob('world_matrix')
        matrix = nuke.math.Matrix4()
        for y in range(worldMatrix.height()):
            for x in range(worldMatrix.width()):
                matrix[x+(y*worldMatrix.width())] = worldMatrixAt[y+worldMatrix.width()*x]

        transM = nuke.math.Matrix4(matrix)
        transM.translationOnly()
        rotM = nuke.math.Matrix4(matrix)
        rotM.rotationOnly()
        scaleM = nuke.math.Matrix4(matrix)
        scaleM.scaleOnly()
        
        scale = (scaleM.xAxis().x, scaleM.yAxis().y, scaleM.zAxis().z)
        rot = rotM.rotationsZXY()
        rotate = (math.degrees(rot[0]), math.degrees(rot[1]), math.degrees(rot[2]))
        translate = (transM[12], transM[13], transM[14])
        
        return translate, rotate, scale
        
    def createCamera(self, basecamera, framerange, cameraData, usematrix):
        """ create a new bake camera """

        camera = nuke.createNode('Camera2', inpanel =  False)
        camera.setName(basecamera.name()+'_bakedCamera')
            
        for frame in range(framerange[0], framerange[1]+1):
            nuke.frame(frame)
            attributes = cameraData[frame]

            if usematrix:
                camera.knob('useMatrix').setValue(True)
                camera.knob('matrix').setValue(attributes['matrix'])
                camera.knob('matrix').setKeyAt(frame)
            else:
                camera.knob('translate').setValue(attributes['translate'])
                camera.knob('translate').setKeyAt(frame)
                camera.knob('rotate').setValue(attributes['rotate'])
                camera.knob('rotate').setKeyAt(frame)
                camera.knob('scaling').setValue(attributes['scaling'])
                camera.knob('scaling').setKeyAt(frame)

            camera.knob('focal').setValue(attributes['focal'])
            camera.knob('focal').setKeyAt(frame)

            camera.knob('haperture').setValue(attributes['hap'])
            camera.knob('vaperture').setValue(attributes['vap'])
            camera.knob('haperture').setKeyAt(frame)
            camera.knob('vaperture').setKeyAt(frame)

            camera.knob('near').setValue(attributes['near'])
            camera.knob('far').setValue(attributes['far'])
            camera.knob('near').setKeyAt(frame)
            camera.knob('far').setKeyAt(frame)
            
            camera.knob('xform_order').setValue(attributes['trOrder'])
            camera.knob('rot_order').setValue(attributes['rotOrder'])
            camera.knob('xform_order').setKeyAt(frame)
            camera.knob('rot_order').setKeyAt(frame)
            
            camera.knob('win_translate').setValue(attributes['win_translate'])
            camera.knob('win_translate').getValueAt(frame)

            camera.knob('xpos').setValue(basecamera.knob('xpos').value()+100)
            camera.knob('ypos').setValue(basecamera.knob('ypos').value())
            
        return camera
        