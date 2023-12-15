from django.db import models

class DailyOCR(models.Model):
    date = models.DateField()
    json_result = models.JSONField()

class Page(models.Model):
    page_number = models.IntegerField()
    ocr_object = models.ForeignKey(DailyOCR,on_delete=models.CASCADE, related_name='pages')

class OCRResult(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='results')
    name = models.CharField(max_length=25)
    file = models.FileField(upload_to='ocr/')
