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
        ctl = hotkey['ctrl']
        alt = hotkey['alt']
        command = hotkey['command']
        release = hotkey['release']
        shift = True if key[0].isupper() else False
        #appendName = 'key:  '+str(key)+'\tctrl:  '+str(ctl)+'\talt:  '+str(alt)+'\t'+str(name)
        namePart1 = 'key:  '+str(key)+['\tctrl' if ctl else '\t'][0]+['\talt' if alt else '\t'][0]+['\tshift' if shift else '\t'][0]
        appendName = namePart1+'\t'+str(name)
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
        create the dmptools hotkeys
    """
    print '- creating dmptools hotkeys...'

    for hotKey in HOTKEYS_ITEMS:
            setHotkey(hotKey)
    # save hotkeys pref files
    cmds.savePrefs(hotkeys=True)
    print '> done.'

if __name__ == '__main__':
    main()
