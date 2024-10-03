from django.urls import path
from .views import BadgeListCreateView, AchievementsListCreateView

urlpatterns = [
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('achievements/', AchievementsListCreateView.as_view(), name='achievement-list-create'),
]