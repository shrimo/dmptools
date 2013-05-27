"""
    run a shell command from nuke
"""

import subprocess

import nuke
import nukescripts
from threading import Thread

class RunCommand(nukescripts.PythonPanel, Thread):
    def __init__(self):        
        nukescripts.PythonPanel.__init__( self, 'RunCommand', 'RunCommand')
        Thread.__init__(self)

        knobs = []
    
        self.header = nuke.Text_Knob('header', '', "Run a shell command from nuke.")
        self.output = nuke.Multiline_Eval_String_Knob('output', '')
        # self.output.setEnabled(False)   
        self.input = nuke.String_Knob('input', '', '')

        knobs.append(self.output)
        knobs.append(self.input)
        for knob in knobs:
            self.addKnob(knob)
        
    def knobChanged(self, knob):
        if knob == self.input:
            # get the input value
            value = self.input.getValue()
            # run the command
            popObj = subprocess.Popen(value, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = popObj.communicate()
            # show the output
            self.output.setValue(out[0])
            self.input.setValue('')

