from IPython.display import display_html
from PIL import Image as PILImage
from openpyxl import load_workbook
from io import BytesIO
import cv2
from img2table.document import Image

from img2table.ocr import TesseractOCR

# Instantiation of OCR
# , tessdata_dir="/Program Files (x86)/Tesseract-OCR/"
ocr = TesseractOCR(n_threads=1, lang="eng")

# Instantiation of document, either an image or a PDF
doc = Image(src="./table (1).jpg")

# Table extraction
extracted_tables = doc.extract_tables(ocr=ocr,
                                      implicit_rows=False,
                                      implicit_columns=False,
                                      borderless_tables=False,
                                      min_confidence=50)