from django.urls import path 
from . import views

app_name='youtube'

urlpatterns = [
    path('',views.index,name='home'),
    path('upload_video/',views.upload_video,name='upload_video'),
    path('upload_list/',views.upload_list,name='upload_list'),
    path('upload_edit/<id>/',views.upload_edit,name='upload_edit'),
    path('upload_delete/<id>/',views.upload_delete,name='upload_delete'),
    path('video_detail/<id>/',views.video_detail,name='video_detail'),
    path('add_new_tag/',views.add_new_tag_ajax,name='add_new_tag'),
    path('like_video/',views.like_video_ajax,name='like_video'),
    path('channel_home_page/<id>/',views.channel_home_page,name='channel_home_page'),

]