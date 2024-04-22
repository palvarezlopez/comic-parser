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
        # extract all files
        self.extractFiles(comicFolder)
        # read all elements of comic folder
        for pathRoot, subdirsRoot, filesRoot in os.walk(comicFolder):
            for dirNames in subdirsRoot:
                imagenes = []

                for path, subdirs, files in os.walk(dirNames):
                    for name in files:
                        if ".py" not in name and ".pdf" not in name and ".db" not in name:
                            imagenes.append(os.path.join(path, name))

                imagenes.sort()

                with open(os.path.basename(os.getcwd() + dirNames) + ".pdf", "wb") as manga:
                    manga.write(img2pdf.convert(imagenes))

    # extract files
    def extractFiles(self, comicFolder: str):
        files = []
        # get all  files        
        for (dirpath, dirnames, filenames) in os.walk(comicFolder):
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
        #    