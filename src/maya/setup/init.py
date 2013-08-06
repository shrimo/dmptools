"""
dmptools for Maya
init the dmptools for Maya

"""

import os
import sys

starttime = os.times()[-1]

from dmptools.output import defaultPrint, successPrint, errorPrint

DRIVE = '!GOOGLEDRIVE_PATH!'

try:
    defaultPrint('loading dmptools...')
    # add google drive path to sys if exists
    # this is for using dmptools_misc modules
    if os.path.exists(DRIVE):
        defaultPrint('loading dmptools_misc...')
        sys.path.append(DRIVE)

    # custom maya settings
    import dmptools.setup.settings as mayaSettings
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

except BaseException as e:
    errorPrint('failed to load dmptools:\n'+str(e))
