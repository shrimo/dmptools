import subprocess

import maya.cmds as cmds

def run(value=None):
    # get the value from the textfield 
    value = cmds.textField('runCmd_input', q=True, text=True)

    # execute the command and whow the output if the checkbox is checked
    if cmds.checkBox('runCmd_chkbx', q=True, value=True):
        popObj = subprocess.Popen(value, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = popObj.communicate()
        # ouptut the result in the window
        cmds.scrollField('runCmd_output', e=True, text=out[0])
    else:
        subprocess.Popen(value, shell=True)
    # clear the input field
    cmds.textField('runCmd_input', e=True, text='')

def ui():
    """
        run command main UI
    """
    windowName = 'runCommand'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)
    
    cmds.window(windowName, t='run a command')
    form = cmds.formLayout()
    inputText = cmds.textField('runCmd_input', editable=True, text='', enterCommand=run, changeCommand=run)
    checkBox = cmds.checkBox('runCmd_chkbx', value=True, label='output')
    separator = cmds.separator('runCmd_separator', style='in')
    outPane = cmds.scrollField('runCmd_output', editable=False, wordWrap=False, text='')

    cmds.formLayout(form, e=True,
        attachControl=[(outPane, 'bottom', 5, separator),
                    (inputText, 'right', 5, checkBox),
                    (separator, 'bottom', 5, inputText)
                        ])

    cmds.formLayout(form, e=True,
        attachForm=[(outPane, 'top', 5),
                    (outPane, 'left', 5),
                    (outPane, 'right', 5)])

    cmds.formLayout(form, e=True,
        attachForm=[(inputText, 'left', 5),
                    (inputText, 'bottom', 5)
                    ])

    cmds.formLayout(form, e=True,
        attachForm=[(checkBox, 'bottom', 5),
                    (checkBox, 'right', 5)])
    
    cmds.showWindow(windowName)
    
def main():
    ui()

if __name__ == '__main__':
    main()