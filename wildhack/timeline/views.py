from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import datetime
import json
from .models import Fact, News, Tag
from django.core import serializers



class TimelineView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'timeline':['хехех']})

class ModeratorView(View):
    def get(self, request, *args, **kwargs):
        latest_facts_list = Fact.objects.order_by('-date')[:5]
        return JsonResponse(serializers.serialize('json', latest_facts_list), safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        fact = Fact(title=json_data['title'])
        fact.date = datetime.date.fromisoformat(json_data['date'])
        fact.text = json_data['text']
        fact.source = json_data['source']
        fact.importance = json_data['importance']
        fact.save()
        return JsonResponse({'data': json_data}, json_dumps_params={'ensure_ascii': False})
        '''
        	title = models.CharField(max_length=200)
	date = models.DateField()
	text = models.TextField()
	source = models.URLField()
	importance = models.PositiveIntegerField(validators=[validators.MaxValueValidator(10)])
'''