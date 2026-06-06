
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from comic_parser.comic_parser import ComicParser

try:
    import pikepdf
except ImportError:
    pikepdf = None


def build_sample_cbz(output_folder: Path):
    source_folder = output_folder / "chapter_01_source"
    source_folder.mkdir(parents=True, exist_ok=True)

    for image_index in range(1, 4):
        image_path = source_folder / f"{image_index:02d}.jpg"
        image = Image.new("RGB", (640, 900), color="white")
        drawer = ImageDraw.Draw(image)
        drawer.text((30, 30), f"Page {image_index}", fill="black")
        image.save(image_path)

    cbz_path = output_folder / "chapter_01.cbz"
    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED) as cbz_file:
        for image_path in sorted(source_folder.iterdir()):
            cbz_file.write(image_path, arcname=image_path.name)

    shutil.rmtree(source_folder)


def read_metadata(pdf_path: Path):
    if pikepdf is None:
        print("Install pikepdf to inspect embedded metadata in this example.")
        return

    with pikepdf.open(str(pdf_path)) as pdf:
        info = pdf.docinfo
        print("Embedded metadata:")
        print("  Title   :", info.get("/Title"))
        print("  Author  :", info.get("/Author"))

        assert str(info.get("/Title")) == "Demo Comic 01", f"Expected title 'Demo Comic 01' but got '{info.get('/Title')}'"
        assert str(info.get("/Author")) == "Demo Author", f"Expected author 'Demo Author' but got '{info.get('/Author')}'"


def main():
    with tempfile.TemporaryDirectory() as temp_folder:
        working_folder = Path(temp_folder)
        build_sample_cbz(working_folder)

        original_folder = os.getcwd()
        os.chdir(str(working_folder))
        try:
            ComicParser([
                str(working_folder),
                "Demo Comic",
                "Demo Author",
            ])
        finally:
            os.chdir(original_folder)

        output_pdf = working_folder / "Demo Comic 01 - Demo Author.pdf"
        if not output_pdf.exists():
            raise RuntimeError("Output PDF was not generated.")
        print("Generated PDF:", output_pdf)
        read_metadata(output_pdf)
        print("Example finished correctly.")


if __name__ == "__main__":
    main()
