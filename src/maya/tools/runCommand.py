import subprocess

import maya.cmds as cmds

def run(value):
    value = cmds.scrollField('runCommandInput', q=True, text=True)
    command = value.split()
    popObj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = popObj.communicate()
    cmds.scrollField('runCommandOutput', e=True, text=out[0])
    cmds.scrollField('runCommandInput', e=True, cl=True)
    cmds.scrollField('runCommandInput', e=True, ip=1)

def ui():
    
    windowName = 'runCommand'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)
    
    cmds.window(windowName, t='run a command')
    form = cmds.formLayout()
    hPane = cmds.paneLayout(configuration='horizontal2', )
    cmds.scrollField('runCommandInput', editable=True, wordWrap=False, h=3, text='', ec=run)
    cmds.scrollField('runCommandOutput', editable=False, wordWrap=False, text='Output')
    #cmds. button(label='run')   
    cmds.formLayout(form, e=True, attachForm=[(hPane, 'top', 5), (hPane, 'bottom', 5), (hPane, 'left', 5), (hPane, 'right', 5)])
    
    cmds.showWindow(windowName)
    
def main():
    ui()

if __name__ == '__main__':
    main()