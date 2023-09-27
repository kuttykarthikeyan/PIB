from django.db import models

# Create your models here.

class News(models.Model):

    data = models.FileField()
    title = models.CharField(max_length=200)
    published_time = models.DateTimeField()
    source = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    is_positive = models.BooleanField()
    is_latest = models.BooleanField()