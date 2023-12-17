from django.shortcuts import render
from .models import *
import datetime
# model = YOLO(r"model_ocr\best_model_article.pt")
# classes_list = model.names



# Create your views here.
def ocr(request):
    papers = DailyOCR.objects.filter(date=datetime.datetime.now().date())
    return render(request, 'ocr/ocr.html',{
        "papers":papers
    })


def view_pages(request,id):
    paper = DailyOCR.objects.filter(id=id).first()
    pages = Page.objects.filter(ocr_object=paper)
    return render(request, 'ocr/view_pages.html',{
        'pages':pages
    })

def view_page_results(request,id):
    page = Page.objects.get(id=id)
    results = OCRResult.objects.filter(page=page)
    return render(request,'ocr/view_page_results.html',{
        'results':results
    })