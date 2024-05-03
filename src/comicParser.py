import os
import sys
import img2pdf
import zipfile
from PIL import Image

# comic parser
class ComicParser:

    # init method or constructor
    def __init__(self):
        if (len(sys.argv) != 4):
            print ("format 'folder' 'comic name' 'author name'")
        else:
            # comic folder
            folder = sys.argv[1]
            # comic title
            title = sys.argv[2]
            # comic author
            author = sys.argv[3]
            # extract all files
            #self.extractFiles(comicFolder)
            # build PDFs
            self.buildPDFs(folder, title, author)

    # extract files
    def extractFiles(self, folder: str):
        files = []
        # get all  files
        for (dirpath, directories, filenames) in os.walk(folder):
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
                    with zipfile.ZipFile(folder + "/" + file, 'r') as zip_ref:
                        zip_ref.extractall(folder + "/" + fileWithoutExtension)

    # build PDF
    def buildPDFs(self, folder: str, name: str, author: str):
        # read all folders from comicFolder
        comicFolders = self.listFolders(folder)
        # iterate over all comic folders
        for comicFolder in comicFolders:
            # reset image vector
            self.images = []
            # list images recursive
            self.listImagesRecursive(comicFolder)
            # sort images
            self.images.sort()
            # declare pdf name
            pdfName = name + " " + self.getComicIndex() + " - " + author + ".pdf"
            # print info
            print("Parsing: " + pdfName)
            # make pdf with i mages
            with open(folder + "/" + pdfName, "wb") as manga:
                manga.write(img2pdf.convert(self.images))
            # update comic index
            self.index += 1

    # calculate comic index
    def getComicIndex(self) -> str:
        if (self.index < 10):
            return "0" + str(self.index)
        else:
            return str(self.index)

    # display images
    def displayImages(self):
        for image in self.images:
            print(image)

    # list folders
    def listFolders(self, rootFolder: str):
        files_dir = [
            os.path.join(rootFolder, folder) for folder in os.listdir(rootFolder) if os.path.isdir(os.path.join(rootFolder, folder))
        ]
        return files_dir

    # list images recursive
    def listImagesRecursive(self, path):
        for entry in os.listdir(path):
            fullPath = os.path.join(path, entry)
            if os.path.isdir(fullPath):
                self.listImagesRecursive(fullPath)
            else:
                self.images.append(fullPath)

    # declare list of valid extensions
    allowedExtensions = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]

    # comic index
    index = 1

    # declare image vector
    images = []