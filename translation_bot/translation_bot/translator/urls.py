from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('translate/', views.translate, name='translate'),
    path('batch-translate/', views.batch_translate, name='batch_translate'),
    path('history/', views.history, name='history'),
    path('clear-history/', views.clear_history, name='clear_history'),
]
