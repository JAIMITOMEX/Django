from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # La URL principal para la vista index
]