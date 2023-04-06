from bucket import bucket
from celery import shared_task
import random
import string

from youtube.models import Category

# TODO: can be async?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result

@shared_task
def delete_object_task(key):
    bucket.delete_object(key)


@shared_task
def download_object_task(key):
    bucket.download_object(key)

@shared_task
def test_periodic_task_celery_beat():
    letters = string.ascii_letters
    random_text = ''.join(random.choice(letters) for _ in range(10))
    Category.objects.create(name=random_text)

