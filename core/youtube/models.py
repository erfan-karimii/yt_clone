from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from moviepy.editor import VideoFileClip
from account.models import Profile

# Create your models here.

def get_video_duration_with_moviepy(filename):
    clip = VideoFileClip(filename)
    duration = clip.duration
    return int(duration)

class Video(models.Model):
    youtuber = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    video = models.FileField()
    video_time = models.CharField(max_length=10,null=True,blank=True)
    thumbnail = models.ImageField()
    visited = models.PositiveIntegerField(default=0)
    pin_comment = models.CharField(max_length=10,null=True,blank=True)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self):
        self.video_time = get_video_duration_with_moviepy(self.video.path)
        super().save() 


    def __str__(self):
        return self.title

class VideoTag(models.Model):
    tag = models.ManyToManyField(Video,)

# nested comment 

