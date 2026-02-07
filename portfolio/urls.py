from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('work/<slug:slug>/', views.artwork_detail, name='artwork_detail'),
]
