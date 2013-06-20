import maya.cmds as cmds

def parseInputText(none=None):
    """ change the preview name as the user is typing """

    parseText = cmds.textFieldGrp('selecter_nameField', q=True, text=True)
    cmds.textScrollList('selecter_output', e=True, removeAll=True)
    cmds.textScrollList('selecter_output', e=True, append=cmds.ls(parseText, tr=True))
    
def closeUI(none=None):
    """ save the fields and close the ui """

    cmds.deleteUI('selecter', window=True)

def selectItem(none=None):
    item = cmds.textScrollList('selecter_output', q=True, si=True)
    cmds.select(item, replace=True)
    
def ui():
    """ batch rename main UI """

    # create ui
    windowName = 'selecter'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)
    
    cmds.window(windowName, t='Select by name')
    form = cmds.formLayout()

    # frame layout containing selection items
    frameSelection = cmds.frameLayout('selecter_frameLayoutSelection',
                            label='Items:',
                            cll=True,
                            cl=False,
                            bv=True)
    #outPane = cmds.scrollField('selecter_output', editable=False, wordWrap=False, text='')
    outPane = cmds.textScrollList('selecter_output', append=[], sii=True, ams=True, sc=selectItem)


    inputText = cmds.textFieldGrp('selecter_nameField', editable=True, l='Filter:', text='', fcc=True,cc=parseInputText, tcc=parseInputText)
    cmds.setParent('..')

    separatorBottom = cmds.separator('selecter_separatorBottom', style='in')
    closeButton = cmds.button('selecter_close', l='Close', command=closeUI)
    
    cmds.formLayout(form, e=True,
        attachControl=[(frameSelection, 'bottom', 5, separatorBottom),
                       (separatorBottom, 'bottom', 5, closeButton),
                        ])

    cmds.formLayout(form, e=True,
        attachForm=[
                    (frameSelection, 'top', 5),
                    (frameSelection, 'right', 5),
                    (frameSelection, 'left', 5),
                    (separatorBottom, 'left', 5),
                    (separatorBottom, 'right', 5),
                    (closeButton, 'left', 5),
                    (closeButton, 'right', 5),
                    (closeButton, 'bottom', 5),
                    ])
    
    cmds.showWindow(windowName)
    parseInputText()

def main():
    ui()

if __name__ == '__main__':
    main()