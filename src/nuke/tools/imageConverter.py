import nuke
import nukescripts
import os

def deselectAll():
	for n in nuke.allNodes():
		n['selected'].setValue(False)

def selectReplace(node):
	for n in nuke.allNodes():
		n['selected'].setValue(False)
	node['selected'].setValue(True)

def selectAdd(node):
	node['selected'].setValue(True)

def makeProxy(node, filePath, filePathBool, fileType, convertFrom, convertTo, scaleFactor, createRead, alpha, anim, overwrite):
	
	deselectAll()
	selectReplace(node)
	reformat = nuke.createNode('Reformat', inpanel = False)
	reformat['type'].setValue('scale')
	reformat['scale'].setValue(scaleFactor)
	
	file = node['file'].value().split('.')[-2]
	if file in ['####', '%4d']:
		file = node['file'].value().split('.')[-3]
	filename = os.path.basename(file)
	write = nuke.createNode('Write', inpanel = False)
	if filePathBool == 0:
		if anim:
			readFile = filePath+filename+'.####.'+fileType
		else:
			readFile = filePath+filename+'.'+fileType			
		if os.path.exists(readFile) and not overwrite:
			panel = nuke.Panel('warning, file name already exists !')
			panel.addSingleLineInput('please type new file name:', os.path.basename(file))
			val = panel.show()
			if val == 1:
				readFile = str(filePath+panel.value('please type new file name:')+'.'+fileType)
			#else:
			#	readFile = filePath+filename+'_copy.'+fileType
				
		write['file'].setValue(readFile)
	if filePathBool == 1:
		if anim:
			readFile = file+'.####.'+fileType
		else:
			readFile =file+'.'+fileType			
		
		if os.path.exists(readFile):
			panel = nuke.Panel('warning, file name already exists !')
			panel.addSingleLineInput('please type new file name:', os.path.basename(file))
			val = panel.show()
			if val == 1:
				readFile = str(os.path.dirname(file)+'/'+panel.value('please type new file name:')+'.'+fileType)
			else:
				readFile = filePath+filename+'_copy.'+fileType
		
		write['file'].setValue(readFile)
		
	write['file_type'].setValue(fileType)
	
	if fileType == 'jpeg':
		write['_jpeg_quality'].setValue(1)
	write['colorspace'].setValue(convertTo)
	try:
		write['views'].setValue('main')
	except:
		write['views'].setValue('left')
	
	if alpha == 1:
		write['channels'].setValue('rgba')

	if anim == 1:
		framerange = frameRange()
		try:
			first, last = int(framerange.split(',')[0]), int(framerange.split(',')[1])
		except:
			first, last = int(framerange.split('-')[0]), int(framerange.split('-')[1])
			
		nuke.execute(write, first, last)	
	else:
		nuke.execute(write, 1,1)	

	if createRead == 1:
		deselectAll()
		nuke.createNode('Read', inpanel = False).setName(node.name()+'_convert')
		read = nuke.selectedNode()
		read['file'].setValue(readFile)
		read['colorspace'].setValue(convertTo)
		if anim:
			read['first'].setValue(first)
			read['last'].setValue(last)

	deselectAll()
	selectAdd(reformat)
	selectAdd(write)
	nukescripts.node_delete()
	deselectAll()	
	
def frameRange():
	
	panel = nuke.Panel('frame range')
	panel.addSingleLineInput('range:', str(int(nuke.root()['first_frame'].getValue()))+','+str(int(nuke.root()['last_frame'].getValue())))
	val = panel.show()
	if val ==1:
		frames = panel.value('range:')
		return frames
	
def makeProxyUI():
	sel = nuke.selectedNodes()
	if  sel:
		panel = nuke.Panel('Nuke Converter')
		panel.addFilenameSearch("output folder: ","")
		panel.addBooleanCheckBox("same path as source", 0)
		panel.setWidth(400)
		fileTypes = 'tif exr jpeg'
		colorspaces = 'linear Cineon sRGB'
		panel.addEnumerationPulldown("format: ", fileTypes)
		panel.addEnumerationPulldown("from: ", colorspaces)
		panel.addEnumerationPulldown("to: ", colorspaces)
		panel.addSingleLineInput("scale factor: ", "1")
		panel.addBooleanCheckBox("create read node", 0)
		panel.addBooleanCheckBox("keep alpha channel", 0)
		panel.addBooleanCheckBox("Image Sequence", 0)
		panel.addBooleanCheckBox("Overwrite", 0)
		
		val = panel.show()
		if val:
			
			filePath = panel.value("output folder: ")
			filePathBool = int(panel.value("same path as source"))
			fileType = panel.value("format: ")
			convertFrom = panel.value("from: ")
			convertTo = panel.value("to: ")
			scaleFactor = float(panel.value("scale factor: "))
			createRead = int(panel.value("create read node"))
			alpha = int(panel.value("keep alpha channel"))
			anim = int(panel.value("Image Sequence"))
			overwrite = int(panel.value("Overwrite"))
			
			for node in sel:
				if node.Class() in ('Read', 'Write', 'hubRead', 'hubWrite'):
					makeProxy(node, filePath, filePathBool, fileType, convertFrom, convertTo, scaleFactor, createRead, alpha, anim, overwrite)
					
					
					
