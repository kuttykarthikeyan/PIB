from django.shortcuts import render
from ultralytics import YOLO

# model = YOLO(r"model_ocr\best_model_article.pt")
# classes_list = model.names

def image_to_text_OCR(image_path):
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image=image_path)
    return text



# Create your views here.
def ocr(request):
    return render(request, 'ocr/ocr.html')
