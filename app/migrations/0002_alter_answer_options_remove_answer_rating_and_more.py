# Generated by Django 4.0.3 on 2022-04-27 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['is_correct']},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='question',
            name='rating',
        ),
    ]
