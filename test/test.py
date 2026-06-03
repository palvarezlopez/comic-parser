
import sys
import zipfile
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from comic_parser import ComicParser


def create_sample_cbz(inputFolder: Path) -> Path:
    chapterFolder = inputFolder / "chapter_01_src"
    chapterFolder.mkdir(parents=True, exist_ok=True)
    imagePaths = []
    for index in range(1, 4):
        imagePath = chapterFolder / f"{index:03}.jpg"
        image = Image.new("RGB", (800, 1200), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((40, 40), f"Sample page {index}", fill=(0, 0, 0))
        image.save(imagePath)
        imagePaths.append(imagePath)

    cbzPath = inputFolder / "chapter_01.cbz"
    with zipfile.ZipFile(cbzPath, "w") as cbzFile:
        for imagePath in imagePaths:
            cbzFile.write(imagePath, imagePath.name)
    for imagePath in imagePaths:
        imagePath.unlink()
    chapterFolder.rmdir()
    return cbzPath


def read_pdf_metadata(pdfPath: Path):
    try:
        import pikepdf
    except ImportError:
        print("Install pikepdf to inspect metadata: pip install pikepdf")
        return None

    with pikepdf.open(pdfPath) as pdf:
        info = pdf.docinfo
        return {
            "title": str(info.get("/Title", "")),
            "author": str(info.get("/Author", "")),
            "subject": str(info.get("/Subject", "")),
            "creator": str(info.get("/Creator", "")),
            "producer": str(info.get("/Producer", "")),
            "creationDate": str(info.get("/CreationDate", "")),
            "modDate": str(info.get("/ModDate", ""))
        }


def main():
    comicName = "Example Comic"
    author = "Example Author"

    with tempfile.TemporaryDirectory() as tempFolder:
        inputFolder = Path(tempFolder)
        create_sample_cbz(inputFolder)

        parser = ComicParser()
        parser.runFromArgs(["comic-parser", str(inputFolder), comicName, author])

        outputPdf = inputFolder / f"{comicName} 01 - {author}.pdf"
        if not outputPdf.exists():
            raise RuntimeError(f"Expected output PDF was not generated at {outputPdf}")

        metadata = read_pdf_metadata(outputPdf)
        if metadata is None:
            return

        print("Generated PDF:", outputPdf)
        print("Embedded metadata:", metadata)

        assert metadata["title"] == f"{comicName} 01"
        assert metadata["author"] == author
        assert "01" in metadata["subject"]
        assert metadata["creator"] == "comic-parser"
        assert metadata["producer"] == "comic-parser"
        assert metadata["creationDate"] != ""
        assert metadata["modDate"] != ""

        print("Metadata validation OK")


if __name__ == "__main__":
    main()
