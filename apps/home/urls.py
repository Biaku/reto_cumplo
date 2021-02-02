from django.urls import path
from django.views.generic import TemplateView

from apps.home.views import index

app_name = 'home'

urlpatterns = [
    path('', index, name='index')
]
