from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/competition/', include('competition.urls')),
    path('api/', include('api.urls')),
]
