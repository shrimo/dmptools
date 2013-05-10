"""
init the dmptools for maya
"""

DRIVE = '!GOOGLEDRIVE_PATH!'

def main():
    """
    init the dmptools basic setup   
    """
    # create sheld and init hotkeys
    import dmptools.shelf as shelf
    import dmptools.hotkeys as hotkeys
    shelf.main()
    hotkeys.main()

    # add google drive path to sys
    import sys
    import os
    if os.path.exists(DRIVE):
        sys.path.append(DRIVE)

if __name__ == '__main__':
    main()