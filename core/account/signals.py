from django.db.models.signals import post_save
from django.dispatch import receiver
from youtube.models import PlayList
from account.models import User , Profile


@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        profile= Profile.objects.create(user=instance)
        PlayList.objects.create(profile=profile,name='watch_later')