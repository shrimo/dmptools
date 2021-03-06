import os
import nuke

def createFramestoreFavorites():
    """ create framestore based favorites directory if env vars are found """

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
                    nukeCompPath = shotPath+'/work/'+os.getenv('USER')+'/nuke/comp/'
                    renderWorkP = shotPath+'/work/'+os.getenv('USER')+'/render/'
                    texturePath = shotPath+'/asset/texture/'
                    renderPath = shotPath+'/render/'
                    renderWsPath = shotPath+'/renderws/'

                    # add favorite dirs
                    nuke.addFavoriteDir(name='|-work maya ', directory=mayaPath)
                    nuke.addFavoriteDir(name='|-work nuke', directory=nukeScriptsPath)
                    nuke.addFavoriteDir(name='|-work nuke', directory=nukeCompPath)
                    nuke.addFavoriteDir(name='|-work render', directory=renderWorkP)
                    nuke.addFavoriteDir(name='|-textures', directory=texturePath)
                    nuke.addFavoriteDir(name='|-render', directory=renderPath)
                    nuke.addFavoriteDir(name='|-renderws', directory=renderWsPath)

def createMpcFavorites():
    """ create MPC based favorites directory if env vars are found """

    user = os.getenv('USER')
    job = os.getenv('JOB')
    if job:
        shot = os.getenv('SHOT')
        if shot:
            dmpPath = str('/jobs/' + job + '/' + shot + '/maya/textures/images/env/')
            dmpmasterPath = str('/jobs/' + job + '/' + shot + '/maya/textures/masters/env/')

            nukePath = str('/jobs/' + job + '/' + shot + '/nuke/scene/'+user+'/')
            if not os.path.exists(nukePath):
                nukePath = str('/jobs/' + job + '/' + shot + '/nuke/scene/')

            mayaEnv = str('/jobs/' + job + '/' + shot + '/maya/scenes/env/'+user+'/')
            if not os.path.exists(mayaEnv):
                mayaEnv = str('/jobs/' + job + '/' + shot + '/maya/scenes/env/')

            mayaPath = str('/jobs/' + job + '/' + shot + '/maya/renders/'+user+'/')
            if not os.path.exists(mayaPath):
                mayaPath = str('/jobs/' + job + '/' + shot + '/maya/renders/')

            nuke.addFavoriteDir(name='|-Maya env dir', directory=mayaEnv)
            nuke.addFavoriteDir(name='|-Maya renders dir', directory=mayaPath)
            nuke.addFavoriteDir(name='|-Nuke user dir', directory=nukePath)
            nuke.addFavoriteDir(name='|-DMP images', directory=dmpPath)
            nuke.addFavoriteDir(name='|-DMP master', directory=dmpmasterPath)
            
def createFavorites():
    # get framestore host name
    host = os.getenv('HOST')
    # get mpc hostname
    hostname = os.getenv('HOSTNAME')

    # create framestore based favorites
    if host and host.split('.')[-2] == 'framestore':
        createFramestoreFavorites()

    # create mpc based favorites
    if hostname and hostname.split('.')[-2] == 'mpc':
        createMpcFavorites()