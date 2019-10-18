from django.urls import path
from simplemooc.core.views import home

urlpatterns = [
    path('', home, name='home'),
]