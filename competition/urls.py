from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.CompetitionViewSet, basename='competition')

urlpatterns = [
    path('', include(router.urls)),
    path('apply/<int:pk>/', views.ApplyCompetition.as_view()),
]
