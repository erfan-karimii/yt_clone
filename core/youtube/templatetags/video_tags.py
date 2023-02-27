from django import template
from youtube.models import Video
register = template.Library()


# @register.filter(name='days_passed') 
# def convert_id_to_video(id):
#     video = Video.objects.get(id=id)    
#     return video
