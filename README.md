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

Generated PDFs include embedded metadata derived from the same 3 arguments and the internal chapter index:

- `Title`: `<comic name> <chapter index>`
- `Author`: `<author>`
- `Subject`/`Keywords`: include chapter or volume index information
- `Creator`/`Producer`: `comic-parser`
- `CreationDate` and `ModDate`: current generation date

## Example project (test/)

Run the example script in `test/test.py` to generate a sample `.cbz`, parse it and validate embedded PDF metadata:

```bash
python test/test.py
```