from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('cluster/<int:id>',views.cluster,name='cluster'),
    path('article_analysis/<int:pk>/<int:check>/',views.article_analysis,name='article_analysis'),
    path('article_home',views.article_home,name='article_home'),
    path('article/<int:index>/<int:id>',views.article,name='article'),
    path('youtube_videos/',views.youtube_data_home,name='youtube_data_home'),
    path('youtube_video_analysis/<int:id>',views.youtube_data_analysis,name='youtube_data_analysis'),
    path('text_video/',views.text_video,name='text_video'),
    # path('eprints',views.eprints,name='eprints'),
#     path('eprint',views.eprint,name='eprint'),
    path('newsanalysis',views.newsanalysis,name='newsanalysis'),
#     path('youtubes',views.youtubes,name='youtubes'),
    # path('youtubes',views.youtubes,name='youtubes'),
    path('dash',views.dash,name='dash'),
    # path('filters',views.filters,name='filters'),
    path('lang',views.lang,name='lang'),
    
]
