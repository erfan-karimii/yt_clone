from celery import shared_task
from youtube.models import Video 
from account.models import User,Profile
from pytube import YouTube 
from pytube.helpers import safe_filename
from youtube.models import Video
from django.conf import settings
from bucket import bucket
import os

@shared_task
def save_video_from_youtube_task(url,itag,email):
    user = User.objects.get(email=email)
    profile = Profile.objects.get(user=user)

    video = YouTube(url)
    stream = video.streams.get_by_itag(itag)
    # stream.download()
    filename = safe_filename(video.title)
    Video.objects.create(youtuber = profile,video=filename,title='منتظر ادیت')
    return 'Done'

@shared_task
def save_video_task(object_name,file_abs_path):
    import os
    print(os.path.isfile(file_abs_path))
    bucket.upload_file(file_abs_path, settings.AWS_STORAGE_BUCKET_NAME, object_name)
