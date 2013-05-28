import nuke
import fnmatch
import os

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('nuke')

def deselectAll():
    for node in nuke.allNodes():
        node.setSelected(False)

def demosaicer(node):
    """
        takes a tiled image and deconstruct it to multiple pieces
    """
    savedPath = SETTINGS.get('demosaicerPath')
    if not savedPath:
        savedPath = ''

    panel = nuke.Panel('Demosaicer')
    panel.addFilenameSearch('Output path: ', savedPath)
    panel.addSingleLineInput('Texture name: ', 'eastEntrance')
    panel.addSingleLineInput('Tiles number: ', '10')
    show = panel.show()
    if show:
        path = panel.value('Output path: ')
        texturename = panel.value('Texture name: ')
        tilesNumber = panel.value('Tiles number: ')
        SETTINGS.add('demosaicerPath', path)
    else:
        nuke.message('No tiles!')
        raise UserWarning('No tiles!')

    textureNode = node
    textureSize = [float(textureNode.width()), float(textureNode.height())]
    
    rows = int(tilesNumber)
    columns = int(tilesNumber)
    tile = textureSize[0]/float(rows)
    
    # init values
    x = 0
    y = 0
    r = 0
    t = 0
    
    # go through the Y axis
    for column in range(columns):
        cropX = x
        cropR = r+tile
        cropY = y+tile
        cropT = t
        
        # go through the X axis
        for row in range(rows):
            # create crop
            deselectAll()
            sname = str('%02d' % row)
            tname = str('%02d' % column)
            cropNode = nuke.createNode('Crop', inpanel=False)
            cropNode.setName('bake_s'+sname+'t'+tname+'_crop')
            cropNode['box'].setValue([cropX, cropY, cropR, cropT])
            cropNode.setInput(0, textureNode)
            cropNode['softness'].setValue(0.0)
            cropNode['reformat'].setValue(True)
            
            # create write node
            writeNode = nuke.createNode('Write', inpanel=False)
            writeNode.setName('write_'+cropNode.name())
            # writeNode['raw'].setValue(True)
            writeNode['colorspace'].setValue('Linear')
            filename = 'LouvrePlaza_'+texturename+'_COL_LIN_s'+sname+'t'+tname+'_00_v004.exr'
            writeNode['file'].setValue(path+'/'+filename)

            # write the file to the disk
            frame = nuke.root()['first_frame'].value()
            nuke.execute(writeNode, frame, frame)

            # go to the next tile in X axis
            cropX += tile
            cropR += tile

        # go to the next tile in Y axis
        x = 0
        t += tile
        y += tile

def main():
    demosaicer(nuke.selectedNode())

if __name__ == '__main__':
    main()