from django.urls import path
from . import views

urlpatterns = [
    # path('gpt3/', views.gpt3, name='gpt3'),
    path('', views.gpt3, name='gpt3'),
    path('upload/', views.upload_file, name='upload_file'),
]