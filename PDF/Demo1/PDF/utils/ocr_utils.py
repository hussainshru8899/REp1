import tempfile
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


def ocr_pdf_to_text(pdf_path, dpi=200):
    pages = convert_from_path(pdf_path, dpi=dpi)
    texts = []
    for p in pages:
        txt = pytesseract.image_to_string(p)
        texts.append(txt)
    return texts


def ocr_image_to_text(img_path):
    img = Image.open(img_path)
    return pytesseract.image_to_string(img)
