from django.urls import path
from . import views
from store.views import index


app_name= 'store'

urlpatterns = [
    path('', views.index ,name='index'),


]