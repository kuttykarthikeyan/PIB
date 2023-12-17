from django.db import models

class DailyOCR(models.Model):
    date = models.DateField()
    json_result = models.JSONField(null=True,default={},blank=True)
    languauge = models.CharField(max_length=30,null=True)
    file = models.FileField(upload_to='ocr/',null=True)
    name = models.CharField(max_length=40,null=True)
    

class Page(models.Model):
    page_number = models.IntegerField()
    ocr_object = models.ForeignKey(DailyOCR,on_delete=models.CASCADE, related_name='pages')
    file = models.FileField(upload_to='ocr/',null=True)

class OCRResult(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='results')
    name = models.CharField(max_length=25)
    file = models.FileField(upload_to='ocr/')
