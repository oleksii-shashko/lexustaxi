# Generated by Django 2.2 on 2019-05-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='img_url',
            field=models.TextField(blank=True, help_text='Enter image path', null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='comment',
            field=models.TextField(blank=True, help_text='Enter comments to request', max_length=256, null=True),
        ),
    ]