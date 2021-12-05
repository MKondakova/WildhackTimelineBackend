from django.db import models
from django.core import validators

class Tag(models.Model):
	name = models.CharField(max_length=50)

class News(models.Model):
	title = models.CharField(max_length=200)
	source = models.URLField()
	date = models.CharField(max_length=20)
	isProcessed = models.BooleanField(default=False)

	
class Fact(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateField()
	text = models.TextField()
	source = models.URLField()
	importance = models.PositiveIntegerField(validators=[validators.MaxValueValidator(10)])

	tags = models.ManyToManyField(Tag)
