from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),  # Enlazando las URLs de la app polls
    path('admin/', admin.site.urls),
]