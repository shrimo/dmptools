"""
init the dmptools for maya
"""

DRIVE = '!GOOGLEDRIVE_PATH!'

def createShelf():
    """
    create shelf
    """
    import dmptools.setup.shelf as shelf
    shelf.main()

def createHotkeys():
    """
    create hotkeys
    """    
    import dmptools.setup.hotkeys as hotkeys
    hotkeys.main()

def addDrivePath():
    # add google drive path to sys if exists
    # this is for using dmptools_misc modules
    import os
    import sys
    if os.path.exists(DRIVE):
        sys.path.append(DRIVE)

def main():
    """
    init the dmptools basic setup   
    """
    createHotkeys()
    createShelf()
    addDrivePath()

if __name__ == '__main__':
    main()