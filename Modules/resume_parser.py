import fitz
import cv2
import pytesseract
from PIL import Image


def extract_text_from_pdf(file_path):
    text = ""
    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    return text


def extract_text_from_image(file_path):
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text


if __name__ == "__main__":
    pdf_path = "Resumes/sample_resume.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    print("--- PDF OUTPUT ---")
    print(pdf_text[:500])

    img_path = "Resumes/resume.png"
    img_text = extract_text_from_image(img_path)
    print("--- IMAGE OUTPUT ---")
    print(img_text[:500])