from timeline.views import TimelineView
from timeline.views import FactsView
from timeline.views import NewsView

from django.urls import path


urlpatterns = [
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('facts/', FactsView.as_view(), name='facts'),
    path('news/', NewsView.as_view(), name='news')
]
