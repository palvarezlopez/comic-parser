import os
import sys
import img2pdf
import zipfile
import datetime
from PIL import Image

# comic parser
class ComicParser:

    # init method or constructor
    def __init__(self):
        # comic index
        self.index = 1
        # declare image vector
        self.images = []

    # parse args and run parser
    def runFromArgs(self, args):
        if (len(args) != 4):
            print ("format 'folder' 'comic name' 'author name'")
            return
        # comic folder
        folder = args[1]
        # comic title
        title = args[2]
        # comic author
        author = args[3]
        # extract all files
        self.extractFiles(folder)
        # build PDFs
        self.buildPDFs(folder, title, author)

    # run parser from sys args
    def runFromCli(self):
        self.runFromArgs(sys.argv)

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
                    outputFolder = folder + "/" + fileWithoutExtension
                    os.makedirs(outputFolder, exist_ok=True)
                    # extract file
                    with zipfile.ZipFile(folder + "/" + file, 'r') as zip_ref:
                        zip_ref.extractall(outputFolder)

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
            # calculate comic index
            comicIndex = self.getComicIndex()
            # declare pdf name
            pdfName = name + " " + comicIndex + " - " + author + ".pdf"
            # print info
            print("Parsing: " + pdfName)
            # build metadata
            metadata = self.buildPdfMetadata(name, author, comicIndex)
            # make pdf with images
            with open(folder + "/" + pdfName, "wb") as manga:
                manga.write(self.buildPdfBytes(self.images, metadata))
            # update comic index
            self.index += 1

    # build metadata for PDF
    def buildPdfMetadata(self, name: str, author: str, comicIndex: str):
        now = datetime.datetime.now(datetime.timezone.utc)
        return {
            "title": name + " " + comicIndex,
            "author": author,
            "subject": name + " chapter " + comicIndex,
            "keywords": [name, author, "chapter " + comicIndex, "volume " + comicIndex],
            "creator": "comic-parser",
            "producer": "comic-parser",
            "creationdate": now,
            "moddate": now
        }

    # build PDF bytes and fallback if some metadata keys are unsupported
    def buildPdfBytes(self, images, metadata):
        metadataKeys = ["keywords", "subject", "producer", "creator", "moddate", "creationdate", "author", "title"]
        for removedKeys in range(0, len(metadataKeys) + 1):
            metadataToUse = dict(metadata)
            for key in metadataKeys[:removedKeys]:
                if (key in metadataToUse):
                    del metadataToUse[key]
            try:
                return img2pdf.convert(images, **metadataToUse)
            except TypeError:
                continue
        return img2pdf.convert(images)

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