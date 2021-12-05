from django.http import JsonResponse
from django.views import View
import datetime
import json
from .models import Fact, News
from django.core import serializers

class TimelineView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'timeline':['хехех']})

class FactsView(View):
    def get(self, request, *args, **kwargs):
        latest_facts_list = Fact.objects.order_by('-pk')[:5]
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

class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.filter(isProcessed=False).order_by('?')[:1]
        if  news.count() == 0:
            return JsonResponse({'error': 'Все новости обработаны'}, json_dumps_params={'ensure_ascii': False})
        return JsonResponse(serializers.serialize('json', news), json_dumps_params={'ensure_ascii': False}, safe=False)
