"""
dmptools for Nuke
init the dmptools for Nuke

"""
__author__ = "Michael Havart"
__copyright__ = "Copyright (C) 2013 Michael Havart"
__credits__ = "Michael Havart, Jordi Riera, Julien Bolbach, Eddy Richard"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Michael Havart"
__email__ = "michael.havart@gmail.com"
__github__ = "https://github.com/michael-ha/dmptools"
__status__ = "Production"

import os
import sys
from dmptools.output import defaultPrint, successPrint, errorPrint

starttime = os.times()[-1]
DRIVE = '!GOOGLEDRIVE_PATH!'

# add google drive path to sys if exists
# this is for using dmptools_misc modules
if os.path.exists(DRIVE):
    sys.path.append(DRIVE)

try:
    defaultPrint('loading dmptools...')    
    # build menus
    import dmptools.menu as menu
    menu.main()

    defaultPrint('loading user menu...')
    # build user menu
    import dmptools.userMenu as userMenu
    userMenu.main()

    endtime = os.times()[-1]
    elapsedtime = endtime-starttime

    successPrint('loading time: '+str(elapsedtime)[:6]+'sec', timestamp=True)
    
except BaseException as e:
    errorPrint('failed to load dmptools:\n'+str(e))
