    """
    some custom maya settings
    TO DO:
            -hide cube
            -select handle
            -uncheck interactive creation
    """

import maya.cmds as cmds

def customSettings():
    # view cube off
    cmds.viewManip(visible=False)
    cmds.optionVar(iv = ["viewCubeShowCube", 0])

def defaultSettings():
    cmds.displayRGBColor('outlinerInvisibleColor', 0.4, 0.4, 0.4)
    # view cube on
    cmds.viewManip(visible=True)
    cmds.optionVar(iv = ["viewCubeShowCube", 1])

def customBookmarks():
    cmds.optionVar(sva = ["CustomFileDialogSidebarUrls", '/net/homes/mhavart/code/python/dmptools'])

def customScriptEditorColors():
    """
    set custom maya environment color scheme
    """
    cmds.displayRGBColor('syntaxKeywords', 0.14, 0.9, 0.14)
    cmds.displayRGBColor('syntaxText', 0.84, 0.84, 0.84)
    cmds.displayRGBColor('syntaxStrings', 0.09, 0.4, 0.1)
    cmds.displayRGBColor('syntaxComments', 0.45, 0.45, 0.45)
    cmds.displayRGBColor('syntaxCommands', 0.75, 0.75, 0.27)
    cmds.displayRGBColor('syntaxBackground', 0.15, 0.15, 0.15)

def defaultScriptEditorColors():
    """
    set the default maya environment color scheme
    """
    cmds.displayRGBColor('syntaxKeywords', 0.0, 1.0, 0.0)
    cmds.displayRGBColor('syntaxText', 0.78431373834609985, 0.78431373834609985, 0.78431373834609985)
    cmds.displayRGBColor('syntaxStrings', 1.0, 1.0, 0.0)
    cmds.displayRGBColor('syntaxComments', 1.0, 0.0, 0.0)
    cmds.displayRGBColor('syntaxCommands', 0.0, 1.0, 1.0)
    cmds.displayRGBColor('syntaxBackground', 0.16470588743686676, 0.16470588743686676, 0.16470588743686676)

def setDefaultColors():
    """
    set the default maya environment color scheme
    """

    # outliner
    cmds.displayRGBColor('outlinerInvisibleColor', 0.4, 0.4, 0.4)
    # background
    cmds.displayRGBColor('background', 0.63099998235702515, 0.63099998235702515, 0.63099998235702515)
    cmds.displayRGBColor('backgroundBottom', 0.052000001072883606, 0.052000001072883606, 0.052000001072883606)
    cmds.displayRGBColor('backgroundTop', 0.5350000262260437, 0.61699998378753662, 0.70200002193450928)

    # meshes
    cmds.displayRGBColor('lead', 0.4, 0.4, 0.4, create=True)
    cmds.displayColor('hilite', 18, active=True)
    cmds.displayColor('hiliteComponent', 9, active=True)
    cmds.displayColor('lead', 19, active=True)
    cmds.displayColor('polymesh', 16, active=True)
    cmds.displayColor('polymesh', 5, dormant=True)

def setCustomColors():
    """
    set the custom maya environment color scheme
    """
    
    # outliner
    cmds.displayRGBColor('outlinerInvisibleColor', 0.943999, 0.233173, 0.233173)
    """
    # background
    cmds.displayRGBColor('background', 0.6, 0.6, 0.6)
    cmds.displayRGBColor('backgroundBottom', 0.3, 0.3, 0.3)
    cmds.displayRGBColor('backgroundTop', 0.025, 0.025, 0.025)
    # meshes
    cmds.displayRGBColor('lead', 0.4, 0.4, 0.4, create=True)
    cmds.displayColor('hilite', 2, active=True)
    cmds.displayColor('hiliteComponent', 1, active=True)
    cmds.displayColor('lead', 3, active=True)
    cmds.displayColor('polymesh', 3, active=True)
    cmds.displayColor('polymesh', 2, dormant=True)
    """

def switchColors():
    """
    switch between color schemes
    """
    
    global switchColor
    try:
        switchColor
    except:
        switchColor = 1

    if switchColor == 1:
        headsUpDisplayMessage("custom color scheme")
        setCustomColors()
        switchColor = 0
    elif switchColor == 0:
        headsUpDisplayMessage("default color scheme")
        setDefaultColors()
        switchColor = 1

def setCustomSettings():
    customSettings()
    customBookmarks()
    customScriptEditorColors()
    setCustomColors()