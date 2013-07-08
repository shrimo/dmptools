"""
dmptools for Maya
init the dmptools for Maya

"""

import os
import sys

DRIVE = '!GOOGLEDRIVE_PATH!'

try:
    os.system('echo "[dmptools]: loading dmptools..."')
    # add google drive path to sys if exists
    # this is for using dmptools_misc modules
    if os.path.exists(DRIVE):
        sys.path.append(DRIVE)

    # create shelf
    import dmptools.setup.shelf as shelf
    shelf.main()

    # create hotkeys
    import dmptools.setup.hotkeys as hotkeys
    hotkeys.main()
    
    os.system('echo "[dmptools]: done."')

except:
    os.system('echo "[dmptools]: ERROR: failed to load dmptools..."')