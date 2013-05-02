import nuke
import fnmatch
import os

def deselectAll():
    for node in nuke.allNodes():
        node.setSelected(False)

def getResolution():
        panel = nuke.Panel("Specify the resolution:")
        panel.setWidth(200)
        panel.addSingleLineInput("Resolution: ", '2048')
        show = panel.show()
        if show == 1:
            resolution = panel.value("Resolution: ")
            return resolution
        else:
            nuke.message('No resolution selected!')            
            raise UserWarning('No resolution selected!')

def getResolutionFromNodes(nodes):
    resolutions = set([node.width() for node in nodes])
    
    if not len(resolutions) == 1:
        resolutionsStr = ' '.join(str(r) for r in resolutions)
        panel = nuke.Panel("Select the resolution:")
        panel.setWidth(200)
        panel.addEnumerationPulldown("Available resolutions: ", resolutionsStr)
        show = panel.show()
        if show == 1:
            resolution = panel.value("Available resolutions: ")
            return resolution
        else:
            nuke.message('No resolution selected!')            
            raise UserWarning('No resolution selected!')
            
    else:
        resolution = int(''.join(str(r) for r in resolutions))
        return resolution

def getTextureFiles(path, component, prefix):
    texturePath = path
    fileFilter = 'LouvrePlaza_'+prefix+'_'+component+'_*_s*t*_00_v*.tif'
    files = os.listdir(texturePath+'/'+component)
    goodfiles = []
    for file in files:
        if fnmatch.fnmatch(file, fileFilter):
            goodfiles.append(file)

    reads = []
    if goodfiles:
        for f in goodfiles:
            read = nuke.createNode('Read', inpanel=False)
            read['file'].setValue(path+'/'+component+'/'+f)
            reads.append(read)
    if reads:
        return reads
    else:
        nuke.message('No textures found!')
        raise UserWarning('No textures found!')

def getTextureNodes():
    values = {}
    panel = nuke.Panel('Mosaicer')
    panel.addFilenameSearch('Texture root: ', os.getenv('PWD'))
    panel.addFilenameSearch('Texture prefix: ', 'eastEntrance')
    panel.addEnumerationPulldown('Component: ', 'COL BMP SPC')
    panel.addEnumerationPulldown('Mosaic resolution: ', '512 1024 2048 2072 4096 5120 6144 7168 8192')
    panel.addSingleLineInput('Tiles number: ', '10')
    show = panel.show()
    if show:
        values['textureRoot'] = panel.value('Texture root: ')
        values['texturePrefix'] = panel.value('Texture prefix: ')
        values['component'] = panel.value('Component: ')
        values['resolution'] = panel.value('Mosaic resolution: ')
        values['tilesNumber'] = panel.value('Tiles number: ')
        values['reads'] = getTextureFiles(values['textureRoot'], values['component'], values['texturePrefix'])
        return values
    else:
        raise UserWarning('Canceld by the user.')

def mosaicer():

    values = getTextureNodes()
    
    nodes = values['reads']
    tiles = values['tilesNumber']
    prefix = values['texturePrefix']
    #resolution = getResolutionFromNodes(nodes)
    resolution = values['resolution']
    tileSize = float(resolution)/float(tiles)

    # add format
    formatN = ("mosaicFormat")
    form = ("%s %s 1 %s" % (resolution, resolution, formatN))
    nuke.addFormat(form)
    formatDict = {}
    for item in nuke.formats():
        formatDict[item.name()]=item
    nuke.Root()['format'].setValue(formatDict[formatN])
    
    # create background node
    bg = nuke.createNode('Constant', inpanel=False)
    bg['format'].setValue(formatN)

    merges = []
    deselectAll()
    for node in nodes:
        node.setSelected(True)
        filename = os.path.basename(node['file'].value())
        s, t = filename.split('_')[-3].split('s')[-1].split('t')
        # create reformat
        reformat = nuke.createNode('Reformat', inpanel=False)
        reformat['type'].setValue(1)
        reformat['box_fixed'].setValue(True)
        reformat['box_width'].setValue(tileSize)
        reformat['box_height'].setValue(tileSize)
        # create transform
        transform = nuke.createNode('Transform', inpanel=False)
        transform['center'].setValue([0, 0])
        transform['translate'].setValue([float(s)*tileSize, float(t)*tileSize])
        deselectAll()
        # create merge
        merge = nuke.createNode('Merge', inpanel=False)
        merge.setInput(1, transform)
        merge.setInput(0, bg)
        merges.append(merge)

    #deselectAll()
    #for m in merges:
    #    m.setSelected(True)
    #nuke.createNode('Merge', inpanel=False)

