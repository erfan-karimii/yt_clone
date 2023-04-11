from celery import shared_task
from youtube.models import Video 
from account.models import User,Profile
from pytube import YouTube 
from pytube.helpers import safe_filename
from django.core.files import File
from django.core.files.storage import DefaultStorage as storage
from youtube.models import Video
import logging
# from bucket import bucket

logging.basicConfig(level=logging.INFO)

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

@shared_task()
def save_video_task(object_name,file_path,email):
    # bucket.upload_object(object_name,file_path)
    user = User.objects.get(email=email)
    profile = Profile.objects.get(user=user)

    with open(file_path, 'r') as f:
        file = File(f)

        newdoc = Video(youtuber=profile,video=file)
        newdoc.save()

        logging.info("document saved successfully")

        storage.delete(file_path) # cleanup temp file
    
    return 'Done'
