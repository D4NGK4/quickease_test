# Generated by Django 5.0.2 on 2024-09-05 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarizer_api', '0003_alter_usernotes_notetitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotes',
            name='notetitle',
            field=models.CharField(default='', max_length=30, verbose_name='Note Title'),
        ),
    ]
