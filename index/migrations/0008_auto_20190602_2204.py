# Generated by Django 2.2 on 2019-06-02 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_auto_20190602_2202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-status', '-data']},
        ),
    ]