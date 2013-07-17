import os
import nuke

def coverageMap():
    
    # get start, end frames
    frameStart = int(nuke.thisNode().knob('frameStart').getValue())
    frameEnd = int(nuke.thisNode().knob('frameEnd').getValue())
    
    # get image
    imageName = nuke.thisNode().knob('coverageMapName').getValue().split('.')[0]
    modelName = ('%s.obj' %(imageName))

    cameraNode = nuke.thisNode().input(0)
    cameraRatio = cameraNode.knob('haperture').getValue()/cameraNode.knob('vaperture').getValue()

    # create 256 pixels format
    imageFormatName = ("coverageMap_projectMap")
    resX = 256
    resY = int (resX/cameraRatio) 
    imageFormat = ("%s %s %s" % (resX, resY, imageFormatName))

    nuke.addFormat(imageFormat)
    nuke.thisNode().node('ConstantProjection').knob('format').setValue(imageFormatName)

    print '### SAVE MODEL ###'
    writeGeoNode = nuke.thisNode().node('WriteGeo_input')

    writeGeoNode.knob('file').setValue(modelName)
    nuke.execute(writeGeoNode, frameStart, frameStart, 1)

    print '### READ MODEL ###'
    readGeoNode = nuke.thisNode().node('ReadGeo_input')
    readGeoNode.knob('file').setValue(modelName)
    readGeoNode.knob('reload').execute()


    print '### WRITE FIRST FRAME ###'
    writeFirstNode = nuke.thisNode().node('WriteFirst')
    writeFirstNode.knob('file').setValue('%s.%s.exr' %(imageName, frameStart-1))
    nuke.execute(writeFirstNode, frameStart, frameStart, 1)

    readLastNode = nuke.thisNode().node('ReadLast')
    readLastNode.knob('file').setValue('%s.####.exr' %(imageName))
    readLastNode.knob('first').setValue(frameStart-1)
    readLastNode.knob('last').setValue(frameEnd)

    readLastNode.knob('reload').execute()

    nuke.thisNode().node('SwitchReadLast').knob('which').setValue(1)

    print '### WRITE SEQUENCE ###'
    writeSequenceNode = nuke.thisNode().node('WriteSequence')
    writeSequenceNode.knob('file').setValue('%s.####.exr' %imageName)
    nuke.execute(writeSequenceNode,frameStart,frameEnd,1)

    os.system ('cp %s.%s.exr %s.exr' %(imageName,frameEnd,imageName))

    readResultNode = nuke.thisNode().node('ReadResult')
    readResultNode.knob('file').setValue('%s.exr' %imageName)
    readResultNode.knob('reload').execute()

    readLastNode.knob('file').setValue('%s.exr' %imageName)
    readLastNode.knob('reload').execute()


    nuke.thisNode().node('SwitchOutput').knob('which').setValue(1)
    nuke.thisNode().node('SwitchReadLast').knob('which').setValue(0)

    # clean unused stuff
    os.system('rm %s.*.exr' %imageName)
    os.system('rm %s' %modelName)



