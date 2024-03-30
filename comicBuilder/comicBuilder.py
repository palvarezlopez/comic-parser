import os
import img2pdf
from PIL import Image

for pathRoot, subdirsRoot, filesRoot in os.walk('./'):
    for dirNames in subdirsRoot:
        imagenes = []

        for path, subdirs, files in os.walk(dirNames):
            for name in files:
                if ".py" not in name and ".pdf" not in name and ".db" not in name:
                    imagenes.append(os.path.join(path, name))

        imagenes.sort()

        with open(os.path.basename(os.getcwd() + dirNames) + ".pdf", "wb") as manga:
            manga.write(img2pdf.convert(imagenes))
