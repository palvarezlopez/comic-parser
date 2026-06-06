```bash
comic-parser <folder> "<comic name>" "<author>"
python -m comic_parser <folder> "<comic name>" "<author>"
```

Arguments:

- `folder`: directory containing the `.zip` or `.cbz` files to parse.
- `comic name`: base name used for the generated PDF files.
- `author`: author name included in the generated PDF file names.

Generated PDFs now include embedded metadata (title with chapter index, author, subject/keywords, creation/modification date, creator, producer), not only metadata in the file name.

## Example project (`test/`)

Run the executable example script that creates a sample `.cbz`, generates a PDF, and verifies embedded metadata:

```bash
python test/test.py
```