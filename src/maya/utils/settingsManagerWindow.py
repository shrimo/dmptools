from maya import cmds, mel

from dmptools.settings import SettingsManager

def buildUI(settingsName):
    settings = SETTINGS.getAll()
    # create ui
    if cmds.window(settingsName, exists=True):
        cmds.deleteUI(settingsName, window=True)
    settingsWindow = cmds.window(settingsName,
                        t='dmptools | '+settingsName+' Settings',
                        w=100,
                        h=50)
    cmds.columnLayout(adj=True)
    for setting in settings:
        cmds.textFieldGrp(str(setting.keys()[0])+'_txtfield',
                        label=str(setting.keys()[0]).replace('_', ' '),
                        text=str(setting.values()[0]),
                        editable=True,
                        cc=updateSettings)

    cmds.showWindow(settingsWindow)

def updateSettings(*argv):
    for setting in SETTINGS.getAll():
        newValue = cmds.textFieldGrp(str(setting.keys()[0])+'_txtfield', text=True, q=True)
        SETTINGS.add(setting.keys()[0], newValue)

def main(name=''):
    global SETTINGS
    global settingsName
    settingsName = name
    SETTINGS = SettingsManager(settingsName)
    buildUI(settingsName)