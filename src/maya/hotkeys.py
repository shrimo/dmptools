#==========================================================================
#
# createHotkeys.py
# michael.havart@gmail.com
#
# create Maya hotkeys instead of typing them in the maya hotkey menu.
#
#==========================================================================

import maya.cmds as cmds
import maya.mel as mel
import os

import dmptools.items as items

# hotkeys files path
CMD_FILE = cmds.internalVar(userPrefDir=True)+'userRunTimeCommands.mel'
HOTKEY_FILE = cmds.internalVar(userPrefDir=True)+'userHotkeys.mel'
COMMAND_NAME_FILE = cmds.internalVar(userPrefDir=True)+'userNamedCommands.mel'
HOTKEYS_ITEMS = items.hotkeysItems

def setHotkey(hotkey):
    """
    create a hotkey from a given hotkey dict
    """
    # get hotkey dict data
    name = hotkey['name']
    key = hotkey['key']
    alt = hotkey['alt']
    ctl = hotkey['ctrl']
    release = hotkey['release']
    command = hotkey['command']
    if release:
        releaseName = name+"Release"
        releaseCommand = hotkey['releaseCommand']
    
    #create hotkey command
    cmds.nameCommand(name, sourceType="mel", annotation=name, command=command)
    if release:
        cmds.nameCommand(releaseName, sourceType="mel", annotation=releaseName, command=releaseCommand)
    
    # set hotkey
    cmds.hotkey(k=key, alt=alt, ctl=ctl, name=name)    
    if release:
        cmds.hotkey(k=key, alt=alt, ctl=ctl, releaseName=releaseName)

def showHotkeysList():
    """shows the current user hotkeys mapping and its name
    """       
    windowName = 'hotkeysWindow'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)

    cmds.window(windowName, title='dmptools hotkeys list')
    form = cmds.formLayout()
    txt = cmds.textScrollList('hotkeysScrollList')
    for hotkey in HOTKEYS_ITEMS:
        name = hotkey['name']
        key = hotkey['key']
        alt = hotkey['alt']
        ctl = hotkey['ctrl']
        release = hotkey['release']
        command = hotkey['command']
        appendName = 'key:  '+str(key)+'\tctrl:  '+str(ctl)+'\talt:  '+str(alt)+'\t'+str(name)
        cmds.textScrollList('hotkeysScrollList', e=True, append=appendName, dcc=executeHotkey, ann='double click to execute the command')

    cmds.formLayout(form, e=True, attachForm = [(txt, 'top', 5),(txt, 'bottom', 5), (txt, 'left', 5), (txt, 'right', 5)])
    cmds.showWindow(windowName)

def executeHotkey():
    items = HOTKEYS_ITEMS
    itemName = cmds.textScrollList('hotkeysScrollList', q=True, si=True)[0].split('\t')[-1]
    command = [item['command'] for item in items if item['name'] == itemName][0]
    print command
    mel.eval(command)

def main():
    """
        delete the old maya hotkey files
        and install the new ones from the HOTKEYS list
    """
    print '- creating dmptools hotkeys...'
    # delete old hotkeys
    if os.path.exists(CMD_FILE):
        os.remove(CMD_FILE)
    if os.path.exists(HOTKEY_FILE):
        os.remove(HOTKEY_FILE)
    if os.path.exists(COMMAND_NAME_FILE):
        os.remove(COMMAND_NAME_FILE)
    # create hotkeys
    for hotKey in HOTKEYS_ITEMS:
            setHotkey(hotKey)
    # save hotkeys pref files
    cmds.savePrefs(hotkeys=True)
    print '> done.'

if __name__ == '__main__':
    main()
