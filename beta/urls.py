from django.urls import path

from .views import *



app_name='beta'

urlpatterns = [
    path('',beta_view, name='beta_view'),
    path('volatility/',volatility_view, name='volatility_view'),
    #path('pe-ratio/',sp500_view_pe, name='sp500_view_pe'),
]