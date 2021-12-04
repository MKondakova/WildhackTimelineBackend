from timeline.views import TimelineView
from timeline.views import ModeratorView

from django.urls import path

urlpatterns = [
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('moderator/', ModeratorView.as_view(), name='moderator')
]
