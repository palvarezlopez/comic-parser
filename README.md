# comic-parser

Python utility for building comic PDFs from `.zip` and `.cbz` archives.

## Installation

```bash
pip install comic-parser
```

## Usage

```bash
comic-parser <folder> "<comic name>" "<author>"
python -m comic_parser <folder> "<comic name>" "<author>"
```

Arguments:

- `folder`: directory containing the `.zip` or `.cbz` files to parse.
- `comic name`: base name used for the generated PDF files.
- `author`: author name included in the generated PDF file names.