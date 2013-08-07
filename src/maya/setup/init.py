"""
dmptools for Maya
init the dmptools for Maya

"""

import os
import sys

# get start time
starttime = os.times()[-1]

# load shell/interpreter dmptools print modules
from dmptools.output import defaultPrint, successPrint, errorPrint

DRIVE = '!GOOGLEDRIVE_PATH!'

# load dmptools setup modules
try:
    defaultPrint('loading dmptools...')
    # add google drive path to sys if exists
    # this is for using dmptools_misc modules
    if os.path.exists(DRIVE):
        defaultPrint('loading dmptools_misc...')
        sys.path.append(DRIVE)

    # custom maya settings
    import dmptools.setup.mayaSettings as mayaSettings
    mayaSettings.setCustomSettings()

    # create shelf
    import dmptools.setup.shelf as shelf
    shelf.main()

    # create hotkeys
    import dmptools.setup.hotkeys as hotkeys
    hotkeys.main()

    endtime = os.times()[-1]
    elapsedtime = endtime-starttime
    successPrint('loading time: '+str(elapsedtime)[:6]+'sec', timestamp=True)  

# report the error if any
except BaseException as exception:
    errorPrint('failed to load dmptools:\n'+str(exception))
