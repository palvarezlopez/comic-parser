import os
import sys
import img2pdf
import zipfile
from PIL import Image

# comic parser
class ComicParser:

    # init method or constructor
    def __init__(self):
        # comic folder
        comicFolder = sys.argv[1]
        # declare comic name
        comicName = sys.argv[2]
        if (comicName == ""):
            print ("specify comic name")
        else:                              
            # extract all files
            #self.extractFiles(comicFolder)
            # build PDFs
            self.buildPDFs(comicFolder, comicName)        

    # extract files
    def extractFiles(self, comicFolder: str):
        files = []
        # get all  files        
        for (dirpath, directories, filenames) in os.walk(comicFolder):
            files.extend(filenames)
        # declare list of allowed extensions
        extensions = [".zip", ".cbz"]            
        # extract files
        for extension in extensions:
            for file in files:
                if (extension in file):
                    # declare file without extension
                    fileWithoutExtension = file.replace(extension, '')                    
                    # create folder
                    os.mkdir(fileWithoutExtension)                          
                    # extract file
                    with zipfile.ZipFile(comicFolder + "/" + file, 'r') as zip_ref:
                        zip_ref.extractall(comicFolder + "/" + fileWithoutExtension)
                        
    # extract files
    def buildPDFs(self, comicFolder: str, comicName: str):      
        # read all folders from comicFolder
        for (dirpath, directories, filenames) in os.walk(comicFolder):
            # iterate over every directory 
            for directory in directories:
                # first clear images
                self.images = []                  
                # read all images using os.walk
                for (dirSubPath, subdirs, imageNames) in os.walk(comicFolder + "/" + directory):
                    for imageName in imageNames:
                        # iterate over allowed extensiones
                        for allowedExtension in self.allowedExtensions:                     
                            if allowedExtension in imageName:
                                self.images.append(os.path.join(dirSubPath, imageName))
            # sort images                              
            self.images.sort()
            # make pdf with i mages
            with open(comicFolder + "/" + comicName + " - volume " + self.getComicIndex(directories) + ".pdf", "wb") as manga:
                manga.write(img2pdf.convert(self.images))
            # update index
            self.index += 1                   

    # calculate comic index
    def getComicIndex(self, directories) -> str:
        return "0" + str(self.index)     
    
    # display images
    def displayImages(self):
        for image in self.images:
            print(image)                          

    # declare list of valid extensions
    allowedExtensions = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]                       
        
    # comic index        
    index = 1  

    # declare image vector                
    images = []                             