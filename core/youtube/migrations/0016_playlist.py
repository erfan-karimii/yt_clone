# Generated by Django 4.1.3 on 2023-02-18 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_profile_first_name_remove_profile_last_name'),
        ('youtube', '0015_remove_video_dislike'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
                ('video', models.ManyToManyField(to='youtube.video')),
            ],
        ),
    ]