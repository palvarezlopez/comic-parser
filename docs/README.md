# Usage

Install the project from the repository root:

```bash
pip install .
```

Run the parser with a folder that contains `.zip` or `.cbz` files, the comic name, and the author:

```bash
comic-parser <folder> "<comic name>" "<author>"
```

Optional metadata arguments can be passed while keeping the 3-argument command compatible:

```bash
comic-parser <folder> "<comic name>" "<author>" \
  --subject "<subject>" \
  --keywords "<k1,k2>" \
  --publisher "<publisher>" \
  --series "<series>"
```

The generated PDFs embed metadata in the document itself (title with chapter/volume index, author, subject, keywords, creation/modification dates, creator and producer).

You can also run it as a module:

```bash
python -m comic_parser <folder> "<comic name>" "<author>"
```

## Example under `test/`

The `test/test.py` script is an executable sample project included in `test/test.pyproj` (and therefore in `Comic-parser.sln`). It creates a sample `.cbz`, runs the parser with metadata options and validates embedded PDF metadata.

```bash
python test/test.py
```
