from django.urls import path 
from . import views

app_name='youtube'

urlpatterns = [
    path('',views.index,name='home'),
    path('upload_video/',views.upload_video,name='upload_video'),
    path('upload_list/',views.upload_list,name='upload_list'),
    path('upload_edit/<id>/',views.upload_edit,name='upload_edit'),


]