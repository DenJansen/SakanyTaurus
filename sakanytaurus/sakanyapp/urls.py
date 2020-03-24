from django.urls import path
from . import views

app_name = 'sakanyapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('findpub/', views.findpub, name='findpub'),
    path('newcrawl/', views.newcrawl, name='newcrawl'),
    path('profile/', views.profile, name='profile')
]
