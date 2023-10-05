from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('article/<int:index>/<int:id>',views.article,name='article'),

]
