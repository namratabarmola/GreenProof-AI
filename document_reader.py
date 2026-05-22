import cv2
import numpy as np
import pytesseract
from PIL import Image
import PyPDF2

def extract_text(uploaded_file):
    text = ""

    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    elif uploaded_file.name.endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(uploaded_file)

        # Convert PIL → OpenCV
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise removal
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Threshold for better OCR
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # OCR
        text = pytesseract.image_to_string(
            thresh,
            lang="hin+eng",
            config="--psm 6"
        )

    return text