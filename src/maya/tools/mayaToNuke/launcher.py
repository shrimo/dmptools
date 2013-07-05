#========================================================
#
# Generates a Nuke .nk file from Maya 
# objects cameras and locators (animated)
# michael.havart@gmail.com
#
#=========================================================

import dmptools.tools.mayaToNuke.ui as ui

def main(dockable=True):
    # run the maya to nuke UI
    mayaToNukeUI = ui.MayaToNukeUI()
    mayaToNukeUI.buildUI(dockable)

if __name__ == '__main__':
    main()