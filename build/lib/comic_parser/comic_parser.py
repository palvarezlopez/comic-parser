"""
comic_parser.py is a script that defines the ComicParser class, which is responsible for parsing comic files from a specified folder, extracting them if necessary, and building PDFs for each comic folder found in the directory.
"""
import os
import sys
import re
import argparse
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
        args = self.parse_arguments(argv)
        if args is None:
            return
        # extract all files
        self.extract_files(args["folder"])
        # build PDFs
        self.build_pdfs(
            args["folder"],
            args["title"],
            args["author"],
            args["subject"],
            args["keywords"],
            args["publisher"],
            args["series"],
        )

    def build_argument_parser(self) -> argparse.ArgumentParser:
        """
        Builds and returns the argument parser for the comic parser command.
        """
        parser = argparse.ArgumentParser(
            prog="comic-parser",
            description="Build comic PDFs from .zip and .cbz files."
        )
        parser.add_argument("folder", help="Folder containing .zip/.cbz comic archives.")
        parser.add_argument("title", help="Comic title used in generated PDF names and metadata.")
        parser.add_argument("author", help="Comic author used in generated PDF names and metadata.")
        parser.add_argument("--subject", default=None, help="Additional subject text to embed in PDF metadata.")
        parser.add_argument("--keywords", default=None, help="Additional comma-separated keywords for PDF metadata.")
        parser.add_argument("--publisher", default=None, help="Publisher name to include in PDF metadata.")
        parser.add_argument("--series", default=None, help="Series name to include in PDF metadata.")
        return parser

    def parse_arguments(self, argv: list[str]) -> dict[str, str | None] | None:
        """
        Parses the command line arguments and returns a dictionary of the parsed values. 
        If the arguments are invalid or if help is requested, it prints the usage instructions and returns None.
        """
        # show help
        if len(argv) == 0:
            self.print_usage()
            return None
        parser = self.build_argument_parser()
        try:
            parsed_args = parser.parse_args(argv)
        except SystemExit:
            return None
        args: dict[str, str | None] = {
            "folder": parsed_args.folder,
            "title": parsed_args.title,
            "author": parsed_args.author,
            "subject": parsed_args.subject,
            "keywords": parsed_args.keywords,
            "publisher": parsed_args.publisher,
            "series": parsed_args.series,
        }
        return args

    def print_usage(self):
        """
        Prints the usage instructions for the comic parser.
        """
        self.build_argument_parser().print_help()

    def extract_files(self, folder: str):
        """
        Extracts all comic files (with allowed extensions) from the specified folder and its subdirectories, and organizes them into folders based on their names.
        """
        # declare list of allowed extensions
        file_extensions = {".zip", ".cbz"}
        # extract files
        for dirpath, _directories, filenames in os.walk(folder):
            for file in filenames:
                file_without_extension, file_extension = os.path.splitext(file)
                if file_extension.lower() not in file_extensions:
                    continue
                source_path = os.path.join(dirpath, file)
                destination_path = os.path.join(dirpath, file_without_extension)
                os.makedirs(destination_path, exist_ok=True)
                with zipfile.ZipFile(source_path, "r") as zip_ref:
                    zip_ref.extractall(destination_path)

    def build_pdfs(
        self,
        folder: str,
        name: str,
        author: str,
        subject: str | None = None,
        keywords: str | None = None,
        publisher: str | None = None,
        series: str | None = None,
    ):
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
            with open(os.path.join(folder, pdf_name), "wb") as manga:
                manga.write(
                    self.build_pdf(
                        self.image_paths,
                        self.get_pdf_metadata(
                            name,
                            author,
                            comic_index,
                            subject,
                            keywords,
                            publisher,
                            series,
                        ),
                    )
                )
            # update comic index
            self.index += 1

    def get_pdf_metadata(
        self,
        name: str,
        author: str,
        index: str,
        subject: str | None = None,
        keywords: str | None = None,
        publisher: str | None = None,
        series: str | None = None,
    ) -> dict[str, Any]:
        """
        Returns the metadata for the PDF, including title, author, and creation date.
        """
        chapter_subject = f"Chapter/Volume {index}"
        subject_parts = [chapter_subject]
        if subject:
            subject_parts.append(subject)
        if publisher:
            subject_parts.append(publisher)
        if series:
            subject_parts.append(series)

        chapter_keyword = f"chapter-{index}"
        keyword_parts = [chapter_keyword]
        if keywords:
            keyword_parts.append(keywords)
        if publisher:
            keyword_parts.append(publisher)
        if series:
            keyword_parts.append(series)

        now = datetime.now()
        return {
            "title": name + " " + index,
            "author": author,
            "subject": ", ".join(subject_parts),
            "keywords": keyword_parts,
            "creator": "comic-parser",
            "producer": "comic-parser",
            "creationdate": now,
            "moddate": now,
        }

    def build_pdf(self, images: list[str] , metadata: dict[str, Any]) -> Buffer:
        """
        Builds a PDF from the given images and metadata, while ensuring compatibility with different versions of img2pdf.
        """
        current_metadata = metadata.copy()
        while True:
            try:
                return img2pdf.convert(images, **current_metadata)
            except TypeError as error:
                message = str(error)
                if "unexpected keyword argument" not in message:
                    raise
                unexpected = re.search(r"unexpected keyword argument '([^']+)'", message)
                if unexpected is None:
                    raise RuntimeError(
                        f"Could not parse unsupported metadata key from img2pdf. Original error: {message}"
                    )
                unsupported_key = unexpected.group(1)
                if unsupported_key not in current_metadata:
                    raise RuntimeError(
                        f"img2pdf rejected unsupported metadata key '{unsupported_key}'. Original error: {message}"
                    )
                current_metadata.pop(unsupported_key)

    def get_comic_index(self) -> str:
        """
        Returns the comic index as a string, with leading zeros if necessary.
        """
        return f"{self.index:02d}"

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
