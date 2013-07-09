import maya.cmds as cmds
import fnmatch

from dmptools.settings import SettingsManager

SETTINGS = SettingsManager('batchRename')
WINDOWNAME = 'batch_rename'
CONTROLNAME = 'batch_rename_control'

def saveSettings(none=None):
    """ stuff to save """
    
    counter = cmds.textFieldGrp('rename_counter', q=True, text=True)
    padding = cmds.textFieldGrp('rename_padding', q=True, text=True)
    step = cmds.textFieldGrp('rename_step', q=True, text=True)
    name = cmds.textFieldGrp('rename_nameField', q=True, text=True)
    namePreview = cmds.textFieldGrp('rename_namePreview', q=True, text=True)
    searchfor = cmds.textFieldGrp('rename_search', q=True, text=True)
    replaceby = cmds.textFieldGrp('rename_replace', q=True, text=True)
    asset = cmds.textFieldGrp('rename_asset', q=True, text=True)
    desc = cmds.textFieldGrp('rename_desc', q=True, text=True)
    category = cmds.textFieldGrp('rename_category', q=True, text=True)

    # save
    SETTINGS.add('counter', counter)
    SETTINGS.add('padding', padding)
    SETTINGS.add('step', step)
    SETTINGS.add('name', name)
    SETTINGS.add('namePreview', namePreview)
    SETTINGS.add('searchfor', searchfor)
    SETTINGS.add('replaceby', replaceby)
    SETTINGS.add('asset', asset)
    SETTINGS.add('desc', desc)
    SETTINGS.add('category', category)

def selectItem(none=None):
    item = cmds.textScrollList('selecter_output', q=True, si=True)
    cmds.select(item, replace=True)
    
def parseFilterSelection(none=None):
    """ change the preview name as the user is typing """

    parseText = cmds.textFieldGrp('selecter_nameField', q=True, text=True)
    
    dag = cmds.checkBoxGrp('selecter_dagcheck', q=True, value1=True)
    tranform = cmds.checkBoxGrp('selecter_dagcheck', q=True, value2=True)
    shapes = cmds.checkBoxGrp('selecter_dagcheck', q=True, value3=True)

    meshType = cmds.checkBoxGrp('selecter_typecheck', q=True, value1=True)
    cameraType = cmds.checkBoxGrp('selecter_typecheck', q=True, value2=True)
    lightType = cmds.checkBoxGrp('selecter_typecheck', q=True, value3=True)
    # print parseText, '-dag:', dag, '-tranform:', tranform, '-shapes:', shapes, '-meshType:', meshType, '-cameraType:', cameraType, '-lightType:', lightType

    items = fnmatch.filter(cmds.ls(dag=True, tr=True), '*'+parseText+'*')

    if dag:
        items = fnmatch.filter(cmds.ls(dag=False), '*'+parseText+'*')      

    if tranform:
        newitems = []
        for item in items:
            if cmds.nodeType(item) == 'transform':
                newitems.append(item)
        items = newitems
    if shapes:
        newitems = []
        print items
        for item in items:
            try:
                shape = cmds.listRelatives(item, shapes=True)[0]
                newitems.append(shape)
            except:
                continue
        items = newitems
    if meshType:
        newitems = []
        for item in items:
            try:
                if cmds.nodeType(cmds.listRelatives(item, shapes=True)[0]) == 'mesh':
                    newitems.append(item)
            except:
                continue
        items = newitems
    if cameraType:
        newitems = []
        for item in items:
            try:
                if cmds.nodeType(cmds.listRelatives(item, shapes=True)[0]) == 'camera':
                    newitems.append(item)
            except:
                continue
        items = newitems
    if lightType:
        newitems = []
        for item in items:
            try:            
                if cmds.nodeType(cmds.listRelatives(item, shapes=True)[0]) == 'light':
                    newitems.append(item)
            except:
                continue
        items = newitems

    cmds.textScrollList('selecter_output', e=True, removeAll=True)
    cmds.textScrollList('selecter_output', e=True, append=items)

def removeArnoldAttr(none=None):
    selection = cmds.ls(sl=True)

    # remove attrs
    for node in selection:
        shape = cmds.listRelatives(node, shapes=True)
        try:
            cmds.deleteAttr(shape, at='rmanSassetName')
        except:
            pass
        try:
            cmds.deleteAttr(shape, at='rmanSassetDesc')
        except:
            pass
        try:
            cmds.deleteAttr(shape, at='rmanSassetCategory')
        except:
            pass

def setArnoldAttr(none=None):
    selection = cmds.ls(sl=True)
    selectionShapes = cmds.listRelatives(selection, shapes=True)

    asset = cmds.textFieldGrp('rename_asset', q=True, text=True)
    desc = cmds.textFieldGrp('rename_desc', q=True, text=True)
    category = cmds.textFieldGrp('rename_category', q=True, text=True)

    # remove attrs
    for node in selection:
        shape = cmds.listRelatives(node, shapes=True)
        try:
            cmds.deleteAttr(shape, at='rmanSassetName')
        except:
            pass
        try:
            cmds.deleteAttr(shape, at='rmanSassetDesc')
        except:
            pass
        try:
            cmds.deleteAttr(shape, at='rmanSassetCategory')
        except:
            pass

    # add attr
    for sel in selectionShapes:
        # asset attribute
        attrname = 'rmanSassetName'
        selAttr = sel+'.'+attrname
        cmds.addAttr(sel, ln=attrname, nn='Rman Sasset Name', dt='string')
        cmds.setAttr(selAttr, asset, type='string')
        cmds.setAttr(selAttr, e=True, keyable=True)
        
        # desc attribute
        attrname = 'rmanSassetDesc'
        selAttr = sel+'.'+attrname
        cmds.addAttr(sel, ln=attrname, nn='Rman Sasset Desc', dt='string')
        cmds.setAttr(selAttr, desc, type='string')
        cmds.setAttr(selAttr, e=True, keyable=True)
            
        # category attribute
        attrname = 'rmanSassetCategory'
        selAttr = sel+'.'+attrname
        cmds.addAttr(sel, ln=attrname, nn='Rman Sasset Category', dt='string')
        cmds.setAttr(selAttr, category, type='string')
        cmds.setAttr(selAttr, e=True, keyable=True)

    saveSettings()
    
def parseInputText(none=None):
    """ change the preview name as the user is typing """

    counter = int(cmds.textFieldGrp('rename_counter', q=True, text=True))
    padding = int(cmds.textFieldGrp('rename_padding', q=True, text=True))
    step = int(cmds.textFieldGrp('rename_step', q=True, text=True))
    parseText = cmds.textFieldGrp('rename_nameField', q=True, text=True)
    if '[C]' in parseText:
        outText = parseText.replace('[C]', str(counter).rjust(padding, '0'))
    else:
        outText = parseText

    # set preview field   
    cmds.textFieldGrp('rename_namePreview', e=True, text=outText)
    
    return outText

def renameItems(none=None):
    """ rename the items in selection """

    counter = int(cmds.textFieldGrp('rename_counter', q=True, text=True))
    padding = int(cmds.textFieldGrp('rename_padding', q=True, text=True))
    step = int(cmds.textFieldGrp('rename_step', q=True, text=True))
    parseText = cmds.textFieldGrp('rename_nameField', q=True, text=True)
    i = counter
    for node in cmds.ls(sl=True):
        if '[C]' in parseText:
            newname = parseText.replace('[C]', str(i).rjust(padding, '0'))
            cmds.rename(node, newname)
        else:
            cmds.warning('counter not found! please insert a [C] in the new name field')
        i += step

    saveSettings()
   
def searchReplace(none=None):
    """ search and replace the items in selection """

    searchfor = cmds.textFieldGrp('rename_search', q=True, text=True)
    replaceby = cmds.textFieldGrp('rename_replace', q=True, text=True)
    for node in cmds.ls(sl=True):
        try:
            newname = node.replace(searchfor, replaceby)
            cmds.rename(node, newname)
        except:
            print 'failed to rename', node
    saveSettings()

def closeUI(none=None):
    """ save the fields and close the ui """

    saveSettings()
    try:
        cmds.deleteUI(CONTROLNAME, control=True)
    except:
        pass
    try:
        cmds.deleteUI(WINDOWNAME, window=True)
    except:
        pass

def ui(dockable):
    """ batch rename main UI """

    # get settings
    counter = SETTINGS.get('counter')
    if not 'counter' in locals():
        counter = '1'
    padding = SETTINGS.get('padding')
    if not 'padding' in locals():
        padding = '2'
    step = SETTINGS.get('step')
    if not 'step' in locals():
        step = '1'
    name = SETTINGS.get('name')
    if not 'name' in locals():
        name = 'example_[C]_GEP'
    namePreview = SETTINGS.get('namePreview')
    if not 'namePreview' in locals():
        namePreview = ''
    searchfor = SETTINGS.get('searchfor')
    if not 'searchfor' in locals():
        searchfor = ''
    replaceby = SETTINGS.get('replaceby')
    if not 'replaceby' in locals():
        replaceby = ''
    asset = SETTINGS.get('asset')
    if not 'asset' in locals():
        asset = 'LouvreVisitorsCenter'
    desc = SETTINGS.get('desc')
    if not 'desc' in locals():
        desc = 'lidar'
    category = SETTINGS.get('category')
    if not 'category' in locals():
        category = 'set'

    # create ui
    try:
        cmds.deleteUI(windowName, window=True)
    except:
        pass
    try:
        cmds.deleteUI(controlName, control=True)
    except:
        pass

    myWindow = cmds.window(windowName, t='Batch rename selection')
    form = cmds.formLayout(parent=myWindow)

    # rename with counter frame layout
    frameRename = cmds.frameLayout('rename_frameLayoutRename',
                            label='Rename',
                            cll=True,
                            cl=True,
                            bv=True)

    separator = cmds.separator('rename_separator', style='in')
    coubterInput = cmds.textFieldGrp('rename_counter', editable=True, l='Counter start', text=counter, fcc=True, cc=parseInputText, tcc=parseInputText)
    stepInput = cmds.textFieldGrp('rename_step', editable=True, l='Step', text=step, fcc=True, cc=parseInputText, tcc=parseInputText)
    paddingInput = cmds.textFieldGrp('rename_padding', editable=True, l='Padding', text=padding, fcc=True, cc=parseInputText, tcc=parseInputText)

    inputText = cmds.textFieldGrp('rename_nameField', editable=True, l='New name', text=name, fcc=True,cc=parseInputText, tcc=parseInputText)
    inputText = cmds.textFieldGrp('rename_namePreview', editable=False, l='Preview', text='')

    renameButton = cmds.button('rename_button', l='Rename', command=renameItems)
    cmds.setParent('..')


    # Search and replace frame layout
    frameReplace = cmds.frameLayout('rename_frameLayoutReplace',
                            label='Search & Replace',
                            cll=True,
                            cl=True,
                            bv=True)
    separator = cmds.separator('rename_separator', style='in')                            
    searchInput = cmds.textFieldGrp('rename_search', editable=True, l='Search for', text=searchfor)
    replaceInput = cmds.textFieldGrp('rename_replace', editable=True, l='Replace by', text=replaceby)
    
    renameButton = cmds.button('rename_replacebutton', l='Search and Replace', command=searchReplace)
    cmds.setParent('..')

    # add attributes frame layout
    frameAttr = cmds.frameLayout('rename_frameLayoutAttr',
                            label='Add attributes',
                            cll=True,
                            cl=True,
                            bv=True)
    separator = cmds.separator('rename_separator', style='in')

    assetField = cmds.textFieldGrp('rename_asset', editable=True, l='asset', text=asset)
    descField = cmds.textFieldGrp('rename_desc', editable=True, l='desc', text=desc)
    categoryField = cmds.textFieldGrp('rename_category', editable=True, l='category', text=category)
    
    addAttrButton = cmds.button('rename_setattrbutton', l='Add attributes', command=setArnoldAttr)
    removeAttrButton = cmds.button('rename_removeattrbutton', l='Remove attributes', command=removeArnoldAttr)
    cmds.setParent('..')

    # frame layout containing selection items
    frameSelection = cmds.frameLayout('selecter_frameLayoutSelection',
                            label='Item Selecter',
                            cll=True,
                            cl=True,
                            bv=True)
    #outPane = cmds.scrollField('selecter_output', editable=False, wordWrap=False, text='')
    outPane = cmds.textScrollList('selecter_output', append=[], sii=True, ams=True, sc=selectItem)
    inputText = cmds.textFieldGrp('selecter_nameField', editable=True, l='Filter:', text='', fcc=True, cc=parseFilterSelection, tcc=parseFilterSelection)
    nodeCheckbox = cmds.checkBoxGrp('selecter_dagcheck', numberOfCheckBoxes=3, labelArray3=['Dag objects', 'Transforms', 'Shapes'], cc=parseFilterSelection)
    typeCheckbox = cmds.checkBoxGrp('selecter_typecheck', numberOfCheckBoxes=3, labelArray3=['Meshes', 'Cameras', 'Lights'], cc=parseFilterSelection)

    cmds.setParent('..')

    separatorBottom = cmds.separator('rename_separatorBottom', style='in')
    closeButton = cmds.button('rename_close', l='Close', command=closeUI)
    
    cmds.formLayout(form, e=True,
        attachControl=[(frameReplace, 'top', 5, frameRename),
                        (frameAttr, 'top', 5, frameReplace),
                        (frameSelection, 'top', 5, frameAttr),
                        (frameSelection, 'bottom', 5, separatorBottom),
                        (separatorBottom, 'bottom', 5, closeButton),
                        ])

    cmds.formLayout(form, e=True,
        attachForm=[(frameRename, 'right', 5),
                    (frameRename, 'left', 5),
                    (frameRename, 'top', 5),
                    (frameReplace, 'left', 5),
                    (frameReplace, 'right', 5),
                    (frameAttr, 'left', 5),
                    (frameAttr, 'right', 5),
                    (frameSelection, 'left', 5),
                    (frameSelection, 'right', 5),
                    (separatorBottom, 'left', 5),
                    (separatorBottom, 'right', 5),
                    (closeButton, 'left', 5),
                    (closeButton, 'right', 5),
                    (closeButton, 'bottom', 5),
                    ])
    
    
    parseInputText()
    parseFilterSelection()
    
    if dockable:
        cmds.dockControl(controlName, label='Batch rename', floating=True, area='right', content=windowName)
    else:
        cmds.showWindow(windowName)

def main():
    ui(dockable=True)

if __name__ == '__main__':
    main()