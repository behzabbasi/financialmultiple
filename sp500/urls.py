from django.urls import path

from .views import sp500_view



app_name='sp500'

urlpatterns = [
    path('',sp500_view, name='sp500_view'),
]
