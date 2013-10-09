import nuke
import os

def scriptNode():

    scriptNode = nuke.createNode('NoOp')
    scriptNode.setName('scriptNode')
    textKnob = nuke.Multiline_Eval_String_Knob('script', 'script')
    executeButton = nuke.PyScript_Knob('Execute script', 'execute')
    cmd = "print nuke.thisNode()['script'].getValue();eval(nuke.thisNode()['script'].getValue())"
    executeButton.setCommand(cmd)

    scriptNode.addKnob(textKnob)
    scriptNode.addKnob(executeButton)

def main():
    scriptNode()

if __name__ == '__main__':
    main()