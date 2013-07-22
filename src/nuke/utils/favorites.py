import os
import nuke

def createFavoriteDirs():
    """
        create favorite directory if env vars are found
    """
    show = os.getenv('PL_SHOW')
    if show:
        division = os.getenv('PL_DIVISION')
        if division:
            sequence = os.getenv('PL_SEQ')
            if sequence:
                shot = os.getenv('PL_SHOT')
                if shot:
                    # create paths
                    shotPath = os.getenv('PL_SHOT_PATH')
                    mayaPath = shotPath+'/work/'+os.getenv('USER')+'/maya/'
                    nukeScriptsPath = shotPath+'/work/'+os.getenv('USER')+'/nuke/scripts/'
                    renderWorkP = shotPath+'/work/'+os.getenv('USER')+'/render/'
                    texturePath = shotPath+'/asset/texture/'
                    renderPath = shotPath+'/render/'
                    renderWsPath = shotPath+'/renderws/'

                    # add favorite dirs
                    nuke.addFavoriteDir(name='|-work maya ', directory=mayaPath)
                    nuke.addFavoriteDir(name='|-work nuke', directory=nukeScriptsPath)
                    nuke.addFavoriteDir(name='|-work render', directory=renderWorkP)
                    nuke.addFavoriteDir(name='|-textures', directory=texturePath)
                    nuke.addFavoriteDir(name='|-render', directory=renderPath)
                    nuke.addFavoriteDir(name='|-renderws', directory=renderWsPath)