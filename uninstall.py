import install

def main():
    install.uninstall()

if __name__ == '__main__':
    main()
    # ask to press enter if the install.py file is executed by hand
    try:
        raw_input("\npress enter to continue...")
    except:
        pass
