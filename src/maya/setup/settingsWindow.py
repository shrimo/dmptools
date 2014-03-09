from maya import cmds, mel

from dmptools.settings import SettingsManager

WINDOWNAME = 'dmptools_settings_window'

def buildUI():
    """
    build a window containing all the settings from the dmptools module
    """
    S = SettingsManager('maya_main')
    mainSettings = [setting for setting in S.getAllSettingsFiles() if 'maya' in setting]
    mainSettings.remove('maya_main')

    if cmds.window(WINDOWNAME, exists=True):
        cmds.deleteUI(WINDOWNAME, window=True)

    settingsWindow = cmds.window(WINDOWNAME,
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
    closeButton = cmds.button(WINDOWNAME+'_close_button',
                    label="Close",
                    c='import maya.cmds as cmds;cmds.deleteUI("'+WINDOWNAME+'", window=True)')
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

    cmds.showWindow(WINDOWNAME)

def strAttribute(mainSetting, setting):
    cmds.textFieldGrp(str(setting.keys()[0])+'_attribute',
                    label=str(setting.keys()[0]).replace('_', ' '),
                    text=str(setting.values()[0]),
                    editable=True,
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateStrAttr('"+mainSetting+"')"
                    )

def updateStrAttr(mainSetting):
    SETTINGS = SettingsManager(mainSetting)
    for setting in SETTINGS.getAll():
        try:
            newValue = cmds.textFieldGrp(str(setting.keys()[0])+'_attribute', text=True, q=True)
            SETTINGS.add(setting.keys()[0], newValue)
        except:
            pass
            
def floatAttribute(mainSetting, setting):
    cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateFloatAttr('"+mainSetting+"')"
                    )

def updateFloatAttr(mainSetting):
    SETTINGS = SettingsManager(mainSetting)
    for setting in SETTINGS.getAll():
        try:
            newValue = cmds.floatFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
            SETTINGS.add(setting.keys()[0], newValue[0])
        except:
            pass

def intAttribute(mainSetting, setting):
    cmds.intFieldGrp(str(setting.keys()[0])+'_attribute',
                    numberOfFields=1,
                    label=str(setting.keys()[0]).replace('_', ' '),
                    value1=setting.values()[0],
                    cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateIntAttr('"+mainSetting+"')"
                    )

def updateIntAttr(mainSetting):
    SETTINGS = SettingsManager(mainSetting)
    for setting in SETTINGS.getAll():
        try:
            newValue = cmds.intFieldGrp(str(setting.keys()[0])+'_attribute', value=True, q=True)
            SETTINGS.add(setting.keys()[0], newValue)
        except:
            pass

def boolAttribute(mainSetting, setting):
    cmds.checkBoxGrp(str(setting.keys()[0])+'_attribute',
                        numberOfCheckBoxes=1,
                        label=str(setting.keys()[0]).replace('_', ' '),
                        v1=setting.values()[0],
                        cc="import dmptools.setup.settingsWindow as settingsWindow;settingsWindow.updateBoolAttribute('"+mainSetting+"')"
                        )

def updateBoolAttribute(mainSetting):
    SETTINGS = SettingsManager(mainSetting)
    for setting in SETTINGS.getAll():
        try:
            newValue = cmds.checkBoxGrp(str(setting.keys()[0])+'_attribute', value1=True, q=True)
            SETTINGS.add(setting.keys()[0], newValue)
        except:
            pass

def main(name):
    global SETTINGS
    global settingsName
    settingsName = name
    SETTINGS = SettingsManager(settingsName)
    buildUI(settingsName)