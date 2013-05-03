import nuke
import nukescripts

class PrintPath(nukescripts.PythonPanel):
    """panel of the printPath tool"""
    def __init__(self):
        self.reads = nuke.selectedNodes('Read')
        
        if len(self.reads) == 0:
            self.reads = nuke.allNodes('Read')
        nukescripts.PythonPanel.__init__( self, 'PrintPath', 'printpath')
       
        self.textKnob = nuke.Multiline_Eval_String_Knob('Paths:')

        readList = []
        for read in self.reads:
            readList.append(read.name()+": "+read['file'].value())

        readStr = "\n".join(readList)

        self.textKnob.setValue(readStr)   
        self.refreshButton = nuke.PyScript_Knob('refresh')
        self.addKnob(self.textKnob)
        self.addKnob(self.refreshButton)

    def knobChanged(self, knob):
        if knob == self.refreshButton:
            reads = nuke.selectedNodes('Read')
            if len(reads) == 0:
                reads = nuke.allNodes('Read')
                
            readList = []
            for read in reads:
                readList.append(read.name()+": "+read['file'].value())
            readStr = "\n".join(readList)
            
            self.textKnob.setValue(readStr)
            
def printPath():
    """return a panel with the path of the selected nodes"""
    nukescripts.registerPanel( 'printpath', printPath)
    PrintPath().show()