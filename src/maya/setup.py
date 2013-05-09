DRIVE = '!GOOGLEDRIVE_PATH!'

def main():
    """
    init the dmptools basic setup   
    """
    import dmptools.shelf as shelf
    import dmptools.hotkeys as hotkeys
    shelf.main()
    hotkeys.main()

    # add google drive path to sys
    import sys
    sys.path.append(DRIVE)

if __name__ == '__main__':
    main()