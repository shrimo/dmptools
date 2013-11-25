from maya import cmds
import dmptools.utils.mayaCommands as mayaCommands

def get_camera_info(node):
    camera_info = {}
    camera_info['transform'] = node
    camera_info['shape'] = cmds.listRelatives(node, shapes=True)[0]
    first_frame = int(cmds.playbackOptions(q=True, min=True))
    last_frame = int(cmds.playbackOptions(q=True, max=True))
    for frame in range(first_frame, last_frame+1):
        cmds.currentTime(frame)
        matrix= cmds.xform(node, ws=True, m=True, q=True)
        focal = float(cmds.getAttr(camera_info['shape']+'.focalLength'))
        hap = float(cmds.getAttr(camera_info['shape']+'.horizontalFilmAperture'))
        vap = float(cmds.getAttr(camera_info['shape']+'.verticalFilmAperture'))
        hfo = float(cmds.getAttr(camera_info['shape']+'.horizontalFilmOffset'))
        vfo = float(cmds.getAttr(camera_info['shape']+'.verticalFilmOffset'))
        camera_info['matrix.'+str(frame)] = matrix
        camera_info['focal.'+str(frame)] = focal
        camera_info['hap.'+str(frame)] = hap
        camera_info['vap.'+str(frame)] = vap
        camera_info['hfo.'+str(frame)] = hfo
        camera_info['vfo.'+str(frame)] = vfo
    
    camera_info['frames'] = sorted([key.split('.')[1] for key in camera_info.keys() if 'matrix' in key])
    return camera_info

def main():
    selection = cmds.ls(sl=True)
    if selection:
        node = selection[0]
    else:
        try:
            node = mayaCommands.getActiveCamera()
        except:
            pass

    if node:
        print '\nbaking camera '+str(node)+'...', 
        camera_info = get_camera_info(node)

        newCamera = cmds.camera()
        
        for frame in camera_info['frames']:
            cmds.currentTime(frame)
            # set matrix
            cmds.xform(newCamera[0], m=camera_info['matrix.'+str(frame)])
            cmds.setAttr(newCamera[1]+'.focalLength', camera_info['focal.'+str(frame)])
            cmds.setAttr(newCamera[1]+'.horizontalFilmAperture', camera_info['hap.'+str(frame)])
            cmds.setAttr(newCamera[1]+'.verticalFilmAperture', camera_info['vap.'+str(frame)])
            cmds.setAttr(newCamera[1]+'.horizontalFilmOffset', camera_info['hfo.'+str(frame)])
            cmds.setAttr(newCamera[1]+'.verticalFilmOffset', camera_info['vfo.'+str(frame)])
            # set keyframes
            cmds.setKeyframe(newCamera[0]+'.tx')
            cmds.setKeyframe(newCamera[0]+'.ty')
            cmds.setKeyframe(newCamera[0]+'.tz')
            cmds.setKeyframe(newCamera[0]+'.rx')
            cmds.setKeyframe(newCamera[0]+'.ry')
            cmds.setKeyframe(newCamera[0]+'.rz')
            cmds.setKeyframe(newCamera[1]+'.focalLength')
            cmds.setKeyframe(newCamera[1]+'.horizontalFilmAperture')
            cmds.setKeyframe(newCamera[1]+'.verticalFilmAperture')
            cmds.setKeyframe(newCamera[1]+'.horizontalFilmOffset')
            cmds.setKeyframe(newCamera[1]+'.verticalFilmOffset')
        print '\ncreated '+str(newCamera)+',',
    else:
        print '\nplease select a camera or go to an active 3d viewport.',