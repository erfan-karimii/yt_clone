from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    video = models.FileField()
    thumbnail = models.ImageField()
    visited = models.PositiveIntegerField(default=0)
    pin_comment = models.CharField(max_length=10,null=True,blank=True)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

class VideoTag(models.Model):
    tag = models.ManyToManyField(Video,)

# nested comment 

