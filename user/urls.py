from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('<int:pk>/', views.RetrieveUserView.as_view(), name='user'),
    path('myProfile/', views.RetrieveMyUserProfile.as_view(), name='my_profile')
]