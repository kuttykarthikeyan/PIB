

# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers
 
# import everything from views
from .views import *

router = routers.DefaultRouter()

app_name = 'apis'


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('youtube_video_data_analysis/',youtube_video_data_analysis,name='youtube_video_data_analysis'),
    path('save_youtube_data/',save_youtube_data,name='save_youtube_data'),
    path('scrap_news_clustered_data/',scrap_news_clustered_data,name='scrap_news_clustered_data'),
    path('get_negative_clips/<int:id>',get_negative_clips,name='get_negative_clips'),
    path('get_word_cloud/<int:id>',get_word_cloud,name='get_word_cloud'),
]

