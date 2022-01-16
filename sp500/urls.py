from django.urls import path

from .views import sp500_view,sp500_view_pe, sp500_view_shiller_pe, sp500_view_e_yield, sp500_view_s_growth, sp500_view_e_growth, sp500_view_dis_ps_ratio, sp500_view_dis_rev_growth, sp500_view_dis_op_margin, sp500_view_dis_gr_margin,sp500_view_excess_cape



app_name='sp500'

urlpatterns = [
    path('',sp500_view, name='sp500_view'),
    path('pe-ratio/',sp500_view_pe, name='sp500_view_pe'),
    path('shiller-pe/',sp500_view_shiller_pe, name='sp500_view_shiller_pe'),
    path('earnings-yield/',sp500_view_e_yield, name='sp500_view_e_yield'),
    path('sales-growth/',sp500_view_s_growth, name='sp500_view_s_growth'),
    path('earnings-growth/',sp500_view_e_growth, name='sp500_view_e_growth'),
    path('price-sales-distribution/',sp500_view_dis_ps_ratio, name='sp500_view_dis_ps_ratio'),
    path('revenue-growth-distribution/',sp500_view_dis_rev_growth, name='sp500_view_dis_rev_growth'),
    path('operating-margin-distribution/',sp500_view_dis_op_margin, name='sp500_view_dis_op_margin'),
    path('gross-margin-distribution/',sp500_view_dis_gr_margin, name='sp500_view_dis_gr_margin'),
    path('excess-cape/',sp500_view_excess_cape, name='sp500_view_excess_cape'),
]
