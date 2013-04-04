#==========================================================================
#
# createHotkeys.py
# michael.havart@gmail.com
#
# create Maya hotkeys instead of typing them in the maya hotkey menu.
#
#==========================================================================

import maya.cmds as cmds
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
    #print 'set hotkey:', name, key, alt, ctrl, command

    if release:
        cmds.hotkey(k=key, alt=alt, ctl=ctl, releaseName=releaseName)
        #print 'set hotkey release:', releaseName, key, alt, ctrl, releaseCommand

def showHotkeysList():
    """shows the current user hotkeys mapping and its name
    """

    reload(items)
    lines = []
    for key in HOTKEYS_ITEMS:
        lines.append('key:  '+str(key['key'])+'  ctrl:  '+str(key['ctrl'])+'  alt:  '+str(key['alt'])+'  '+str(key['name']))

    window = cmds.window('hotkeysWindow')
    cmds.paneLayout()
    cmds.textScrollList(numberOfRows=8,
                        allowMultiSelection=True,
                        append=lines,)
    cmds.showWindow()

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
