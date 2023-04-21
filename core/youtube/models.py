from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from moviepy.editor import VideoFileClip
from hitcount.utils import get_hitcount_model
from hitcount.models import HitCountMixin , HitCount
from datetime import datetime , timezone ,timedelta
import os

# Create your models here.

def get_video_duration_with_moviepy(filename):
    clip = VideoFileClip(filename)
    video_duration = clip.duration
    return str(timedelta(seconds=int(video_duration)))

class VideoManager(models.Manager):
    def all_video(self,**kwargs):
        return Video.objects.filter(published=True,**kwargs)

class Video(models.Model,HitCountMixin):
    youtuber = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True)
    video = models.FileField()
    video_time = models.CharField(max_length=15,null=True,blank=True)
    thumbnail = models.ImageField()
    monetize = models.BooleanField(default=True)
    tags = models.ManyToManyField('VideoTag')
    like = models.ManyToManyField('account.Profile',related_name='like')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    published = models.BooleanField(default=False)
    show = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = VideoManager()

    @property
    def days_passed(self):
        today = datetime.now(timezone.utc)
        days_passed = today - self.created
        return f"{days_passed.days} روز پیش" if days_passed.days != 0 else 'امروز'
    
    @property
    def visited(self):
        hit_count = get_hitcount_model().objects.get_for_object(self)
        return hit_count.hits
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs) 
    #     if self.video:
    #         self.video_time = get_video_duration_with_moviepy(self.video.path)


    def __str__(self):
        return self.title

class VideoTag(models.Model):
    name = models.CharField(max_length=155,null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام دسته بندی')
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    profile = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    body = models.TextField()
    like = models.PositiveIntegerField(default=0)
    is_pin_comment = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body
    
    @property
    def days_passed(self):
        today = datetime.now(timezone.utc)
        days_passed = today - self.created
        return f"{days_passed.days} روز پیش" if days_passed.days != 0 else f'{timedelta(seconds=int(days_passed.seconds))} قبل '

    class Meta :
        ordering = ['-created']
        unique_together = ('profile', 'video')

class PlayList(models.Model):
    profile = models.ForeignKey('account.Profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video = models.ManyToManyField('Video')

    def __str__(self):
        return self.name
