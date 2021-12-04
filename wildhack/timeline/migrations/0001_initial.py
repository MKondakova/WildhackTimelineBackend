# Generated by Django 3.2.9 on 2021-12-04 16:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('source', models.URLField()),
                ('text', models.TextField()),
                ('isProcessed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('text', models.TextField()),
                ('importance', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='timeline.news')),
                ('tags', models.ManyToManyField(to='timeline.Tag')),
            ],
        ),
    ]
