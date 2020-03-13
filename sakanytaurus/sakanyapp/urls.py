from django.urls import path
from . import views

app_name = 'sakanyapp'
urlpatterns = [
path('', views.index, name='index')
]
