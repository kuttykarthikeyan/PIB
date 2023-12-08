from django.db import models
import datetime
# Create your models here.

class News(models.Model):
    data = models.FileField()
    title = models.CharField(max_length=200)
    published_time = models.DateTimeField()
    source = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    is_positive = models.BooleanField()
    is_latest = models.BooleanField()

class youtube(models.Model):
    data = models.FileField()
    title = models.CharField(max_length=200)
    published_time = models.DateTimeField()
    source = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    is_positive = models.BooleanField()
    is_latest = models.BooleanField()

class Eprints(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/")

class youtube_csv(models.Model):

    data = models.FileField(upload_to='csv_files/')
    published_time = models.DateTimeField()
    
    def save_published_date(self, published_date):
        published_date = datetime.datetime.strptime(published_date, '%Y-%m-%d %H:%M:%S')
        self.published_time = published_date
        self.save()


class URL(models.Model):
    URLs = models.URLField(max_length=300)

class youtube_csv_data(models.Model):
    
    title = models.CharField(max_length=700,null=True,blank=True)
    views = models.CharField(max_length=200,null=True,blank=True)
    thumbnail = models.CharField(max_length=900,null=True,blank=True)
    link = models.CharField(max_length=800,null=True,blank=True)
    published_time_ago = models.CharField(max_length=200,null=True,blank=True)
    duration_of_video = models.CharField(max_length=200,null=True,blank=True)
    channel_name = models.CharField(max_length=500,null=True,blank=True)
    type_of_platform = models.CharField(max_length=200,null=True,blank=True)
    


