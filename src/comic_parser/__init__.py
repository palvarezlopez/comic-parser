"""
This module serves as the entry point for the ComicParser package. 
It imports the ComicParser class from the comic_parser module and defines a function to run the parser. When this module is executed as a script, it will create an instance of the ComicParser class, which will start the parsing process.
"""
from .comic_parser import ComicParser


def run_parser():
    """
    Runs the ComicParser by creating an instance of the ComicParser class. 
    This function serves as the entry point for executing the comic parser when the module is run as a script.
    """
    ComicParser()
