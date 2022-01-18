from django.urls import path

from .views import *



app_name='interest_rate'

urlpatterns = [
    path('',interest_rate_tbill_view, name='interest_rate_tbill_view'),
    path('t-bond/',interest_rate_tbond_view, name='interest_rate_tbond_view'),
    path('yield-curve/',yield_curve_view, name='yield_curve_view'),
    path('tips/',tips_view, name='tips_view'),
    path('inflation/',inflation_view, name='inflation_view'),
    path('expected-inflation/',expected_inflation_view, name='expected_inflation_view'),
]