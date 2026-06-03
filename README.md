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

Optional metadata arguments:

```bash
comic-parser <folder> "<comic name>" "<author>" \
  --subject "<subject>" \
  --keywords "<k1,k2>" \
  --publisher "<publisher>" \
  --series "<series>"
```

Arguments:

- `folder`: directory containing the `.zip` or `.cbz` files to parse.
- `comic name`: base name used for the generated PDF files.
- `author`: author name included in the generated PDF file names.
- `--subject`: optional PDF subject metadata.
- `--keywords`: optional comma-separated PDF keywords.
- `--publisher`: optional publisher/editorial metadata included in the subject/keywords.
- `--series`: optional series metadata included in the subject/keywords.

Generated PDFs now include embedded metadata (title with chapter index, author, subject/keywords, creation/modification date, creator, producer), not only metadata in the file name.

## Example project (`test/`)

Run the executable example script that creates a sample `.cbz`, generates a PDF, and verifies embedded metadata:

```bash
python test/test.py
```