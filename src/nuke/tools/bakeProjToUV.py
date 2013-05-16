import nuke
import nukescripts

import dmptools.utils.nukeCommands as nukeCommands
from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('nuke')

def bakeIt(node, filePath, fileSize,  fileType, outcolorspace, framerange, connectToObj, alpha, antialiasing, samples, shutter):
    """
    main method used to render the selected node from the UV perspective

    """
    # create render format
    if fileSize == '1K':        
        formatN = ("bakeUV_1K")
        form = ("1024 1024 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])
    
    if fileSize == '2K':        
        formatN = ("bakeUV_2K")
        form = ("2048 2048 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])

    if fileSize == '4K':        
        formatN = ("bakeUV_4K")
        form = ("4096 4096 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])
    
    if fileSize == '8K':        
        formatN = ("bakeUV_8K")
        form = ("8192 8192 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])	
    
    nukeCommands.selectReplace(node)
    
    # create the renderer
    scanlineR = nuke.createNode('ScanlineRender', inpanel = False)
    scanlineR['name'].setValue("Scanline_"+node.name()+"_bake")
    scanlineR['projection_mode'].setValue('uv')
    
    scanlineR['antialiasing'].setValue(antialiasing)
    scanlineR['samples'].setValue(samples)
    scanlineR['shutter'].setValue(shutter)
    
    nukeCommands.deselectAll()
    
    # create the format node
    reformatBake = nuke.createNode('Reformat', inpanel = False)
    reformatBake['name'].setValue("reformat_"+node.name()+"_bake")
    reformatBake['format'].setValue("bakeUV_"+fileSize)
    
    nukeCommands.deselectAll()
    
    scanlineR.setInput(0, reformatBake)
    nukeCommands.selectReplace(scanlineR)
    
    # mpcCol = nuke.createNode('MPC_ColIO_!MPC_COLIO_VERSION!', inpanel = False)
    # mpcCol['inspace'].setValue('Linear')
    # mpcCol['output_space'].setValue(outcolorspace)
    
    # create the write node
    writeNode = nuke.createNode('Write', inpanel = False)        
    writeNode['file_type'].setValue(fileType)
    writeNode['name'].setValue("write_"+node.name()+"_bake")
    writeNode['raw'].setValue(True)

    try:
        startF = int(framerange.split("-")[0])
        endF = int(framerange.split("-")[1])
        if startF == endF:
            writeNode['file'].setValue(filePath+node.name()+"_COL."+fileType)
        else:
            writeNode['file'].setValue(filePath+node.name()+"_COL.%04d."+fileType)
        
    except:
        startF = int(framerange)
        endF = int(framerange)
        writeNode['file'].setValue(filePath+node.name()+"_COL."+fileType)
        
    if alpha == 1:	
        writeNode['channels'].setValue('rgba')
    
    # start the render
    nuke.execute(writeNode, startF, endF)
    
    # clean the uneccessary nodes
    nukeCommands.deselectAll()
    nukeCommands.selectAdd(scanlineR)
    nukeCommands.selectAdd(reformatBake)
    # nukeCommands.selectAdd(mpcCol)
    nukeCommands.selectAdd(writeNode)
    nukescripts.node_delete()
    nukeCommands.deselectAll()
    
    # create the UV texture read node
    readUV = nuke.createNode('Read', inpanel = False)
    readUV['name'].setValue("Read_"+node.name()+"_baked")
    readUV['file'].setValue(filePath+node.name()+"_COL."+fileType)
    readUV['raw'].setValue(True)
    
    lastNode = readUV

    # lastNode = nuke.createNode('MPC_ColIO_'+MPC_colio, inpanel = False)
    # lastNode['inspace'].setValue('Linear')
    # lastNode['output_space'].setValue(outcolorspace)
    
    if alpha:
        lastNode = nuke.createNode('Premult', inpanel = False)
    
    if connectToObj:    
        node.setInput(0, lastNode)
    
def bakeItUI(nodes):
    """ 
    UI
    """

    # get settings
    try:
        path = SETTINGS.get('bakeProj_path')[0]
    except:
        path = ''
    try:
        alpha = SETTINGS.get('bakeProj_alpha')[0]
    except:
        alpha = False
    
    availableColorspace = 'Linear Log sRGB Screen'
    fileTypes = 'tif exr jpg'
    fileSizes = '1K 2K 4K 8K'
    antialiasingMenu = 'none low medium high'
    
    panel = nuke.Panel("Bake Proj To UV")
    panel.setWidth(400)
    panel.addFilenameSearch("Path of UV output files: ", path)
    panel.addEnumerationPulldown("Size: ", fileSizes)
    panel.addEnumerationPulldown("File type: ", fileTypes)
    panel.addBooleanCheckBox("alpha channel", alpha)
    panel.addEnumerationPulldown("output colorspace: ", availableColorspace)
    panel.addSingleLineInput("Frame Range: ", str(int(nuke.root()['first_frame'].getValue()))+"-"+str(int(nuke.root()['last_frame'].getValue())))
    panel.addEnumerationPulldown("Antialiasing: ", antialiasingMenu)
    panel.addSingleLineInput("S-R Samples", '1')
    panel.addSingleLineInput("S-R Shutter", '0')
    panel.addBooleanCheckBox("Connect to object ?", 0)
    
    retVar = panel.show()
    if retVar:
        # get panel values
        filePath = panel.value("Path of UV output files: ")
        fileSize = panel.value("Size: ")
        fileType = panel.value("File type: ")
        outcolorspace = panel.value("output colorspace: ")
        framerange = panel.value("Frame Range: ")
        connectToObj = panel.value("Connect to object ?")
        alpha = int(panel.value("alpha channel"))
        antialiasing = panel.value("Antialiasing: ")
        samples = int(panel.value("S-R Samples"))
        shutter = int(panel.value("S-R Shutter"))
        
        # add settings
        SETTINGS.add('bakeProj_alpha', alpha)
        SETTINGS.add('bakeProj_path', filePath)

        for node in nodes:
            bakeIt(node, filePath, fileSize,  fileType, outcolorspace, framerange, connectToObj, alpha, antialiasing, samples, shutter)
    else:
        print 'abort by the user...'

def main():
    nodes = nuke.selectedNodes()
    if nodes:     
        bakeItUI(nodes)
    else:
        nuke.message('Please select one or multiple 3d objects.')

if __name__ == '__main__':
    main()