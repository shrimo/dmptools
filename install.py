#!/usr/bin/env python

"""
NAME 

    dmptools

DESCRIPTION

    Maya & Nuke dmptools standalone install file
    This will install the Maya and Nuke tools
    in the user respective folders.

    platforms: Windows, Linux

SYNOPSIS

    install:
    > python install.py
    or 
    > ./dmptools install

    uninstall:
    > python uninstall.py
    or
    > ./dmptools uninstall

    check install status:
    > python install.py check
    or
    > ./dmptools check

    help:
    > ./dmptools help

"""

# with statement
from __future__ import with_statement

# system modules
import platform
import os
import sys
import time
import fileinput
import shutil
from shutil import *

# module vars
__author__ = "Michael Havart"
__copyright__ = "Copyright (C) 2013 Michael Havart"
__credits__ = "Michael Havart, Jordi Riera, Julien Bolbach, Eddy Richard"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Michael Havart"
__email__ = "michael.havart@gmail.com"
__github__ = "https://github.com/michael-ha/dmptools"
__status__ = "Production"

# platform check
PLATFORM = platform.uname()[0]
HOST = platform.uname()[1]
MACHINE = platform.machine()

PLATFORMS = ['Windows', 'Linux']
if PLATFORM not in PLATFORMS:
    raise UserWarning('This install only works on Windows and Linux!')

# globals vars
MODULE_NAME = 'dmptools'
VERSION = '1.0.0'
MODULE_PATH = '.'
PYTHON_SOURCE_PATH = MODULE_PATH+'/src'
EXCLUDE_DIRS = \
    [
        '.git',
        'csh',
        'mel',
        'doc',
        'gizmos',
    ]
EXCLUDE_FILES = ['pyc', '~']
MAYA_USERSETUP_MEL_FILE = 'python("import dmptools.setup.init");// automatically added by the dmptools installation'
NUKE_MENU_FILE = 'import dmptools # automatically added by the dmptools installation'

# platform globals
if PLATFORM == 'Windows':
    HOMEPATH = os.getenv('USERPROFILE')
    GOOGLEDRIVE_PATH = HOMEPATH+'/google drive/code/python/'
    # nuke windows globals
    NUKE_PATH = HOMEPATH+'/.nuke/'
    IS_NUKE_EXISTS = os.path.exists(NUKE_PATH)

    # maya windows globals
    MAYA_GLOBAL = HOMEPATH+'/documents/maya/'
    IS_MAYA_EXISTS = os.path.exists(MAYA_GLOBAL)
    MAYA_PATH = MAYA_GLOBAL+'scripts/'

if PLATFORM == 'Linux':
    HOMEPATH = os.getenv('HOME')
    GOOGLEDRIVE_PATH = HOMEPATH+'/code/python/'
    # nuke Linux globals
    NUKE_PATH = HOMEPATH+'/.nuke/'
    IS_NUKE_EXISTS = os.path.exists(NUKE_PATH)

    # maya Linux globals
    MAYA_GLOBAL = os.getenv('HOME')+'/maya/'
    IS_MAYA_EXISTS = os.path.exists(MAYA_GLOBAL)
    MAYA_PATH = MAYA_GLOBAL+'scripts/'

# string replacements
REPLACEMENTS = \
    {
        # common
        '!PLATFORM!'            : PLATFORM,
        '!HOST!'                : HOST,
        '!MACHINE!'             : MACHINE,
        '!VERSION!'             : VERSION,
        '!HOMEPATH!'            : HOMEPATH,
        '!GOOGLEDRIVE_PATH!'    : GOOGLEDRIVE_PATH,
        '!HELP_PAGE!'           : __github__,

        # maya
        '!MAYA_GLOBAL!'         : MAYA_GLOBAL,
        '!MAYA_PATH!'           : MAYA_PATH+MODULE_NAME,
        '!MAYA_PICTURES!'       : MAYA_PATH+MODULE_NAME+'/pictures',
        '!MAYA_SHELF!'          : MAYA_PATH+MODULE_NAME+'/pictures/shelf',

        # nuke
        '!NUKE_SHARE!'          : NUKE_PATH+MODULE_NAME+'/pictures',
    }

def installNuke():
    # install nuke process
    print '=============================='
    print '           N U K E            '
    print '=============================='
    print 'installing nuke '+MODULE_NAME+' in '+NUKE_PATH+MODULE_NAME+' ...'

    # delete old dmpTools
    if os.path.exists(NUKE_PATH+MODULE_NAME):
        print ' > deleting old dmpTools ...'
        shutil.rmtree(NUKE_PATH+MODULE_NAME)
    # install nuke tools
    install(PYTHON_SOURCE_PATH+'/nuke', NUKE_PATH+MODULE_NAME)
    # copy stuff from dmptools/python root to respective modules
    for f in os.listdir(PYTHON_SOURCE_PATH):
        if '.py' in f:
            print ' > installing file', PYTHON_SOURCE_PATH+'/'+f, 'to', NUKE_PATH+MODULE_NAME+'/'+f
            shutil.copy2(PYTHON_SOURCE_PATH+'/'+f, NUKE_PATH+MODULE_NAME+'/'+f)
    # replacements
    print ' > doing replacements...'
    replacements(NUKE_PATH+MODULE_NAME)
    # createnuke menu file
    createNukeMenu()
    print ' > done.'

def installMaya():
    # install maya process
    print '=============================='
    print '           M A Y A            '
    print '=============================='
    print 'installing maya '+MODULE_NAME+' in '+MAYA_PATH+MODULE_NAME+' ...'

    # delete old dmpTools
    if os.path.exists(MAYA_PATH+MODULE_NAME):
        print ' > deleting old dmpTools ...'
        shutil.rmtree(MAYA_PATH+MODULE_NAME)
    # install maya tools (python & mel)
    install(PYTHON_SOURCE_PATH+'/maya', MAYA_PATH+MODULE_NAME)
    # copy stuff from dmptools/python root to respective modules
    for f in os.listdir(PYTHON_SOURCE_PATH):
        if '.py' in f:
            print ' > installing file', PYTHON_SOURCE_PATH+'/'+f, 'to', MAYA_PATH+MODULE_NAME+'/'+f
            shutil.copy2(PYTHON_SOURCE_PATH+'/'+f, MAYA_PATH+MODULE_NAME+'/'+f)
    # replacements
    print ' > doing replacements...'
    replacements(MAYA_PATH+MODULE_NAME)
    # create userSetup to load the shelf
    createMelUserSetup()
    print ' > done.'

def replacements(path):
    # check the files in the install path
    for root, dirs, files in os.walk(path):
        for f in files:
            # go through python & mel files only
            if f.split('.')[-1] in ['py', 'mel', 'nk', 'gizmo']:
                for line in fileinput.input(root+'/'+f, inplace=1):
                    # if the key in REPLACEMENTS is in the file then replace the line
                    for rep in REPLACEMENTS.keys():
                        if rep in line:
                            line = line.replace(rep, REPLACEMENTS[rep])
                    # write the replaced line in the file
                    sys.stdout.write(line)

def createMelUserSetup():
    '''
    create the userSetup file for Maya startup
    '''
    mel_file = MAYA_PATH+'/userSetup.mel'
    is_menu_file = os.path.exists(mel_file)
    # scan the mel file if exists
    if is_menu_file:
        print " > mel userSetup already exists, need to edit it."
        newlines = []
        with open(mel_file, "r+") as FILE:
            lines = FILE.readlines()
            add = True
            for line in lines:
                if 'python("import dmptools' in line:
                    lines.remove(line)
                    lines.append(MAYA_USERSETUP_MEL_FILE)
                    add = False
                    break
                else:
                    add = True
            if add:
                lines.append(MAYA_USERSETUP_MEL_FILE)
            newlines = lines
        with open(mel_file, "w") as FILE:
            FILE.write(str(''.join(newlines)))
    # the mel file doesn't exist so create it
    else:
        print " > mel userSetup doesn't exist, need to create it."
        print ' > creating', mel_file
        with open(mel_file, 'w') as FILE:
            FILE.write(MAYA_USERSETUP_MEL_FILE)

def createNukeMenu():
    '''
    create the menu.py file for Nuke startup
    '''
    menu_file = NUKE_PATH+'/menu.py'
    is_menu_file = os.path.exists(menu_file)
    # scan the menu file if exists
    if is_menu_file:
        print " > nuke menu already exists, need to edit it."
        newlines = []
        with open(menu_file, "r+") as FILE:
            lines = FILE.readlines()
            add = True
            for line in lines:
                if 'import dmptools' in line:
                    lines.remove(line)
                    lines.append(NUKE_MENU_FILE)
                    add = False
                    break
                else:
                    add = True
            if add:
                lines.append(NUKE_MENU_FILE)
            newlines = lines
        with open(menu_file, "w") as FILE:
            FILE.write(str(''.join(newlines)))
    # the mel file doesn't exist so create it
    else:
        print " > nuke menu file doesn't exist, need to create it."
        print ' > creating', menu_file
        with open(menu_file, 'w') as FILE:
            FILE.write(NUKE_MENU_FILE)
     
def install(src, dst, symlinks=False, ignore=None):
    '''
    slightly different shutil.copytree
    '''
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                if os.path.split(srcname)[-1] not in EXCLUDE_DIRS:
                    print ' > installing directory', srcname, 'to', dstname
                    install(srcname, dstname, symlinks, ignore)
            else:
                if os.path.split(srcname)[-1].split('.')[-1] not in EXCLUDE_FILES:
                    print ' > installing file', srcname, 'to', dstname
                    copy2(srcname, dstname)
        # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError, why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def lineCounter():
    """
    quick file and line counter
    """
    lines = {}
    for root, dirs, files in os.walk(MAYA_PATH+MODULE_NAME):
        for f in files:
            if f.split('.')[-1] == 'py':
                lines[f] = {}
                with open(root+'/'+f, 'r') as FILE:
                    lines[f] = FILE.readlines()
    for root, dirs, files in os.walk(NUKE_PATH+MODULE_NAME):
        for f in files:
            if f.split('.')[-1] == 'py':
                lines[f] = {}
                with open(root+'/'+f, 'r') as FILE:
                    lines[f] = FILE.readlines()
    i = 0
    for k in lines.keys():
        i = i+(len(lines[k]))

    return lines.keys(), i

def uninstall():
    """
    uninstall the dmptools for nuke and maya
    remove the module calls from the nuke menu file and the maya userSetup file
    """

    # uninstall maya dmptools
    print "\nUninstalling:"
    print '>> uninstalling maya dmptools...'
    if os.path.exists(MAYA_PATH+MODULE_NAME):
        shutil.rmtree(MAYA_PATH+MODULE_NAME)
    else:
        print 'maya dmptools not found...'
    mel_file = MAYA_PATH+'userSetup.mel'
    is_mel_file = os.path.exists(mel_file)
    # scan the mel file if exists
    if is_mel_file:
        newlines = []
        with open(mel_file, "r+") as FILE:
            lines = FILE.readlines()
            add = False
            for line in lines:
                if 'python("import dmptools' in line:
                    lines.remove(line)
            newlines = lines
        with open(mel_file, "w") as FILE:
            FILE.write(str(''.join(newlines)))
    print '>> done.'

    # uninstall nuke dmptools
    print '>> uninstalling nuke dmptools...'
    if os.path.exists(NUKE_PATH+MODULE_NAME):
        shutil.rmtree(NUKE_PATH+MODULE_NAME)
    else:
        print 'nuke dmptools not found...'
    menu_file = NUKE_PATH+'menu.py'
    is_menu_file = os.path.exists(menu_file)
    # scan the menu file if exists
    if is_menu_file:
        newlines = []
        with open(menu_file, "r+") as FILE:
            lines = FILE.readlines()
            add = False
            for line in lines:
                if 'import dmptools' in line:
                    lines.remove(line)
            newlines = lines
        with open(menu_file, "w") as FILE:
            FILE.write(str(''.join(newlines)))
    print '>> done.'

def checkInstall():
    """
    checks if the dmptools for nuke and maya are installed
    """

    print '\nChecking:'
    if os.path.exists(NUKE_PATH+MODULE_NAME):
        print '+nuke dmptools is installed here:', NUKE_PATH+MODULE_NAME
    else:
        print '-nuke dmptools is NOT installed'
    menu_file = NUKE_PATH+'menu.py'
    is_menu_file = os.path.exists(menu_file)
    if is_menu_file:
        with open(menu_file, "r") as FILE:
            lines = FILE.readlines()
            for line in lines:
                if 'import dmptools' in line:
                    print '+nuke dmptools module found in menu file:', menu_file

    if os.path.exists(MAYA_PATH+MODULE_NAME):
        print '+maya dmptools is installed here:', MAYA_PATH+MODULE_NAME
    else:
        print '-maya dmptools is NOT installed'

    mel_file = MAYA_PATH+'userSetup.mel'
    is_mel_file = os.path.exists(mel_file)
    if is_mel_file:
        with open(mel_file, "r") as FILE:
            lines = FILE.readlines()
            for line in lines:
                if 'import dmptools' in line:
                    print '+maya dmptools module found in userSetup file:', mel_file

def main():
    """
    run the install
    """
    print '\nDMPTOOLS INSTALL\n'
    print 'executing',' '.join(sys.argv)
    print 'We are on', PLATFORM, '!'
    
    # check if dmptools are installed
    checkInstall()

    # install Nuke dmptools
    if IS_NUKE_EXISTS:
        installNuke()
    else:
        print 'Error: nuke path not found!'
    # install Maya dmptools
    if IS_MAYA_EXISTS:
        installMaya()
    else:
        print 'Error: maya path not found!'
    # print the file and line count
    # files = lineCounter()
    # print '>>>', len(files[0]), 'files, ', files[1], 'lines'
    print ' >> installed at', str(time.strftime('%H:%M:%S the %d/%m/%y'))

if __name__ == '__main__':
    """
    runs the check install function if 'check' is the arguments.
    otherwise runs the main function.
    """

    # check install if arg is 'check'
    if len(sys.argv) == 2 and sys.argv[-1] == 'check':
        checkInstall()

    # run the install
    else:
        main()
        # ask to press enter if the install.py file is executed by hand
        try:
            raw_input("\npress enter to continue...")
        except:
            pass
