import pymel.core as pc
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

def resetWindowsLocations():
    #put the names of any windows you want checked in this list
    windowsList = [
            # dmptools windows
            "dmptools_settings_window",
            "create_createCustomItem",
            "ArcMainWindow",
            "uvTileManagerWindow",
            "sym_window",
            "runCommandWin",
            "apertureToolWindow",
            "separateUI",
            "dmptools_display_color_window",
            "camConstraintUI",
            "batch_rename",
            "mtn_Window",
            "hotkeys_window",
            "hotkeys_ctrl",

            # maya windows
            "scriptEditorPanel1Window",
            "polyTexturePlacementPanel1Window",
            "outlinerPanel1Window",
            "hyperGraphPanel1Window",
            "graphEditor1Window", 
            "hyperShadePanel1Window", 
            "PreferencesWindow",
            "pluginManagerWindow",
            "PluginInfoWin",
            "renderViewWindow"]
     
    #loop through all windows
    for window in windowsList:
        #get the window position
        if pc.windowPref(window, exists=True):
            #get the corner location
            corner = pc.windowPref(window, q=True, tlc=True)
     
            #check it against the window:
            #so, grab a QDesktopWidget for the screen
            desk = QtGui.QApplication.desktop()
     
            #now, get the number of the screen this should be on
            screenNum = desk.screenNumber(QtCore.QPoint(corner[0], corner[1]))
     
            #now, get a QRect of the space on that screen
            screenSpace = desk.availableGeometry(screenNum)
     
            #now, check if the point is in that screen space
            if(not screenSpace.contains(corner[0], corner[1], False)):
                #move it
                pc.windowPref(window, e=True, tlc = [10,10])
                print "moved window: ", window
            pc.windowPref(window, remove=True)

def main():
    resetWindowsLocations()
