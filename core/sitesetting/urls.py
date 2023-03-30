from django.urls import path 
from . import views 

app_name = 'sitesetting'

urlpatterns = [
    path('header/',views.header_view,name='header'),
    path('footer/',views.footer_view,name='footer'),

    path('bucket/',views.BucketHome.as_view(),name='bucket')


]