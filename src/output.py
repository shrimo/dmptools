import os
import time
import inspect

# globals
suffix = '\033[m'
defaultColors = '\033[32m'
successColors = '\033[32;1m'
warningColors = '\033[33m'
errorColors = '\033[31;1m'
contexts = ['default', 'system', 'both']

def defaultPrint(stuff, context='both', timeStamp=False):
    """ prints out a default message """
    prefix = '['+inspect.currentframe().f_back.f_globals['__name__']+'] ::'
    if timeStamp:
        currentTime = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    else:
        currentTime = ''
    if not context in contexts:
        raise UserWarning('Context not valid.')
    if context == 'default':
        print prefix, stuff
    if context == 'system':
        os.system('echo "'+defaultColors+prefix+' '+str(stuff)+' '+currentTime+suffix+'"')
    if context == 'both':
        print prefix, stuff
        os.system('echo "'+defaultColors+prefix+' '+str(stuff)+' '+currentTime+suffix+'"')

def successPrint(stuff, context='both', timeStamp=False):
    """ prints out a success message """
    prefix = '['+inspect.currentframe().f_back.f_globals['__name__']+'] ::'
    if timeStamp:
        currentTime = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    else:
        currentTime = ''
    if not context in contexts:
        raise UserWarning('Context not valid.')
    if context == 'default':
        print prefix+' Success ::', stuff
    if context == 'system':
        os.system('echo "'+successColors+prefix+' Success :: '+str(stuff)+' '+currentTime+suffix+'"')
    if context == 'both':
        print prefix+' Success ::', stuff
        os.system('echo "'+successColors+prefix+' Success :: '+str(stuff)+' '+currentTime+suffix+'"')

def warningPrint(stuff, context='both', timeStamp=False):
    """ prints out a warning message """
    prefix = '['+inspect.currentframe().f_back.f_globals['__name__']+'] ::'
    if timeStamp:
        currentTime = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    else:
        currentTime = ''
    if not context in contexts:
        raise UserWarning('Context not valid.')
    if context == 'default':
        print prefix+' Warning ::', stuff
    if context == 'system':
        os.system('echo "'+warningColors+prefix+' Warning :: '+str(stuff)+' '+currentTime+suffix+'"')
    if context == 'both':
        print prefix+' Warning ::', stuff
        os.system('echo "'+warningColors+prefix+' Warning :: '+str(stuff)+' '+currentTime+suffix+'"')

def errorPrint(stuff, context='both', timeStamp=False):
    """ prints out an error message """
    prefix = '['+inspect.currentframe().f_back.f_globals['__name__']+'] ::'
    if timeStamp:
        currentTime = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    else:
        currentTime = ''
    if not context in contexts:
        raise UserWarning('Context not valid.')
    if context == 'default':
        print prefix+' Error ::', stuff
    if context == 'system':
        os.system('echo "'+errorColors+prefix+' Error :: '+str(stuff)+' '+currentTime+suffix+'"')
    if context == 'both':
        print prefix+' Error ::', stuff
        os.system('echo "'+errorColors+prefix+' Error :: '+str(stuff)+' '+currentTime+suffix+'"')
