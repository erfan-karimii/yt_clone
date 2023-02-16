from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from moviepy.editor import VideoFileClip
from hitcount.utils import get_hitcount_model
from datetime import datetime , timezone ,timedelta
import os

# Create your models here.

def get_video_duration_with_moviepy(filename):
    clip = VideoFileClip(filename)
    video_duration = clip.duration
    return str(timedelta(seconds=int(video_duration)))

def get_upload_path(instance, filename):
    return os.path.join(
      f"{instance.youtuber.channel_name}",filename)



class Video(models.Model):
    youtuber = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True)
    video = models.FileField(upload_to=get_upload_path)
    video_time = models.CharField(max_length=15,null=True,blank=True)
    thumbnail = models.ImageField(upload_to=get_upload_path)
    monetize = models.BooleanField(default=True)
    tags = models.ManyToManyField('VideoTag')
    pin_comment = models.CharField(max_length=10,null=True,blank=True)
    like = models.ManyToManyField('account.Profile',related_name='like')
    published = models.BooleanField(default=False)
    show = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def days_passed(self):
        today = datetime.now(timezone.utc)
        days_passed = today - self.created
        return f"{days_passed.days} روز پیش" if days_passed.days != 0 else 'امروز'
    
    @property
    def visited(self):
        hit_count = get_hitcount_model().objects.get_for_object(self)
        return hit_count.hits
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if self.video:
            self.video_time = get_video_duration_with_moviepy(self.video.path)


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

