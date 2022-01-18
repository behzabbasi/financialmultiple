from statistics import median
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta
import quandl
from pathlib import Path
import os, time
import pickle
import pandas_datareader.data as web



BASE_DIR = Path(__file__).resolve().parent.parent
path_name = os.path.join(BASE_DIR, 'data/sp500/')


end_time = date.today()
start_time = end_time - timedelta(days=365 * 10)
end = end_time.strftime("%Y-%m-%d")
start = start_time.strftime("%Y-%m-%d")


# reading data:
def read_data(data_name):
  df_data=pd.DataFrame()
  if (os.path.isfile(f"{path_name}{data_name}.csv")):
    if end_time.day==15 and time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(f"{path_name}{data_name}.csv"))) != str(date.today()):
      df_data=quandl.get(f"MULTPL/{data_name}", authtoken="Q88E1T5tiQ1oFGUQHJqk", collapse="monthly") #start_date="2008-12-31"
      df_data.to_csv(f"{path_name}{data_name}.csv")
    else: 
      df_data = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0)
  else:
    try:
      df_data=quandl.get(f"MULTPL/{data_name}", authtoken="Q88E1T5tiQ1oFGUQHJqk", collapse="monthly") #start_date="2008-12-31"
      df_data.to_csv(f"{path_name}{data_name}.csv")
    except:
      df_data = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 
  return df_data

# colors: #F98404 #FFCC1D

def show_data(data_name):
  df_sp500_ratio=read_data(data_name)

  mean_=round(df_sp500_ratio['Value'].mean(),1)
  median_=round(df_sp500_ratio['Value'].median(),1)
  min_=round(df_sp500_ratio['Value'].min(),1)
  max_=round(df_sp500_ratio['Value'].max(),1)
  current_=round(df_sp500_ratio.iloc[-1]['Value'],1)
  fig = go.Figure()
  fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 20, "t": 20}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.add_trace(go.Scatter(x=df_sp500_ratio.index, y=df_sp500_ratio["Value"], mode="lines",line=dict(width=1), marker=dict(size=7, color='#F98404'), fill='tozeroy',))
  fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  return fig,current_, mean_,median_, min_, max_


# Alpha info
with open(f'{path_name}SP500_alpha_info', 'rb') as SP500_alpha_info:
    SP500_dic_info = pickle.load(SP500_alpha_info)

SP500=pd.read_csv(f'{path_name}SP500_december2021.csv')
SP500.set_index('Emittententicker', inplace=True)

def df_info():
  colums=['symbole','Gewichtung','MarketCapitalization','RevenueTTM','QuarterlyRevenueGrowthYOY','GrossProfitTTM','OperatingMarginTTM','PERatio','ReturnOnAssetsTTM','ReturnOnEquityTTM','PriceToSalesRatioTTM','PriceToBookRatio','EVToRevenue','EVToEBITDA','Beta']
  df=pd.DataFrame(columns=colums)
  for n, item in enumerate(SP500_dic_info):
    list_rev=[]
    try:
      list_rev.append(item)
      list_rev.append(SP500.loc[item]['Gewichtung']/100)
      TTM=0
      for what in colums[2:]:
        try:
          TTM=float(SP500_dic_info[item][what])
        except:
          TTM=0
        list_rev.append(TTM)
      df.loc[n]=list_rev
    except:
      pass
  df.set_index('symbole', inplace=True)
  df['grossMarginTTM']=df['GrossProfitTTM']/df['RevenueTTM']
  df=df.iloc[:-4]
  return df

def sp500_distribution(data_name):
  sp500_info=df_info()
  mean_=round(sp500_info[data_name].mean(),2)
  median_=round(sp500_info[data_name].median(),2)
  min_=round(sp500_info[data_name].min(),2)
  max_=round(sp500_info[data_name].max(),2)
  current_='--'
  fig = go.Figure()

  if data_name=='PriceToSalesRatioTTM':
    dtick=1
    fig.add_trace(go.Histogram(x=round(sp500_info[data_name],2),histnorm='percent',name=data_name,xbins=dict(start=0,end=31,size=1),marker_color='#F98404',opacity=0.7))
    fig.add_vline(x=sp500_info[data_name].median(),annotation_text=f'Median {data_name}', annotation_position="top right", line_width=3, line_dash="dot", line_color="red")
  else:
    dtick=0.05
    fig.add_trace(go.Histogram(x=round(sp500_info[data_name],2),histnorm='percent',name=f'{data_name}',xbins=dict(start=-1.0,end=1.0,size=0.05),marker_color='#F98404',opacity=0.7))
    fig.add_vline(x=sp500_info[data_name].median(),annotation_text=f'Median {data_name}', annotation_position="top right", line_width=3, line_dash="dot", line_color="red")


  fig['layout']['margin'] = {'l': 20, 'r': 20, 'b': 30, 't': 30}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.update_traces(marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=1,)
  fig.update_layout(annotations=[go.layout.Annotation(textangle=90)])
  fig.update_layout(barmode='group',bargap=0.50,bargroupgap=0.0)
  fig.update_layout(xaxis = dict(tickmode = 'linear',tick0 = -0.5,dtick = 0.05,showgrid=True,ticks="outside",))
  fig['layout']['margin'] = {'l': 20, 'r': 20, 'b': 30, 't': 30}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.update_traces(marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.9,)
  fig.update_layout(annotations=[go.layout.Annotation(textangle=90)])
  fig.update_layout(barmode='group',bargap=0.5,bargroupgap=0.0)
  fig.update_layout(xaxis = dict(tickmode = 'linear',tick0 = -0.5,dtick = dtick,showgrid=True,ticks="outside",))
  fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  return fig, current_, mean_,median_, min_, max_


def excess_cape():
  df_shiller = pd.read_csv(f"{path_name}SHILLER_PE_RATIO_MONTH.csv", index_col=0)
  df_real_rate = web.DataReader('DFII10', data_source="fred", start=start, end=end)
  df=pd.concat([df_shiller, df_real_rate], axis=1).ffill().dropna()
  df['Excess_CAPE']=1/df['Value']*100-df['DFII10']
  mean_=round(df['Excess_CAPE'].mean(),1)
  median_=round(df['Excess_CAPE'].median(),1)
  min_=round(df['Excess_CAPE'].min(),1)
  max_=round(df['Excess_CAPE'].max(),1)
  current_=round(df.iloc[-1]['Excess_CAPE'],1)
  fig = go.Figure()
  fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 20, "t": 20}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.add_trace(go.Scatter(x=df.index, y=df["Excess_CAPE"], mode="lines", marker=dict(size=7, color='#F98404'), fill='tozeroy',))
  fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  return fig, current_, mean_,median_, min_, max_