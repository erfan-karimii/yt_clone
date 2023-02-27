# Generated by Django 4.1.3 on 2023-02-24 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_profile_first_name_remove_profile_last_name'),
        ('youtube', '0022_alter_comment_profile_alter_comment_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtube.video'),
        ),
    ]
