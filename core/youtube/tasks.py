from celery import shared_task
from youtube.models import Video 
from account.models import User,Profile
from pytube import YouTube 
from pytube.helpers import safe_filename
from youtube.models import Video
from django.conf import settings
from bucket import bucket
from youtube.models import get_video_duration_with_moviepy
@shared_task
def save_video_from_youtube_task(url,itag,profile_id):
    profile = Profile.objects.get(id=profile_id)
    video = YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    filename = safe_filename(video.title)
    Video.objects.create(youtuber = profile,video=filename,title='منتظر ادیت')
    return 'Done'

@shared_task
def save_video_task(object_name,file_abs_path,profile_id):
    bucket.upload_file(file_abs_path, settings.AWS_STORAGE_BUCKET_NAME, object_name)
    profile = Profile.objects.get(id=profile_id)
    Video.objects.create(video=object_name,youtuber=profile,video_time=get_video_duration_with_moviepy(file_abs_path))

@shared_task
def delete_video_with_object_task(key):
    bucket.delete_object(key)