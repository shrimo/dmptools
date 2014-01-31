from maya import cmds, mel

from dmptools.settings import SettingsManager

def buildUI():
    """
    build a window containing all the settings from the dmptools module
    """
    S = SettingsManager('maya_main')
    mainSettings = [setting for setting in S.getAllSettingsFiles() if 'maya' in setting]
    mainSettings.remove('maya_main')

    windowName = 'dmptools_settings_window'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)

    settingsWindow = cmds.window(windowName,
                        t='dmptools settings',
                        w=220,
                        h=120)

    form = cmds.formLayout()
    scrollLayout = cmds.scrollLayout(cr=True)

    for mainSetting in mainSettings:
        cmds.frameLayout(mainSetting+'settings_frmLayout',
                            label=mainSetting.replace('maya_', '').replace('_', ' '),
                            cll=True,
                            cl=True,
                            bv=False,
                            annotation='Settings for '+mainSetting.replace('maya_', '').replace('_', ' '))

        # creating attibutes based on type of value
        settings = SettingsManager(mainSetting).getAll()
        for setting in settings:
            if type(setting.values()[0]).__name__ in ['str', 'unicode']:
                strAttribute(mainSetting, setting)
            if type(setting.values()[0]).__name__ == 'float':
                floatAttribute(mainSetting, setting)
            if type(setting.values()[0]).__name__ == 'int':
                floatAttribute(mainSetting, setting)
            if type(setting.values()[0]).__name__ == 'bool':
                boolAttribute(mainSetting, setting)
            if type(setting.values()[0]).__name__ in ['list', 'tuple']:
                strAttribute(mainSetting, setting)

        cmds.setParent('..')

    cmds.setParent('..')
    closeButton = cmds.button(windowName+'_close_button',
                    label="Close",
                    c='import maya.cmds as cmds;cmds.deleteUI("'+windowName+'", window=True)')
    cmds.setParent('..')

    cmds.formLayout(form, e=True,
                    attachForm=[
                                    (scrollLayout, 'top', 5),
                                    (scrollLayout, 'left', 5),
                                    (scrollLayout, 'right', 5),
                                    (closeButton, 'left', 5),
                                    (closeButton, 'right', 5),
                                    (closeButton, 'bottom', 5),
                                ],
                    attachControl=[
                                    (scrollLayout, "bottom", 5, closeButton)
                                ]
                )

    cmds.showWindow(windowName)

def strAttribute(mainSetting, setting):
    cmds.textFieldGrp(str(setting.keys()[0])+'_attribute',
                    label=str(setting.keys()[0]).replace('_', ' '),
                    text=str(setting.values()[0]),
                    editable=True,
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateStrAttr('"+mainSetting+"')"
                    )

def updateStrAttr(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.textFieldGrp(str(setting.keys()[0])+'_attribute', text=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def floatAttribute(mainSetting, setting):
    cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateFloatAttr('"+mainSetting+"')"
                    )

def updateFloatAttr(setting):
    SETTINGS = SettingsManager(setting)
    for setting in SETTINGS.getAll():
        newValue = cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue[0])

def intAttribute(mainSetting, setting):
    cmds.intFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateIntAttr('"+mainSetting+"')"
                    )

def updateIntAttr(*argv):
    SETTINGS = SettingsManager(settingsName)
    for setting in SETTINGS.getAll():
        newValue = cmds.intFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def boolAttribute(mainSetting, setting):
    cmds.checkBoxGrp(str(setting.keys()[0])+'_attribute',
                        numberOfCheckBoxes=1,
                        label=str(setting.keys()[0]).replace('_', ' '),
                        v1=setting.values()[0],
                        cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateBoolAttribute('"+mainSetting+"')"
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