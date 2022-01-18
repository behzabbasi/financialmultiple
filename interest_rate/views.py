from django.shortcuts import render
from plotly.offline import plot
from .functions import *

# Create your views here.


def interest_rate_tbill_view(request):
  fig, dic_list  = interest_rate_t_bill()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list':dic_list,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate.html", context)

def interest_rate_tbond_view(request):
  fig, dic_list  = interest_rate_t_bond()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list':dic_list,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate_tbond.html", context)

def yield_curve_view(request):
  fig  = yield_curve()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate_yield_curve.html", context)

def tips_view(request):
  fig, dic_list  = tips_rate()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list':dic_list,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate_tips.html", context)

def inflation_view(request):
  fig, dic_list  = cpi_inflation()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list': dic_list,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate_cpi_inflation.html", context)

def expected_inflation_view(request):
  fig, dic_list = expected_inflation()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list':dic_list,
    #'error_message':error_message
  }
  return render(request, "interest_rate/interest_rate_inflation.html", context)