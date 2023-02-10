from django.urls import path 
from .views import header_view 

app_name = 'sitesetting'

urlpatterns = [
    path('header/',header_view,name='header'),

]