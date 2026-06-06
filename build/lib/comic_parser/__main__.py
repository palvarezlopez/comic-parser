"""
This module serves as the entry point for the comic parser application.
When the module is run as a script, this block will execute. 
It calls the runParser function, which creates an instance of the ComicParser class and starts the parsing process.
"""
from . import run_parser

if __name__ == "__main__":
    run_parser()
