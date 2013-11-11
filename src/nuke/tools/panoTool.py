import nuke

def createCamera(scene, input, rotation):
    camera = nuke.createNode('Camera2', inpanel=False)
    camera['selected'].setValue(False)
    camera.setName('PanoTool_camera')
    camera['rotate'].setValue([0, rotation, 0])
    
    scene.setInput(input, camera)

    return camera

def _add_callback_on_knob():
    node = nuke.thisNode()
    knob = nuke.thisKnob()
    if knob.name() == 'cameras':
        for n in nuke.allNodes():
            if 'PanoTool_camera' in n.name():
                nuke.delete(n)
        camerasN = knob.value()
        print camerasN
        for i in range(float(camerasN)):
            initalRotation = int(360/camerasN)
            createCamera(node, i, i*initalRotation)

def addCallback():
    nuke.callbacks.addKnobChanged(_add_callback_on_knob, args=(), kwargs={}, nodeClass = 'Scene')
    