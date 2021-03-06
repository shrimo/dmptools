=================================================

Maya and Nuke python tools for Windows and Linux.

=================================================

INSTALL

REQUIREMENTS:
    - Maya 2011+ and/or Nuke6.4+ installed.
    - Windows: python2.7 installed in c:/python27.

I - with Sublime Text editor:
    - clone dmptools: git clone git://github.com/michael-ha/dmptools.git
    - open Sublime Text
    - project > open > dmptools.sublime-project
    - tools > build system > dmptools
    - tools > build

II - without Sublime Text editor:
    - clone dmptools: git clone git://github.com/michael-ha/dmptools.git
    - execute install.py from an explorer in the dmptools root OR in command shell run 'python install.py' from the root of the dmptools

UNINSTALL:
    - execute uninstall.py from an explorer in the dmptools root OR run in a command shell run 'python uninstall.py' or 'python install.py uninstall'

RESULT:
    - Maya: You should see a new shelf 'dmptools' and the marking menu of the tools is mapped to the 'j' key.
    - Nuke: You should see a new toolbar 'dmptools' on the left toolbar.
