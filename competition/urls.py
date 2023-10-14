from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.CompetitionViewSet, basename='competition')

urlpatterns = [
    path('myComp/', views.UserCompetitionView.as_view()),
    path('accept/', views.AcceptCompetitionView.as_view()),
    path('showMyReq/', views.ShowMyReq.as_view()),
    path('<int:pk>/apply/', views.ApplyCompetitionView.as_view()),
    path('<int:compId>/compStatus/', views.CompStatus.as_view(), name='user'),
    path('<int:compId>/remove/<int:userSelectorId>/', views.RemoveRequestView.as_view(), name='user'),
    path('', include(router.urls)),
]
