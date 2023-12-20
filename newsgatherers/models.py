from django.db import models
import datetime
import jsonfield
from django.utils import timezone
# from videofield.models import VideoField
# Create your models here.

class news_cluster_head(models.Model):
    title = models.CharField(max_length=800, null=False, blank=False, default='Your Default Title')
    description = models.TextField(null=True,blank=True)
    published_date = models.CharField(max_length=255,null=True,blank=True)
    url = models.URLField(null=True,blank=True,max_length=900)
    publisher = models.CharField(max_length=255,null=True,blank=True)
    image = models.URLField(null=True,blank=True)
    main_text = models.TextField(null=True,blank=True)
    summary_article = models.TextField(null=True,blank=True)
    positive_sentence = models.TextField(null=True,blank=True)
    neutral_sentence = models.TextField(null=True,blank=True)
    negative_sentence = models.TextField(null=True,blank=True)
    published_time_ago = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    department = models.CharField(max_length=255,null=True,blank=True)
    POSITIVE = models.CharField(max_length=255,null=True,blank=True)
    NEUTRAL = models.CharField(max_length=255,null=True,blank=True)
    NEGATIVE = models.CharField(max_length=255,null=True,blank=True)
    SENTIMENT_ANALYSIS_RESULT = models.TextField(null=True,blank=True)
    created_time = models.DateTimeField(default=timezone.now())
    website_data_cluster_obj = models.ManyToManyField("news_obj",related_name="website_data_cluster_obj")
    youtube_data_cluster_obj = models.ManyToManyField("news_obj",related_name="youtube_data_cluster_obj")

    def __str__(self):
        return self.title
   
    
class Eprints(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/")    

class news_obj(models.Model):

    title = models.CharField(max_length=800, null=False, blank=False, default='Your Default Title')
    description = models.TextField(null=True,blank=True)
    published_date = models.CharField(null=True,blank=True,max_length=30)
    url = models.URLField(max_length=900,null=True,blank=True)
    main_text = models.TextField(null=True,blank=True)
    summary_article = models.TextField(null=True,blank=True)
    positive_sentence = models.TextField(null=True,blank=True)
    neutral_sentence = models.TextField(null=True,blank=True)
    negative_sentence = models.TextField(null=True,blank=True)
    department = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    image = models.URLField(null=True,blank=True)
    website = 'website'
    youtube = 'youtube'
    eprints = 'eprints'
    others = 'others'
    clustered = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=timezone.now())
    source_choices = ((website,'website'),(youtube,'youtube'),(eprints,'eprints'),(others,'others'))
    source_type = models.CharField(max_length=200,choices=source_choices)
    source_name = models.CharField(max_length=200,null=True,blank=True)
    source_url = models.CharField(max_length=200,null=True,blank=True)
    link = models.CharField(max_length=800,null=True,blank=True)
    published_time = models.CharField(null=True,blank=True,max_length=50)
    is_positive = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=False)
    views = models.CharField(max_length=200,null=True,blank=True)
    thumbnail = models.CharField(max_length=900,null=True,blank=True)
    published_time_ago = models.CharField(max_length=200,null=True,blank=True)
    duration_of_video = models.CharField(max_length=200,null=True,blank=True)
    channel_name = models.CharField(max_length=500,null=True,blank=True)
    type_of_platform = models.CharField(max_length=200,null=True,blank=True)
    POSITIVE = models.CharField(max_length=255,null=True,blank=True)
    NEGATIVE = models.CharField(max_length=255,null=True,blank=True)
    NEUTRAL = models.CharField(max_length=255,null=True,blank=True)
    cluster_sentiment_analysis_result = models.CharField(max_length=200,null=True,blank=True)
    sentiment_analysis = jsonfield.JSONField(null=True,blank=True)
    summary_json = jsonfield.JSONField(null=True,blank=True)
    youtube_negative_clippings = models.ManyToManyField("negative_clippings",related_name="negative_clippings")

    def __self__(self):
        return self.title

class negative_clippings(models.Model):
    video = models.FileField(upload_to='videos/')

class negative_publisher_today(models.Model):
    NEGATIVE = models.CharField(null=True,blank=True,max_length=50)
    publisher = models.CharField(null=True,blank=True,max_length=150)
    published_date = models.CharField(null=True,blank=True,max_length=200)
    state = models.CharField(null=True,blank=True,max_length=250)
# class News(models.Model):

#     data = models.FileField()
#     title = models.CharField(max_length=200
#     published_time = models.DateTimeField()
#     source = models.CharField(max_length=200)
#     url = models.CharField(max_length=200)
#     is_positive = models.BooleanField()
#     is_latest = models.BooleanField()


# class youtube_data(models.Model):
    
#     title = models.CharField(max_length=700,null=True,blank=True)
#     views = models.CharField(max_length=200,null=True,blank=True)
#     thumbnail = models.CharField(max_length=900,null=True,blank=True)
#     link = models.CharField(max_length=800,null=True,blank=True)
#     published_time_ago = models.CharField(max_length=200,null=True,blank=True)
#     duration_of_video = models.CharField(max_length=200,null=True,blank=True)
#     channel_name = models.CharField(max_length=500,null=True,blank=True)
#     type_of_platform = models.CharField(max_length=200,null=True,blank=True)
#     sentiment_analysis = jsonfield.JSONField(null=True,blank=True)
#     summary_json = jsonfield.JSONField(null=True,blank=True)



