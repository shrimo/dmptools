import os
import subprocess

import nuke
import nukescripts
from threading import Thread

from dmptools.settings import SettingsManager
SETTINGS = SettingsManager('nuke')

class ImageConverter(nukescripts.PythonPanel, Thread):
    def __init__(self):        
        nukescripts.PythonPanel.__init__(self, 'ImageConverter', 'ImageConverter')
        Thread.__init__(self)

        # store the knobs here
        knobs = []
        # create header
        self.header = nuke.Text_Knob('header', '', "Converts images.")

        # file knob
        fileknobPath = SETTINGS.get('img_converter_fileknob')
        if not 'fileknobPath' in locals() or fileknobPath == None:
            fileknobPath = '/tmp/'

        self.fileKnob = nuke.File_Knob('', 'input folder')
        self.fileKnob.setValue(fileknobPath)
        knobs.append(self.fileKnob)

        # main file list knob
        self.fileMultiline = nuke.Multiline_Eval_String_Knob('files to convert', 'files', '')
        knobs.append(self.fileMultiline)

        # create read checkbox
        createRead = SETTINGS.get('img_converter_createRead')
        if not 'createRead' in locals():
            createRead = False
        self.createRead = nuke.Boolean_Knob('Cread read nodes', createRead)
        knobs.append(self.createRead)

        # create the knobs
        for knob in knobs:
            self.addKnob(knob)

    def convert(self, node):
        pass

    def knobChanged(self, knob):
        if knob == self.fileKnob:
            path = self.fileKnob.getValue()
            SETTINGS.add('img_converter_fileknob', path)
            try:
                files = '\n'.join([item for item in os.listdir(path) if os.path.isfile(path+'/'+item)])
                self.fileMultiline.setValue(files)
            except:
                self.fileMultiline.setValue('no files found...')

