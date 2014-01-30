from maya import cmds

def overrideColor():
    colorIndex = cmds.palettePort('dmptools_display_color', setCurCell=True, q=True)
    for node in cmds.ls(sl=True):
        nodeShape = cmds.listRelatives(node, shapes=True)[0]
        
        cmds.setAttr(nodeShape+".overrideEnabled", True)
        cmds.setAttr(nodeShape+".overrideColor", colorIndex)

def ui():
    windowName = 'dmptools_display_color_window'
    try:
        cmds.deleteUI(windowName, window=True)
    except:
        pass

    cmds.window(windowName, title="Display Color Override", rtf=True, sizeable=False)        
    colLayout = cmds.columnLayout(adj=True)
    
    columns = 16
    rows = 2
    cell_width = 17
    cell_height = 17
    color_palette = cmds.palettePort('dmptools_display_color',
                                    dimensions=(columns, rows), 
                                    transparent=0,
                                    width=(columns*cell_width),
                                    height=(rows*cell_width),
                                    topDown=True,
                                    colorEditable=False,
                                    cc=overrideColor)
        
    for index in range(1, 32):
        color_component = cmds.colorIndex(index, q=True)
        cmds.palettePort(color_palette,
                         edit=True,
                         rgbValue=(index, color_component[0], color_component[1], color_component[2]))
        
    cmds.palettePort(color_palette,
                   edit=True,
                   rgbValue=(0, 0.6, 0.6, 0.6))

    cmds.showWindow(windowName)

def main():
    ui()