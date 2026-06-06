"""
comic_parser.py is a script that defines the ComicParser class, which is responsible for parsing comic files from a specified folder, extracting them if necessary, and building PDFs for each comic folder found in the directory.
"""
import os
import sys
from typing_extensions import Buffer
import zipfile
from datetime import datetime
from typing import Any
import img2pdf  # type: ignore[import-untyped]

# comic parser
class ComicParser:
    """
    ComicParser is a class that parses comic files (with allowed extensions) from a specified folder, extracts them if necessary, and builds PDFs for each comic folder found in the directory. 
    It also handles command line arguments for specifying the folder, comic name, and author name.
    """

    def __init__(self, argv: list[str] | None = None):
        """
        Initializes the ComicParser, parses command line arguments, extracts comic files, and builds PDFs for each comic folder found in the specified directory.
        """
        # all comics starts with index 1
        self.index: int = 1
        # list of image paths for the current comic
        self.image_paths: list[str] = []
        # if no arguments are provided, use command line arguments
        if argv is None:
            argv = sys.argv[1:]
        # parse arguments
        args: dict[str, str] | None = self.parse_arguments(argv)
        if args is None:
            return
        # extract all files
        self.extract_files(args["folder"])
        # build PDFs
        self.build_pdfs(
            args["folder"],
            args["title"],
            args["author"],
        )

    def parse_arguments(self, argv: list[str]) -> dict[str, str] | None:
        """
        Parses the command line arguments and returns a dictionary of the parsed values. 
        If the arguments are invalid or if help is requested, it prints the usage instructions and returns None.
        """
        # show help
        if (len(argv) == 0) or ("-h" in argv) or ("--help" in argv):
            self.print_usage()
            return None
        # ensure all required arguments are provided
        if len(argv) < 3:
            print("format 'folder' 'comic name' 'author name'")
            self.print_usage()
            return None
        # parse arguments
        args: dict[str, str] = {
            "folder": argv[0],
            "title": argv[1],
            "author": argv[2],
        }
        return args

    def print_usage(self):
        """
        Prints the usage instructions for the comic parser.
        """
        print("Usage:")
        print("comic-parser <folder> \"<comic name>\" \"<author>\"")

    def extract_files(self, folder: str):
        """
        Extracts all comic files (with allowed extensions) from the specified folder and its subdirectories, and organizes them into folders based on their names.
        """
        files: list[str] = []
        # get all  files
        for (_dirpath, _directories, filenames) in os.walk(folder):
            files.extend(filenames)
        # declare list of allowed extensions
        file_extensions = [".zip", ".cbz"]
        # extract files
        for file_extension in file_extensions:
            for file in files:
                if file_extension in file:
                    # declare file without extension
                    file_without_extension = file.replace(file_extension, '')
                    # create folder
                    os.mkdir(file_without_extension)
                    # extract file
                    with zipfile.ZipFile(folder + "/" + file, 'r') as zip_ref:
                        zip_ref.extractall(folder + "/" + file_without_extension)

    def build_pdfs(self, folder: str, name: str, author: str):
        """
        Builds PDFs for each comic folder found in the specified directory.
        """
        # read all folders from comicFolder
        comic_folders = self.list_folders(folder)
        # iterate over all comic folders
        for comic_folder in comic_folders:
            # reset image vector
            self.image_paths = []
            # list images recursive
            self.list_images_recursive(comic_folder)
            # sort images
            self.image_paths.sort()
            # calculate chapter / volume index
            comic_index = self.get_comic_index()
            # declare pdf name
            pdf_name = name + " " + comic_index + " - " + author + ".pdf"
            # print info
            print("Parsing: " + pdf_name)
            # make pdf with images
            with open(folder + "/" + pdf_name, "wb") as manga:
                manga.write(self.build_pdf(self.image_paths, self.get_pdf_metadata(name, author, comic_index)))
            # update comic index
            self.index += 1

    def get_pdf_metadata(self, name: str, author: str, index: str) -> dict[str, Any]:
        """
        Returns the metadata for the PDF, including title, author, and creation date.
        """
        return {
            "title": name + " " + index,
            "author": author,
            "creationdate": datetime.now(),
        }

    def build_pdf(self, images: list[str] , metadata: dict[str, Any]) -> Buffer:
        """
        Builds a PDF from the given images and metadata, while ensuring compatibility with different versions of img2pdf.
        """
        try:
            return img2pdf.convert(images, **metadata)
        except TypeError as error:
            if "unexpected keyword argument" not in str(error):
                raise
        # throw exception if we couldn't build the PDF with any of the metadata keys
        raise RuntimeError("Could not build PDF metadata with the current img2pdf version.")

    def get_comic_index(self) -> str:
        """
        Returns the comic index as a string, with leading zeros if necessary.
        """
        # if index is less than 10, add leading zero (we asume that we don't have a comic with more than 99 chapters / volumes)
        if self.index < 10:
            return "0" + str(self.index)
        return str(self.index)

    def list_folders(self, root_folder: str) -> list[str]:
        """
        Returns a list of folders in the specified root folder.
        """
        # list all folders in rootFolder and return them as a list
        return [os.path.join(root_folder, folder) for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]


    def list_images_recursive(self, path: str) -> None:
        """
        Recursively lists all images in the specified path and its subdirectories, and adds them to the images list.
        """
        # declare list of valid extensions
        image_extensions: list[str] = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
        # iterate over all entries in the directory
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                # if the entry is a directory, recursively list images in that directory
                self.list_images_recursive(full_path)
            else:
                # ensure that the file has a valid image extension before adding it to the list
                for image_extension in image_extensions:
                    if entry.lower().endswith(image_extension):
                        self.image_paths.append(full_path)
