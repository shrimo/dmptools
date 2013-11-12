import nuke
import os

def executeScript():
    node = nuke.thisNode()
    script = node['input_script'].getValue()
    scriptpath = "/tmp/nuke_scripnode_tmp.py"
    with open(scriptpath, 'w') as FILE:
        FILE.write(script)
    execfile(scriptpath)

def scriptNode():
    # create empty node
    scriptNode = nuke.createNode('NoOp')
    scriptNode.setName('scriptNode')
    scriptNode['hide_input'].setValue(True)
    # create custom text field knob
    textKnob = nuke.Multiline_Eval_String_Knob('input_script', 'Script')
    # create execute button
    executeButton = nuke.PyScript_Knob('execute_script', 'Execute')
    cmd = "import dmptools.nodes.scriptNode as scriptNode;reload(scriptNode);scriptNode.executeScript()"
    executeButton.setCommand(cmd)
    # add the knobs to the node
    scriptNode.addKnob(textKnob)
    scriptNode.addKnob(executeButton)

def main():
    scriptNode()

if __name__ == '__main__':
    main()
