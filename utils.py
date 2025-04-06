import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image):
    results = reader.readtext(np.array(image))
    results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))  # sort top to bottom, then left to right
    return [text for _, _, text in results]
