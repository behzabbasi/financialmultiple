from django.shortcuts import render
from plotly.offline import plot
from .functions import *

# Create your views here.


def sp500_view(request):
  fig,current_, mean_,median_,min_,max_  = show_data('SP500_PSR_QUARTER')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500.html", context)

def sp500_view_pe(request):
  fig,current_,  mean_,median_,min_,max_   = show_data('SP500_PE_RATIO_MONTH')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_pe.html", context)

def sp500_view_shiller_pe(request):
  fig,current_,  mean_,median_,min_,max_   = show_data('SHILLER_PE_RATIO_MONTH')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_shiller_pe.html", context)


def sp500_view_e_yield(request):
  fig,current_,  mean_,median_,min_,max_   = show_data('SP500_EARNINGS_YIELD_MONTH')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_e_yield.html", context)


def sp500_view_s_growth(request):
  fig,current_,  mean_,median_,min_,max_   = show_data('SP500_SALES_GROWTH_QUARTER')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_s_growth.html", context)


def sp500_view_e_growth(request):
  fig,current_,  mean_,median_,min_,max_   = show_data('SP500_EARNINGS_GROWTH_QUARTER')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_e_growth.html", context)


# Distribution
def sp500_view_dis_ps_ratio(request):
  fig, current_, mean_,median_, min_, max_  = sp500_distribution('PriceToSalesRatioTTM')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_dis_ps_ratio.html", context)

def sp500_view_dis_rev_growth (request):
  fig, current_, mean_,median_, min_, max_   = sp500_distribution('QuarterlyRevenueGrowthYOY')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_dis_rev_growth.html", context)

def sp500_view_dis_op_margin (request):
  fig, current_, mean_,median_, min_, max_   = sp500_distribution('OperatingMarginTTM')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_dis_op_margin.html", context)

def sp500_view_dis_gr_margin (request):
  fig, current_, mean_,median_, min_, max_  = sp500_distribution('grossMarginTTM')
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_dis_gr_margin.html", context)

def sp500_view_excess_cape (request):
  fig, current_, mean_,median_,min_,max_  = excess_cape()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'current_': current_,
    'mean_': mean_,
    'median_': median_,
    'min_': min_,
    'max_': max_,
    #'error_message':error_message
  }
  return render(request, "sp500/sp500_excess_cape.html", context)