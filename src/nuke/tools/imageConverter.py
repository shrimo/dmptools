import nuke
import nukescripts
import os

import dmptools.utils.nukeCommands as nukeCommands
from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('nuke')

def makeProxy(node, filePath, filePathBool, fileType, colorspace, scaleFactor, createRead, alpha, anim, overwrite):
    
    nukeCommands.deselectAll()
    nukeCommands.selectReplace(node)
    reformat = nuke.createNode('Reformat', inpanel = False)
    reformat['type'].setValue('scale')
    reformat['scale'].setValue(scaleFactor)
    
    file = node['file'].value().split('.')[-2]
    if file in ['####', '%4d']:
        file = node['file'].value().split('.')[-3]
    filename = os.path.basename(file)
    write = nuke.createNode('Write', inpanel = False)

    if not filePathBool:
        if anim:
            readFile = filePath+filename+'.####.'+fileType
        else:
            readFile = filePath+filename+'.'+fileType            
        if os.path.exists(readFile) and not overwrite:
            panel = nuke.Panel('warning, file name already exists !')
            panel.addSingleLineInput('please type new file name:', os.path.basename(file))
            val = panel.show()
            if val == 1:
                readFile = str(filePath+panel.value('please type new file name:')+'.'+fileType)
            #else:
            #    readFile = filePath+filename+'_copy.'+fileType
                
        write['file'].setValue(readFile)
    else:
        if anim:
            readFile = file+'.####.'+fileType
        else:
            readFile =file+'.'+fileType            
        
        if os.path.exists(readFile):
            panel = nuke.Panel('warning, file name already exists !')
            panel.addSingleLineInput('please type new file name:', os.path.basename(file))
            val = panel.show()
            if val == 1:
                readFile = str(os.path.dirname(file)+'/'+panel.value('please type new file name:')+'.'+fileType)
            else:
                readFile = filePath+filename+'_copy.'+fileType
        
        write['file'].setValue(readFile)
        
    write['file_type'].setValue(fileType)
    
    if fileType == 'jpg':
        write['_jpeg_quality'].setValue(1)
    if colorspace == 'raw':
        write['raw'].setValue(True)
    else:
        write['colorspace'].setValue(colorspace)
    try:
        write['views'].setValue('main')
    except:
        write['views'].setValue('left')
    
    if alpha == 1:
        write['channels'].setValue('rgba')

    if anim == 1:
        framerange = frameRange()
        try:
            first, last = int(framerange.split(',')[0]), int(framerange.split(',')[1])
        except:
            first, last = int(framerange.split('-')[0]), int(framerange.split('-')[1])
            
        nuke.execute(write, first, last)    
    else:
        nuke.execute(write, 1,1)    

    if createRead == 1:
        nukeCommands.deselectAll()
        nuke.createNode('Read', inpanel = False).setName(node.name()+'_convert')
        read = nuke.selectedNode()
        read['file'].setValue(readFile)
        if colorspace == 'raw':
            read['raw'].setValue(True)
        else:
            read['colorspace'].setValue(colorspace)
        if anim:
            read['first'].setValue(first)
            read['last'].setValue(last)

    nukeCommands.deselectAll()
    nukeCommands.selectAdd(reformat)
    nukeCommands.selectAdd(write)
    nukescripts.node_delete()
    nukeCommands.deselectAll()    
    
def frameRange():
    
    panel = nuke.Panel('frame range')
    panel.addSingleLineInput('range:', str(int(nuke.root()['first_frame'].getValue()))+','+str(int(nuke.root()['last_frame'].getValue())))
    val = panel.show()
    if val ==1:
        frames = panel.value('range:')
        return frames
    
def makeProxyUI(nodes):

    path = SETTINGS.get('imageConvert_path')
    if not path:
        path = ''
    createRead = SETTINGS.get('imageConvert_createRead')
    if not createRead:
        createRead = False
    alpha = SETTINGS.get('imageConvert_alpha')
    if not alpha:
        alpha = False
    sourcePath = SETTINGS.get('imageConvert_sameAsSource')
    if not sourcePath:
        sourcePath = False
    overwrite = SETTINGS.get('imageConvert_overwrite')
    if not overwrite:
        overwrite = True
    anim = SETTINGS.get('imageConvert_anim')
    if not anim:
        anim = True

    panel = nuke.Panel('Nuke Converter')
    panel.addFilenameSearch("output folder: ", path)
    panel.addBooleanCheckBox("same path as source", sourcePath)
    panel.setWidth(400)
    fileTypes = 'exr tif jpg'
    colorspaces = 'raw linear Cineon sRGB'
    panel.addEnumerationPulldown("format: ", fileTypes)
    # panel.addEnumerationPulldown("from: ", colorspaces)
    panel.addEnumerationPulldown("colorspace: ", colorspaces)
    panel.addSingleLineInput("scale factor: ", "1")
    panel.addBooleanCheckBox("create read node", createRead)
    panel.addBooleanCheckBox("alpha channel", alpha)
    panel.addBooleanCheckBox("Image Sequence", anim)
    panel.addBooleanCheckBox("Overwrite", overwrite)

    val = panel.show()
    if val:
        
        filePath = panel.value("output folder: ")
        filePathBool = panel.value("same path as source")
        fileType = panel.value("format: ")
        # convertFrom = panel.value("from: ")
        colorspace = panel.value("colorspace: ")
        scaleFactor = float(panel.value("scale factor: "))
        createRead = int(panel.value("create read node"))
        alpha = panel.value("keep alpha channel")
        anim = int(panel.value("Image Sequence"))
        overwrite = panel.value("Overwrite")
        
        SETTINGS.add('imageConvert_path',filePath)
        SETTINGS.add('imageConvert_alpha', alpha)
        SETTINGS.add('imageConvert_sameAsSource', filePathBool)
        SETTINGS.add('imageConvert_overwrite', overwrite)
        SETTINGS.add('imageConvert_createRead', createRead)
        SETTINGS.add('imageConvert_anim', anim)

        for node in nodes:
            makeProxy(node, filePath, filePathBool, fileType, colorspace, scaleFactor, createRead, alpha, anim, overwrite)
                    
def main():
    nodes = nuke.selectedNodes()
    if nodes:
        makeProxyUI(nodes)

if __name__ == '__main__':
    main()
