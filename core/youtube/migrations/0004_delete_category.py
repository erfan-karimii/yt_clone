# Generated by Django 4.1.3 on 2023-02-15 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0003_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]