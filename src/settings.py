# with statement
from __future__ import with_statement

# system modules
import os
import subprocess

# strings to be generated by the install
HOMEPATH = '!HOMEPATH!'

class SettingsManager(object):
    """
    manages the dmptools settings.
    creates a settings file when declaring the class.
    you can only set one setting at a time.

    usage:
    >>> settings = SettingsManager(name='default')
    >>> newsettings = settings.add(key='', value=None)

    to remove a setting:
    >>> settings = SettingsManager('default')
    >>> newSettings = settings.remove(key='')

    to get a setting value (returns a list):
    >>> settings = SettingsManager('default')
    >>> setting = settings.get(key='')

    to get a print version of all the settings (keys and values):
    >>> settings = settingManager('default')
    >>> print settings.getStr()

    to open the settings file:
    >>> settings = SettingsManager('default')
    >>> settings.openFile()

    to clear the settings and recreate (or not) the file:
    >>> settings = SettingsManager('default')
    >>> settings.clearFile(recreate=False) # this will erase the file
    >>> settings.clearFile(recreate=True) # this will erase the file and recreate it

    """
    
    def __init__(self, name=''):
        """
        if the setting file doesn't exists create it.
        """
        # create the settings file in homepath/.dmptools
        self.dmptoolspath = HOMEPATH+'/.dmptools'
        if not os.path.exists(self.dmptoolspath):
            os.mkdir(self.dmptoolspath)
        self.settingsfile = self.dmptoolspath+'/'+name+'.settings'
        
        # create the setting file if it doesnt exists
        if not os.path.exists(self.settingsfile):
            # creating setting file
            print '> creating setting file:', self.settingsfile
            with open(self.settingsfile, 'w') as FILE:
                FILE.write('')

    def checkForFile(self):
        """
        checks if the setting file exists.
        raise an error if not.
        """
        if not os.path.exists(self.settingsfile):
            raise UserWarning("You need to recreate the SettingsManager with a new file")

    def clearFile(self, recreate=False):
        """
        clear the settings file and recreate it if 'recreate' == True
        """
        if os.path.exists(self.settingsfile):
            print '> removing setting file:', self.settingsfile
            os.remove(self.settingsfile)
        if recreate:
            with open(self.settingsfile, 'w') as FILE:
                FILE.write('')
    
    def getAllSettingsFiles(self):
        """
        returns a list of all the settings files
        found in the settings dir
        """
        return [f.replace('.settings', '') for f in os.listdir(self.dmptoolspath) if '.settings' in f]

    def add(self, key='', value=None):
        """
        the setting key need to be a string and the value can be anything.
        if the key already exists in the setting file,
        then remove the old one and append a new one.

        returns a list of all the settings in the file.
        """
        self.checkForFile()
        dic = {key:value}
        # checking if the setting already exists
        settingList = self.getAll()
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

        return self.getAll()

    def remove(self, key=''):
        self.checkForFile()
        """
        remove a setting from the setting file.
        returns a list of all the settings in the file.
        """
        settingList = self.getAll()
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

        return self.getAll()

    def get(self, key=''):
        """
        return the setting matching the key.
        """
        self.checkForFile()
        values = None
        with open(self.settingsfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dic = eval(line)
                    if key in dic.keys():
                        values = dic.values()[0]
                        break
                except:
                    pass

        return values

    def getAll(self):
        """
        returns a list of dict from the setting file.
        """
        self.checkForFile()
        dictList = []
        with open(self.settingsfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dictList.append(eval(line))
                except:
                    pass

        return dictList
        
    def openFile(self):
        """
        open the setting file with notepad
        """
        self.checkForFile()
        subprocess.Popen('notepad '+self.settingsfile)

    def getStr(self):
        """ 
        convert settings dicts to str
        """
        self.checkForFile()
        global settingsStr
        settingsL = self.getAll()
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
