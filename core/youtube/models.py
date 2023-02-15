from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from moviepy.editor import VideoFileClip
from datetime import datetime , timezone 
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
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True)
    video = models.FileField()
    video_time = models.CharField(max_length=10,null=True,blank=True)
    thumbnail = models.ImageField()
    visited = models.PositiveIntegerField(default=0)
    monetize = models.BooleanField(default=True)
    tags = models.ManyToManyField('VideoTag')
    pin_comment = models.CharField(max_length=10,null=True,blank=True)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def days_passed(self):
        today = datetime.now(timezone.utc)
        days_passed = today - self.created
        return f"{days_passed.days} روز پیش" if days_passed.days != 0 else 'امروز'

    def save(self, *args, **kwargs):
        self.video_time = get_video_duration_with_moviepy(self.video.path)
        super().save(*args, **kwargs) 


    def __str__(self):
        return self.title

class VideoTag(models.Model):
    name = models.CharField(max_length=155,null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام دسته بندی')

    def __str__(self):
        return self.name

# nested comment 

