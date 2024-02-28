from django.urls import path
from .views import *
urlpatterns=[
    path('',home),
    path('process_video/', process_video)
]