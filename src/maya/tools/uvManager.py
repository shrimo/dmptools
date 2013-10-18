from maya import cmds

def offsetUVTop(*args):
    value = float(cmds.textField('uvTileManager', text=True, q=True))
    cmds.polyEditUV(u=0, v=value)

def offsetUVBottom(*args):
    value = float(cmds.textField('uvTileManager', text=True, q=True))
    cmds.polyEditUV(u=0, v=-value)

def offsetUVLeft(*args):
    value = float(cmds.textField('uvTileManager', text=True, q=True))
    cmds.polyEditUV(u=-value, v=0)

def offsetUVRight(*args):
    value = float(cmds.textField('uvTileManager', text=True, q=True))
    cmds.polyEditUV(u=value, v=0)

def ui():
    if cmds.window('uvTileManagerWindow', exists=True):
        cmds.deleteUI('uvTileManagerWindow', window=True)
    win = cmds.window('uvTileManagerWindow', t='UV tile manager', w=180, h=180, s=False)

    mainForm = cmds.formLayout()
    #midForm = cmds.formLayout()
    # text field offset
    uvOffsetField = cmds.textField('uvTileManager', text=1)
    
    w = 40
    topButton = cmds.button(l='top', width=w, height=w, c=offsetUVTop)
    leftButton = cmds.button(l='left', width=w, height=w, c=offsetUVLeft)
    rightButton = cmds.button(l='right', width=w, height=w, c=offsetUVRight)
    bottomButton = cmds.button(l='bottom', width=w, height=w, c=offsetUVBottom)
    
    m = 50
    cmds.formLayout(mainForm, e=True,
            attachForm=[
                (topButton, 'top', 5),
                (topButton, 'right', m),
                (topButton, 'left', m),
                (leftButton, 'top', m),
                (leftButton, 'bottom', m),
                (leftButton, 'left', 5),
                (rightButton, 'right', 5),
                (rightButton, 'top', m),
                (rightButton, 'bottom', m),
                (bottomButton, 'bottom', 5),
                (bottomButton, 'right', m),
                (bottomButton, 'left', m),
                        ])
    cmds.formLayout(mainForm, e=True,
            attachControl=[
                (uvOffsetField, 'right', 5, rightButton),
                (uvOffsetField, 'left', 5, leftButton),
                (uvOffsetField, 'top', 40, topButton),
                (uvOffsetField, 'bottom', 40, bottomButton),
                    ])
                    
    cmds.showWindow(win)

def main():
    ui()