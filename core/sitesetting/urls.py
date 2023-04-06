from django.urls import path ,include
from . import views 

app_name = 'sitesetting'

bucket_urls = [
    path('',views.BucketHome.as_view(),name='bucket'),
    path('delete_obj/<key>',views.DeleteBucketObject.as_view(),name='delete_obj_bucket'),
    path('download_obj/<key>',views.DownloadBucketObject.as_view(),name='download_obj_bucket'),


]

urlpatterns = [
    path('header/',views.header_view,name='header'),
    path('footer/',views.footer_view,name='footer'),
    path('bucket/',include(bucket_urls)),
]