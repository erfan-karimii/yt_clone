from django.contrib import admin
from .models import Video ,VideoTag ,Category ,PlayList ,Comment
# Register your models here.

admin.site.register(Video)
admin.site.register(VideoTag)
admin.site.register(Category)
admin.site.register(PlayList)
admin.site.register(Comment)



