from celery import shared_task
from .models import Video 


@shared_task
def test_celery(youtuber_id,video):
    Video.objects.create(youtuber_id=youtuber_id,video=video)
