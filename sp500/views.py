from django.shortcuts import render
from plotly.offline import plot
from .functions import *

# Create your views here.



def sp500_view(request):
  fig  = psRatio()
      
  plot_div =plot(fig, output_type='div')

      
  context={
    'plot_div': plot_div,
    #'error_message':error_message
  }

  return render(request, "sp500/sp500.html", context)









# def index(request):
#     x_data = [0,1,2,3]
#     y_data = [x**2 for x in x_data]
#     plot_div = plot([Scatter(x=x_data, y=y_data,
#                         mode='lines', name='test',
#                         opacity=0.8, marker_color='green')],
#                output_type='div')
#     return render(request, "technical/technical.html", context={'plot_div': plot_div})
