from celery import shared_task
from youtube.models import Video 
from account.models import User,Profile
from pytube import YouTube 
from pytube.helpers import safe_filename

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
