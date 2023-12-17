from django.urls import path
from . import views

urlpatterns = [
    path('',views.ocr, name='ocr'),
    path('view_pages/<int:id>',views.view_pages, name='view-pages'),
    path('view_page_results/<int:id>',views.view_page_results, name='view-page-results'),
]