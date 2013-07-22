import nuke
import os

def texTab():
    """ add a tex convert tab on write nodes """
    # get node
    node = nuke.thisNode()
    # add command in the after frame render field
    node.knob('afterFrameRender').setValue('import dmptools.utils.nukeCommands as nc;reload(nc);nc.texConvert()')

    # create knobs
    tab = nuke.Tab_Knob("texConvertTab","Tex Convert")

    checkBox = nuke.Boolean_Knob("texConvertCheckbox","Do Convertion")
    checkBox.setValue(False)
    sMode = nuke.Enumeration_Knob("sMode","sMode",['black','periodic','clamp'])
    tMode = nuke.Enumeration_Knob("tMode","tMode",['black','periodic','clamp'])
    resizeMenu = nuke.Enumeration_Knob("resize","resize",['up-', 'up','down-','down', 'round-', 'round', 'none'])
    filterMenu = nuke.Enumeration_Knob("filter","filter",['box',
        'point', 'triangle', 'sinc', 'gaussian', 'gaussian-soft', 'catmull-rom', 'mitchell', 'cubic', 'lanczos', 'bessel', 'blackman-harris'])
    otherFlags = nuke.EvalString_Knob('otherFlags', 'Other Flags', '')
    separator = nuke.Text_Knob('none', '')
    showTex = nuke.PyScript_Knob('showTex', 'show tex')
    showTex.setCommand('import dmptools.utils.nukeCommands as nc;reload(nc);nc.showTex()')
    texInfo = nuke.PyScript_Knob('texInfo', 'tex info')
    texInfo.setCommand('import dmptools.utils.nukeCommands as nc;reload(nc);nc.texInfo()')

    # add knobs
    node.addKnob(tab)
    node.addKnob(checkBox)
    node.addKnob(sMode)
    node.addKnob(tMode)
    node.addKnob(resizeMenu)
    node.addKnob(filterMenu)
    node.addKnob(otherFlags)
    node.addKnob(separator)
    node.addKnob(showTex)
    node.addKnob(texInfo)

    # set the focus on the first tab of the node
    node.knob('file').setFlag(True)

def showTex():
    """ show the associated tex file from a file knob """
    node = nuke.thisNode()
    filename = node['file'].getEvaluatedValue().replace('exr', 'tex')
    if filename and os.path.exists(filename):
        command = 'sho '+filename
        popObj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        print 'no file found...'

def texInfo():
    """ show the associated tex info from a file knob """
    node = nuke.thisNode()
    filename = node['file'].getEvaluatedValue().replace('exr', 'tex')
    if filename and os.path.exists(filename):
        command = 'txinfo '+filename
        popObj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = popObj.communicate()
        print out[0]
        nuke.message(out[0])
    else:
        print 'no file found...'

def texConvert():
    """ converts an exr to tex """
    node = nuke.thisNode()
    convert = node.knob('texConvertCheckbox').value()

    if convert == True:
        currentFrame = nuke.frame() 

        fileIn = node.knob('file').getValue().replace('.####.','.%s.' %currentFrame).replace('.%4d.','.%s.' %currentFrame)
        ext = fileIn.split('.')[-1]
        fileOut = fileIn.replace('/%s/' %ext,'/tex/').replace('.%s' %ext,'.tex').replace('.####.','.%s.' %currentFrame).replace('.%4d.','.%s.' %currentFrame)
        
        sMode = node.knob('sMode').value()
        tMode = node.knob('tMode').value()
        resize = node.knob('resize').value()
        filterValue = node.knob('filter').value()
        otherFlags = node.knob('otherFlags').value()
        
        if resize == 'none':
            command = 'txmake -verbose -float -smode %s -tmode %s -resize %s %s %s %s\n' %(sMode, tMode, resize, otherFlags, fileIn, fileOut)
        else:
            command = 'txmake -verbose -float -smode %s -tmode %s -resize %s -filter %s %s %s %s\n' %(sMode, tMode, resize, filterValue, otherFlags, fileIn, fileOut)
        print '> converting tex...'
        print command
        popObj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = popObj.communicate()
        print out[0]

def addCallback():
    """auto add the tex converter to write nodes"""
    nuke.callbacks.addOnUserCreate(texTab, args=(), kwargs={}, nodeClass='Write')
