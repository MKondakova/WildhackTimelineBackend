# Generated by Django 3.2.9 on 2021-12-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fact',
            name='source',
            field=models.URLField(),
        ),
    ]
