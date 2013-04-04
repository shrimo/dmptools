#============================================
#
# settings.py
# michael.havart@gmail.com
# class used to manage various settings. 
#
#============================================

from __future__ import with_statement
import os
import subprocess

HOMEPATH = '!HOMEPATH!'

class SettingsManager(object):
    """
    manage the dmptools settings.
    you can only set one setting at a time.
    usage:
    >>> settings = SettingsManager()
    >>> newsettings = settings.addSetting(key='', value=None)

    to remove a setting:
    >>> settings = SettingsManager()
    >>> newSettings = settings.removeSetting(key='')

    to get a setting value (returns a list):
    >>> settings = SettingsManager()
    >>> setting = settings.getSetting(key='')

    to get a print version of all the settings (keys and values):
    >>> settings = settingManager()
    >>> print settings.getStrsettings()
    """
    
    def __init__(self):
        """
        if the setting file doesn't exists create it.
        """
        # create the settings file in homepath/.dmptools
        dmptoolspath = HOMEPATH+'/.dmptools'
        if not os.path.exists(dmptoolspath):
            os.mkdir(dmptoolspath)
        self.settingsfile = dmptoolspath+'/dmptools.settings'
        
        # create the setting file if it doesnt exists
        if not os.path.exists(self.settingsfile):
            # creating setting file
            print '> creating setting file'
            with open(self.settingsfile, 'w') as FILE:
                FILE.write('')

    def addSetting(self, key='', value=None):
        """
        the setting key need to be a string and the value can be anything.
        if the key already exists in the setting file,
        then remove the old one and append a new one.

        returns a list of all the settings in the file.
        """
        dic = {key:value}
        # checking if the setting already exists
        settingList = self.getSettings()
        newsettingList = []
        if settingList:
            for setting in settingList:
                if not dic.keys() == setting.keys():
                    newsettingList.append(setting)
        newsettingList.append(dic)

        # remove the setting file to re-create the new one
        os.remove(self.settingsfile)
        with open(self.settingsfile, 'w') as FILE:
            for setting in newsettingList:
                FILE.write(str(setting)+'\n')

        return self.getSettings()

    def removeSetting(self, key=''):
        """
        remove a setting from the setting file.

        returns a list of all the settings in the file.
        """
        settingList = self.getSettings()
        newsettingList = []
        if settingList:
            for setting in settingList:
                if not key in setting.keys():
                    newsettingList.append(setting)

        # remove the setting file to re-create the new one
        os.remove(self.settingsfile)
        with open(self.settingsfile, 'w') as FILE:
            for setting in newsettingList:
                FILE.write(str(setting)+'\n')

        return self.getSettings()

    def getSetting(self, key=''):
        """
        return the setting matching the key.
        """
        values = None
        with open(self.settingsfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dic = eval(line)
                    if key in dic.keys():
                        values = dic.values()
                        break
                except:
                    pass

        return values

    def getSettings(self):
        """
        returns a list of dict from the setting file.
        """
        dictList = []
        with open(self.settingsfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dictList.append(eval(line))
                except:
                    pass

        return dictList
        
    def openSettingsFile(self):
        """
        open the setting file with notepad
        """
        if os.path.exists(self.settingsfile):
            subprocess.Popen('notepad '+self.settingsfile)
        else:
            raise UserWarning('setting file not found!')

    def getStrSettings(self):
        """ 
        convert settings dicts to str
        """
        global settingsStr
        settings = SettingsManager()
        settingsL = settings.getSettings()
        # recursive method
        def setStr(setting):
            global settingsStr
            for key in setting.keys():
                settingsStr += "-"+str(key)+":\n"
                for value in setting.values():
                    if type(value).__name__ == 'dict':
                        settingsStr += "\t"
                        setStr(value)
                    else:
                        settingsStr += "\t"+str(value)+"\n"
                        
        settingsStr = "settings:\n"
        # go through all the settings
        for setting in settingsL:
            setStr(setting)
        
        return settingsStr
