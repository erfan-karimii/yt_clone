from django.contrib import admin
from .models import Video ,VideoTag ,Category ,PlayList
# Register your models here.

admin.site.register(Video)
admin.site.register(VideoTag)
admin.site.register(Category)
admin.site.register(PlayList)


