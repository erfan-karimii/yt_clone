# Generated by Django 4.1.3 on 2023-02-16 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0014_remove_video_dislike_video_dislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='dislike',
        ),
    ]