from maya import cmds, mel

from dmptools.settings import SettingsManager

def buildUI(settingsName):
    S = SettingsManager(settingsName)
    settings = S.getAll()
    # create ui
    if cmds.window(settingsName, exists=True):
        cmds.deleteUI(settingsName, window=True)
    settingsWindow = cmds.window(settingsName,
                        t='dmptools | '+settingsName+' Settings',
                        w=80,
                        h=60)

    form = cmds.formLayout()
    #colLayout = cmds.columnLayout(adj=True, columnAttach=('both', 5))
    colLayout = cmds.scrollLayout(cr=True)

    # creating attibutes based on type of value
    for setting in settings:
        if type(setting.values()[0]).__name__ in ['str', 'unicode']:
            strAttribute(setting)
        if type(setting.values()[0]).__name__ == 'float':
            floatAttribute(setting)
        if type(setting.values()[0]).__name__ == 'int':
            floatAttribute(setting)
        if type(setting.values()[0]).__name__ == 'bool':
            boolAttribute(setting)
        if type(setting.values()[0]).__name__ in ['list', 'tuple']:
            strAttribute(setting)

    cmds.setParent('..')
    closeButton = cmds.button(settingsName+'_close_button',
                    label="Close",
                    c='import maya.cmds as cmds;cmds.deleteUI("'+settingsWindow+'", window=True)')

    cmds.formLayout(form, e=True,
                    attachForm=[
                                    (colLayout, 'top', 5),
                                    (colLayout, 'left', 5),
                                    (colLayout, 'right', 5),
                                    (closeButton, 'left', 5),
                                    (closeButton, 'right', 5),
                                    (closeButton, 'bottom', 5),
                                ],
                    attachControl=[
                                    (colLayout, "bottom", 5, closeButton)
                                ]
                )

    # displays the window
    cmds.showWindow(settingsWindow)

def strAttribute(setting):
    cmds.textFieldGrp(str(setting.keys()[0])+'_attribute',
                    label=str(setting.keys()[0]).replace('_', ' '),
                    text=str(setting.values()[0]),
                    editable=True,
                    cc=updateStrAttr
                    )

def updateStrAttr(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.textFieldGrp(str(setting.keys()[0])+'_attribute', text=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def floatAttribute(setting):
    cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc=updateFloatAttr
                    )

def updateFloatAttr(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue[0])

def intAttribute(setting):
    cmds.intFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc=updateIntAttr
                    )

def updateIntAttr(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.intFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def boolAttribute(setting):
    cmds.checkBoxGrp(str(setting.keys()[0])+'_attribute',
                        numberOfCheckBoxes=1,
                        label=str(setting.keys()[0]).replace('_', ' '),
                        v1=setting.values()[0],
                        cc=updateBoolAttribute
                        )

def updateBoolAttribute(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.checkBoxGrp(str(setting.keys()[0])+'_attribute', value1=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def main(name):
    global SETTINGS
    global settingsName
    settingsName = name
    SETTINGS = SettingsManager(settingsName)
    buildUI(settingsName)