import os
import sys
import img2pdf
import zipfile
from datetime import datetime

# comic parser
class ComicParser:

    # declare list of valid extensions
    allowedExtensions = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]

    # init method or constructor
    def __init__(self, argv=None):
        self.index = 1
        self.images = []

        if argv is None:
            argv = sys.argv[1:]

        args = self.parseArguments(argv)
        if args is None:
            return

        # extract all files
        self.extractFiles(args["folder"])
        # build PDFs
        self.buildPDFs(
            args["folder"],
            args["title"],
            args["author"],
            args["subject"],
            args["keywords"],
            args["publisher"],
            args["series"],
        )

    def parseArguments(self, argv):
        if (len(argv) == 0 or "-h" in argv or "--help" in argv):
            self.printUsage()
            return None

        if (len(argv) < 3):
            print("format 'folder' 'comic name' 'author name'")
            self.printUsage()
            return None

        args = {
            "folder": argv[0],
            "title": argv[1],
            "author": argv[2],
            "subject": None,
            "keywords": None,
            "publisher": None,
            "series": None
        }

        optionalMapping = {
            "--subject": "subject",
            "--keywords": "keywords",
            "--publisher": "publisher",
            "--series": "series"
        }

        position = 3
        while position < len(argv):
            option = argv[position]
            if option not in optionalMapping:
                print("Unknown option: " + option)
                self.printUsage()
                return None
            if (position + 1) >= len(argv):
                print("Missing value for option: " + option)
                self.printUsage()
                return None
            args[optionalMapping[option]] = argv[position + 1]
            position += 2

        return args

    def printUsage(self):
        print("Usage:")
        print("comic-parser <folder> \"<comic name>\" \"<author>\" [--subject \"<subject>\"] [--keywords \"<k1,k2>\"] [--publisher \"<publisher>\"] [--series \"<series>\"]")

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
    def buildPDFs(self, folder: str, name: str, author: str, subject: str = None, keywords: str = None, publisher: str = None, series: str = None):
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
            # calculate chapter / volume index
            comicIndex = self.getComicIndex()
            # declare pdf name
            pdfName = name + " " + comicIndex + " - " + author + ".pdf"
            # print info
            print("Parsing: " + pdfName)
            # make pdf with images
            with open(folder + "/" + pdfName, "wb") as manga:
                manga.write(self.buildPDF(self.images, self.buildPdfMetadata(name, author, comicIndex, subject, keywords, publisher, series)))
            # update comic index
            self.index += 1

    def buildPdfMetadata(self, name: str, author: str, comicIndex: str, subject: str = None, keywords: str = None, publisher: str = None, series: str = None):
        now = datetime.now()

        finalSubjectParts = []
        if subject:
            finalSubjectParts.append(subject)
        finalSubjectParts.append("Chapter/Volume " + comicIndex)
        if series:
            finalSubjectParts.append("Series: " + series)
        if publisher:
            finalSubjectParts.append("Publisher: " + publisher)

        finalKeywords = []
        if keywords:
            finalKeywords.extend([value.strip() for value in keywords.split(",") if value.strip()])
        finalKeywords.append("chapter-" + comicIndex)
        if series:
            finalKeywords.append(series)
        if publisher:
            finalKeywords.append(publisher)

        return {
            "title": name + " " + comicIndex,
            "author": author,
            "creationdate": now,
            "moddate": now,
            "subject": " | ".join(finalSubjectParts),
            "keywords": finalKeywords,
            "creator": "comic-parser",
            "producer": "comic-parser"
        }

    def buildPDF(self, images, metadata):
        currentMetadata = dict(metadata)
        skippedMetadata = []

        try:
            return img2pdf.convert(images, **currentMetadata)
        except TypeError as error:
            if "unexpected keyword argument" not in str(error):
                raise

        for _ in range(len(currentMetadata) + 1):
            try:
                if len(skippedMetadata) > 0:
                    print("Skipping unsupported metadata keys: " + ", ".join(skippedMetadata))
                return img2pdf.convert(images, **currentMetadata)
            except TypeError as error:
                if "unexpected keyword argument" not in str(error):
                    raise
                messageParts = str(error).split("'")
                if len(messageParts) < 2:
                    raise
                unsupportedKey = messageParts[1]
                if unsupportedKey not in currentMetadata:
                    raise
                currentMetadata.pop(unsupportedKey, None)
                skippedMetadata.append(unsupportedKey)

        raise RuntimeError("Could not build PDF metadata with the current img2pdf version.")

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
