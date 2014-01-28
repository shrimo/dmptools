import maya.cmds as cmds
import maya.mel as mel
import os

import dmptools.setup.items as items
reload(items)
from items import hotkeysItems as HOTKEYS_ITEMS
from dmptools.output import defaultPrint, successPrint, errorPrint

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

def showHotkeysList(dockable):
    """
    shows the current user hotkeys mapping and its name
    """       
    windowName = 'hotkeys_window'
    controlName = 'hotkeys_ctrl'
    try:    
        cmds.deleteUI(controlName, control=True)
    except:
        pass
    try:
        cmds.deleteUI(windowName, window=True)
    except:
        pass

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
    if dockable:
        closeButton = cmds.button('hotkeys_close_button',
                    label="Close",
                    c='cmds.deleteUI("'+controlName+'", control=True)')
    else:
        closeButton = cmds.button('hotkeys_close_button',
                    label="Close",
                    c='cmds.deleteUI("'+windowName+'", window=True)')
    cmds.formLayout(form, e=True,
                        attachForm=[
                                        (txt, 'top', 5),
                                        (txt, 'left', 5),
                                        (txt, 'right', 5),
                                        (closeButton, 'left', 5),
                                        (closeButton, 'right', 5),
                                        (closeButton, 'bottom', 5),
                                    ],
                        attachControl=[
                                        (txt, "bottom", 5, closeButton)
                                    ]
                    )
    if dockable:
        cmds.dockControl(controlName, label='dmptools hotkeys', floating=True, area='right', content=windowName)
    else:
        cmds.showWindow(windowName)

def executeHotkey():
    """
    action of double clicking on item
    """
    items = HOTKEYS_ITEMS
    itemName = cmds.textScrollList('hotkeysScrollList', q=True, si=True)[0].split('\t')[-1]
    command = [item['command'] for item in items if item['name'] == itemName][0]
    mel.eval(command)

def main():
    """
    create the dmptools hotkeys
    """
    defaultPrint('creating hotkeys...')

    for hotKey in HOTKEYS_ITEMS:
            setHotkey(hotKey)
    # save hotkeys pref files
    cmds.savePrefs(hotkeys=True)

if __name__ == '__main__':
    main()
