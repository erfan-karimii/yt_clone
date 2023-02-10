# Generated by Django 4.1.3 on 2023-02-10 09:18

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('video', models.FileField(upload_to='')),
                ('video_time', models.CharField(blank=True, max_length=10, null=True)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('visited', models.PositiveIntegerField(default=0)),
                ('pin_comment', models.CharField(blank=True, max_length=10, null=True)),
                ('like', models.PositiveIntegerField(default=0)),
                ('dislike', models.PositiveIntegerField(default=0)),
                ('youtuber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ManyToManyField(to='youtube.video')),
            ],
        ),
    ]
