# Generated by Django 4.1.3 on 2023-02-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_channel_name'),
        ('youtube', '0012_alter_video_video_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='visited',
        ),
        migrations.RemoveField(
            model_name='video',
            name='like',
        ),
        migrations.AddField(
            model_name='video',
            name='like',
            field=models.ManyToManyField(related_name='like', to='account.profile'),
        ),
    ]
