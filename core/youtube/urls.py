from django.urls import path 
from . import views

app_name='youtube'

urlpatterns = [
    path('',views.index,name='home'),
    path('upload_video/',views.upload_video,name='upload_video'),
    path('upload_list/',views.upload_list,name='upload_list'),
    path('upload_edit/<id>/',views.upload_edit,name='upload_edit'),
    path('upload_edit_youtube/',views.upload_edit_youtube,name='upload_edit_youtube'),
    path('upload_delete/<id>/',views.upload_delete,name='upload_delete'),
    path('video_detail/<id>/',views.video_detail,name='video_detail'),
    path('add_new_tag/',views.add_new_tag_ajax,name='add_new_tag'),
    path('like_video/',views.like_video_ajax,name='like_video'),
    path('follow_channel/',views.follow_channel_ajax,name='follow_channel'),
    path('watch_later/',views.watch_later_ajax,name='watch_later'),
    path('get_playlist/',views.get_playlist_ajax,name='get_playlist'),
    path('add_video_to_playlist/',views.add_video_to_playlist_ajax,name='add_video_to_playlist'),
    path('create_playlist/',views.create_playlist_ajax,name='create_playlist'),
    path('save_comment/',views.save_comment_ajax,name='save_comment'),
    path('delete_comment/<id>/',views.delete_comment,name='delete_comment'),
    path('pin_comment/<id>/',views.pin_comment,name='pin_comment'),
    path('delete_playlist/<id>/',views.delete_playlist,name='delete_playlist'),
    path('channel_home_page/<id>/',views.channel_home_page,name='channel_home_page'),
    path('history_page/',views.history_page,name='history_page'),
    path('browse_category/',views.browse_category,name='browse_category'),
    path('browse_channels/',views.browse_channels,name='browse_channels'),
    path('save_video_from_youtube/',views.save_video_from_youtube,name='save_video_from_youtube'),
    path('clear_watch_history/',views.clear_watch_history,name='clear_watch_history'),
]