# Generated by Django 2.2.16 on 2021-02-14 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='log',
            name='object_id',
        ),
        migrations.AddField(
            model_name='log',
            name='page',
            field=models.CharField(default='Empty', help_text='Required.', max_length=255, verbose_name='Page'),
            preserve_default=False,
        ),
    ]
