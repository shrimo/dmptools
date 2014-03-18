import os

from maya import cmds, mel

def getShaderFromObject(node):
    nodeShape = cmds.listRelatives(node, shapes=True)[0]
    shader = cmds.listConnections(cmds.listConnections(nodeShape+".instObjGroups[0]")[0]+".surfaceShader")
    
    return shaders

def getNormalFileFromObject(node):
    shaders = getShaderFromObject(node)

    if shaders:
        shadingGroup = cmds.listConnections(shader[0]+".outColor")
        colorTexture = cmds.listConnections(shader[0]+".color")
        
        if colorTexture:
            colorTexturePath = cmds.getAttr(colorTexture[0]+'.fileTextureName')
            normalPath = os.path.dirname(colorTexturePath).replace('color', 'normal')
            if os.path.exists(normalPath):
                normalTexturePath = normalPath+'/'+os.path.basename(colorTexturePath).replace('_C', '_N')
                if os.path.isfile(normalTexturePath):
                    print 'normal map exists'

def getComponentFromTexture(textureNode, component='color'):
    comps = {'color':'_C', 'normal':'_N', 'specular':'_S'}

    if not 'dead_space' in cmds.getAttr(textureNode+'.fileTextureName'):
        cmds.warning('Cannot create component beacause this is not a  DS texture.')

    if not component in ('color', 'normal', 'specular'):
        cmds.warning("Please put one of the following component: 'color', 'normal', 'specular'")

    texturePath = cmds.getAttr(textureNode+'.fileTextureName')
    textureComponent = os.path.dirname(texturePath).split('/')[-1]

    if textureComponent == component:
        cmds.warning('You are trying to get the same component as the texture selected.')

    componentPath = os.path.dirname(texturePath).replace(textureComponent, component)
    if os.path.exists(componentPath):
        originalComp = comps[textureComponent]
        replaceComp = comps[component]
    else:
        cmds.warning('Cannot find component path.')
    componentTexturePath = componentPath+'/'+os.path.basename(texturePath).replace(originalComp, replaceComp)
    if os.path.isfile(componentTexturePath):
        return componentTexturePath
    else:
        cmds.warning('Cannot find component texture file.')
        

def main():
    selection = cmds.ls(sl=True)
    if selection:
        node = selection[0]
    else:
        cmds.warning('no selection!')

    normal = getComponentFromTexture(node, 'normal')
    newTextureFile = cmds.shadingNode('file', asTexture=True)
    cmds.setAttr(newTextureFile+'.fileTextureName', t, type="string")