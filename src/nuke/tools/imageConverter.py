import nuke
import nukescripts
import os

import dmptools.utils.nukeCommands as nukeCommands
from dmptools.settings import SettingsManager

import dmptools_misc.framestore as framestore

SETTINGS = SettingsManager('nuke')
FCONVERTIONPATH = framestore.__path__[0]

def makeProxy(node, filePath, filePathBool, fileType, colorspace, scaleFactor, createRead, alpha, anim, overwrite, convertion, texconvert):
    """
    batch converts the node
    """

    nodesToDelete = []

    nukeCommands.deselectAll()
    nukeCommands.selectReplace(node)

    file = node['file'].value().split('.')[-2]
    if file in ['####', '%04d']:
        file = node['file'].value().split('.')[-3]
    filename = os.path.basename(file)

    # create reformat for scale
    if not scaleFactor == 1:
        reformat = nuke.createNode('Reformat', inpanel = False)
        reformat['type'].setValue('scale')
        reformat['scale'].setValue(scaleFactor)
        nodesToDelete.append(reformat)

    # create convertion node
    if convertion:
        node['raw'].setValue(True)
        convertionNode = nuke.nodePaste(FCONVERTIONPATH+"/sRGB_to_Linear.nk")
        convertionNode['in_colorspace'].setValue('cineon')
        convertionNode['out_colorspace'].setValue('linear')
        nodesToDelete.append(convertionNode)

    # create write for outputfile
    write = nuke.createNode('Write', inpanel = False)
    nodesToDelete.append(write)

    # check the tex convertion on the write node if exists
    if texconvert:
        try:
            write['texConvertCheckbox'].setValue(True)
        except:
            print 'tex convertion not found...'

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

    # delete tmp nodes
    nukeCommands.deselectAll()
    for node in nodesToDelete:
        nukeCommands.selectAdd(node)
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
    """
    main UI
    """
    # checkfor the saved settings
    path = SETTINGS.get('imageConvert_path')
    if not 'path' in locals():
        path = ''
    fileType = SETTINGS.get('imageConvert_fileType')
    if not 'fileType' in locals():
        fileType = 'exr'
    colorspace = SETTINGS.get('imageConvert_colorspace')
    if not 'colorspace' in locals():
        colorspace = 'raw'
    texconvert = SETTINGS.get('imageConvert_texconvert')
    if not 'texconvert' in locals():
        texconvert = False
    createRead = SETTINGS.get('imageConvert_createRead')
    if not 'createRead' in locals():
        createRead = False
    alpha = SETTINGS.get('imageConvert_alpha')
    if not 'alpha' in locals():
        alpha = False
    convertion = SETTINGS.get('imageConvert_convertion')
    if not 'convertion' in locals():
        convertion = False
    sourcePath = SETTINGS.get('imageConvert_sameAsSource')
    if not 'sourcePath' in locals():
        sourcePath = False
    overwrite = SETTINGS.get('imageConvert_overwrite')
    if not 'overwrite' in locals():
        overwrite = True
    anim = SETTINGS.get('imageConvert_anim')
    if not 'anim' in locals():
        anim = False

    # create UI
    panel = nuke.Panel('Nuke Converter')
    panel.addFilenameSearch("output folder: ", path)
    panel.addBooleanCheckBox("same path as source", sourcePath)
    panel.setWidth(400)

    # file types
    fileTypesL = ['exr', 'tif', 'jpg']
    fileTypesL.remove(fileType)
    fileTypesL.insert(0, fileType)
    fileTypes = ' '.join(fileTypesL)

    # colorspaces
    colorspacesL = ['raw', 'linear', 'Cineon', 'sRGB']
    colorspacesL.remove(colorspace)
    colorspacesL.insert(0, colorspace)
    colorspaces = ' '.join(colorspacesL)

    panel.addEnumerationPulldown("format: ", fileTypes)
    # panel.addEnumerationPulldown("from: ", colorspaces)
    panel.addEnumerationPulldown("colorspace: ", colorspaces)
    panel.addBooleanCheckBox("F sRGB to linear", convertion)
    panel.addBooleanCheckBox("tex convert", texconvert)
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
        convertion = panel.value("F sRGB to linear")
        texconvert = panel.value("tex convert")
        scaleFactor = float(panel.value("scale factor: "))
        createRead = int(panel.value("create read node"))
        alpha = panel.value("keep alpha channel")
        anim = int(panel.value("Image Sequence"))
        overwrite = panel.value("Overwrite")
        
        # save settings
        SETTINGS.add('imageConvert_colorspace', colorspace)
        SETTINGS.add('imageConvert_fileType', fileType)
        SETTINGS.add('imageConvert_path', filePath)
        SETTINGS.add('imageConvert_alpha', alpha)
        SETTINGS.add('imageConvert_convertion', convertion)
        SETTINGS.add('imageConvert_texconvert', texconvert)
        SETTINGS.add('imageConvert_sameAsSource', filePathBool)
        SETTINGS.add('imageConvert_overwrite', overwrite)
        SETTINGS.add('imageConvert_createRead', createRead)
        SETTINGS.add('imageConvert_anim', anim)

        # convert nodes
        for node in nodes:
            makeProxy(node, filePath, filePathBool, fileType, colorspace, scaleFactor, createRead, alpha, anim, overwrite, convertion, texconvert)
                    
def main():
    nodes = nuke.selectedNodes()
    if nodes:
        makeProxyUI(nodes)

if __name__ == '__main__':
    main()
