from django.shortcuts import render
from plotly.offline import plot
from .functions import *

# Create your views here.



def beta_view(request):
  error_message=None
  #print(request.POST.get('stock_ticker'))
  if request.POST:
    stock_ticker=request.POST.get('stock_ticker')
    benchmark=request.POST.get('benchmark')
    try:
      beta, cor,intercept, fig  = correlation(stock_ticker, benchmark)
      
      plot_div =plot(fig, output_type='div')
      
      context={
        'plot_div': plot_div,
        'stock_ticker':stock_ticker,
        'benchmark': benchmark,
        'beta':beta,
        'cor':cor,
        'intercept':intercept,
        'error_message':error_message
      }
    except:
      error_message='Error! Please enter a valid stock ticker'
      context = {'error_message':error_message}
  else:
    context = {}

  return render(request, "beta/beta.html", context)

def volatility_view(request):
  fig, dic_list  = volatility()
  plot_div =plot(fig, output_type='div')
  context={
    'plot_div': plot_div,
    'dic_list':dic_list,
    #'error_message':error_message
  }
  return render(request, "beta/volatility.html", context)