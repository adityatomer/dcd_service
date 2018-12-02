from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

import logging as logger
# import mdtraj as md
import mdtraj as md
import numpy as np

from django.template import loader
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.utils.encoding import smart_str

# # def getLogging(filePath):
logger.basicConfig(
	format="%(asctime)s [%(threadName)-12.12s %(lineno)d] [%(levelname)-5.5s]  %(message)s",
	handlers=[
	logger.FileHandler("{0}/{1}.log".format("./", "app.log")),
	logger.StreamHandler()
	],
	level=logger.INFO)

def convert(infile,topologyFile):
    t=md.load_dcd(infile, top=topologyFile)
    nparray=t.xyz
    xyz=np.squeeze(np.multiply(nparray,10))
    
    return xyz


def simpleUpload(request):
	logger.info("reached here in view")

	if request.method=='POST' and request.FILES['dcd_file'] and request.FILES['pdb_file']:
		dcdFile=request.FILES["dcd_file"]
		pdbFile=request.FILES["pdb_file"]
		fs = FileSystemStorage()
		dcdFile = fs.save("temp_files/"+dcdFile.name, dcdFile)
		pdbFile = fs.save("temp_files/"+pdbFile.name, pdbFile)
		dcdFile_url = fs.url(dcdFile)
		pdbFile_url = fs.url(pdbFile)
		#Name and Path for file where content will be written.
		writeFileName = (dcdFile.split(".dcd")[0]).split("temp_files/")[1]+".txt"
		writepath = "temp_files"
		wholePath = writepath+"/"+writeFileName
		logger.info("wholePath: "+wholePath)
		#Convert dcd file in XYZ format
		content=str(convert(dcdFile_url,pdbFile_url))
		
		#Save content into temp file.
		with open(wholePath, 'a') as the_file:
			the_file.write(content)

		#Serve file using http response.
		response = HttpResponse(content, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(writeFileName)
		response['X-Sendfile'] = smart_str(wholePath)
		return response

		
		


def index(request):
	context={"ww":"ww"}
	return render(request, 'index.html', context,)
