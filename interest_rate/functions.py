import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta
from pathlib import Path
import os, time
import pandas_datareader.data as web

API_KEY='fe837a2c2f654a04d41f5c3ca3e0124b'


BASE_DIR = Path(__file__).resolve().parent.parent
path_name = os.path.join(BASE_DIR, 'data/interest_rate/')


end_time = date.today()
start_time = end_time - timedelta(days=365 * 6)
end_str = end_time.strftime("%Y-%m-%d")
start_str = start_time.strftime("%Y-%m-%d")


def check_data_exist(data_name):
    if (os.path.isfile(f"{path_name}{data_name}.csv")) and time.strftime(
        "%Y-%m-%d", time.gmtime(os.path.getmtime(f"{path_name}{data_name}.csv"))
    ) == str(date.today()):
        return True
    else:
        return False

# read data every day
def read_data_fred(symb, data_name, columns_name, start=start_str, end=end_str):
    if check_data_exist(data_name):
        df = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 
    else:
      try:
        df = web.DataReader(symb, "fred", start=start, end=end)
        df=df.dropna()
        df.columns=columns_name
        df.to_csv(f"{path_name}{data_name}.csv")
      except:
        df = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 
    return df


# read date every month
def read_data_fred_month(symb, data_name, columns_name, start=start_str, end=end_str):
  df=pd.DataFrame()
  if (os.path.isfile(f"{path_name}{data_name}.csv")):
    if end_time.day==15 and time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(f"{path_name}{data_name}.csv"))) != str(date.today()):
        df = web.DataReader(symb, "fred", start=start, end=end)
        df=df.dropna()
        df.columns=columns_name
        df.to_csv(f"{path_name}{data_name}.csv")
    else: 
      df = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 
  else:
    try:
      df = web.DataReader(symb, "fred", start=start, end=end)
      df=df.dropna()
      df.columns=columns_name
      df.to_csv(f"{path_name}{data_name}.csv")
    except:
      df = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 
  return df

def show_graph(data_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig.update_layout(height=700)
    fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 30}
    fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
    fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
    # Add traces
    for col in data_df.columns:
        fig.add_trace(
            go.Scatter(x=data_df.index, y=data_df[col], name=col, mode='lines', line=dict(width=1)),
            secondary_y=True,
        )
    return fig

def yield_curve():
  symbols=['DFF','DTB3','DTB6','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30'] 
  columns_name=['Fed_Funds_Eff._Rate','3_Month_TBill','6_Month_TBill','1Y_Treasury','2Y_Treasury','3Y_Treasury','5Y_Treasury','7Y_Treasury','10Y_Treasury','20Y_Treasury','30Y_Treasury']
  df_data=read_data_fred(symbols,'US_Interest_rate',columns_name)
  df_data=df_data.dropna()
  #df_data.index = pd.to_datetime(df_data.index, format = "%Y-%m-%d").strftime('%Y-%m-%d')
  color = ['#F98404', '#aefeff','#8bcbcc', '#689899','#466666']
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  for i in range(0,5):
    df=pd.DataFrame()
    df=df_data.iloc[[-252*i-1]].T
    col=str(df.columns[0])
    fig.add_trace(
        go.Scatter(x=df.index, y=df[col].values,name=col,mode='lines+markers',marker_color=color[i]),secondary_y=True,
    )
  fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 30}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  return fig

def interest_rate_t_bill():
  symbols=['DFF','DTB3','DTB6','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30'] 
  columns_name=['Fed Funds Eff. Rate','3 Month TBill','6 Month TBill','1Y Treasury','2Y Treasury','3Y Treasury','5Y Treasury','7Y Treasury','10Y Treasury','20Y Treasury','30Y Treasury']
  t_bill=['Fed Funds Eff. Rate','3 Month TBill','6 Month TBill','1Y Treasury']
  df_data=read_data_fred(symbols,'US_Interest_rate',columns_name)
  df_data=df_data[t_bill]

  list_items=[]
  for x in t_bill:
    dic={}
    dic['name']=x
    dic['current']=df_data.iloc[-1][x]
    dic['min']=df_data[x].min()
    dic['max']=df_data[x].max()
    list_items.append(dic)
  fig=show_graph(df_data)
  return fig, list_items

def interest_rate_t_bond():
  symbols=['DFF','DTB3','DTB6','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30'] 
  columns_name=['Fed Funds Eff. Rate','3 Month TBill','6 Month TBill','1Y Treasury','2Y Treasury','3Y Treasury','5Y Treasury','7Y Treasury','10Y Treasury','20Y Treasury','30Y Treasury']
  t_bond=['2Y Treasury','3Y Treasury','5Y Treasury','7Y Treasury','10Y Treasury','20Y Treasury','30Y Treasury']
  df_data=read_data_fred(symbols,'US_Interest_rate',columns_name)
  df_data=df_data[t_bond]
  fig=show_graph(df_data)

  list_items=[]
  for x in t_bond:
    dic={}
    dic['name']=x
    dic['current']=df_data.iloc[-1][x]
    dic['min']=df_data[x].min()
    dic['max']=df_data[x].max()
    list_items.append(dic)
  return fig, list_items

def tips_rate():
  symbols=['DFII5','DFII10','DFII20','DFII30'] 
  columns_name=['TIPS 5-Year','TIPS 10-Year','TIPS 20-Year','TIPS 30-Year']
  df_data=read_data_fred(symbols,'US_TIPS_rate',columns_name)
  fig=show_graph(df_data)

  list_items=[]
  for x in columns_name:
    dic={}
    dic['name']=x
    dic['current']=df_data.iloc[-1][x]
    dic['min']=df_data[x].min()
    dic['max']=df_data[x].max()
    list_items.append(dic)
  return fig, list_items


def expected_inflation():
  start_inflation=(start_time-timedelta(days=365)).strftime("%Y-%m-%d")
  symbols3=['DGS10','DFII10'] 
  columns_name3=['10Y Treasury','10Y TIPS']
  df_infl_expec=read_data_fred(symbols3,'inflation_expectation',columns_name3)
  df_infl_expec['expected Inflation']=df_infl_expec['10Y Treasury']-df_infl_expec['10Y TIPS']
  df=read_data_fred('CPIAUCSL','core_cpi',['CPIAUCSL'], start=start_inflation)
  df['CPI Growth']=(df/df.shift(12)-1)*100
  df_infl_expec=df_infl_expec.dropna()
  df=df.dropna()
  columns_list=df_infl_expec.columns
  list_items=[]
  for x in columns_list:
    dic={}
    dic['name']=x
    dic['current']=round(df_infl_expec.iloc[-1][x],2)
    dic['min']=round(df_infl_expec[x].min(),2)
    dic['max']=round(df_infl_expec[x].max(),2)
    list_items.append(dic)
  dic={}
  dic['name']='CPI Growth'
  dic['current']=round(df.iloc[-1]['CPI Growth'],2)
  dic['min']=round(df['CPI Growth'].min(),2)
  dic['max']=round(df['CPI Growth'].max(),2)
  list_items.append(dic)
  fig1 = go.Figure()
  fig1.add_trace(go.Scatter(x=df_infl_expec.index, y=df_infl_expec['10Y Treasury'], name='10Y Treasury', fill=None, line=dict(color="#aefeff", width=1))) # fill down to xaxis
  fig1.add_trace(go.Scatter(x=df_infl_expec.index, y=df_infl_expec['10Y TIPS'],name='10Y TIPS', fill='tonexty', line=dict(color="#E60965", width=1))) # fill to trace0 y
  fig1.add_trace(go.Scatter(x=df_infl_expec.index, y=df_infl_expec['expected Inflation'], name='expected Inflation', line=dict( width=1))) # fill to trace0 y
  fig1.add_trace(go.Scatter(x=df.index, y=df['CPI Growth'], name='Core CPI growth',mode='lines+markers',line=dict( width=1.5) )) # fill to trace0 y
  fig1["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 30}
  fig1["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig1.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig1.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig1.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig1.update_xaxes(range=[df_infl_expec.index[100], df_infl_expec.index[-1]])
  return fig1, list_items

def cpi_inflation():
  symbols=['WPU083','CPIENGSL','CPIHOSNS','CPIFABSL','CPITRNSL','CPIAPPSL','CUSR0000SETA02','CUUR0000SETA01','CPIAUCSL'] 
  columns_name=['CPI Lumber','CPI Energy','CPI Housing','CPI Food','CPI Transportation','CPI Apparel','Used Cars and Trucks','New cars/trucks','CPI core']
  start_inflation=(start_time+timedelta(days=365)).strftime("%Y-%m-%d")
  df= read_data_fred_month(symbols,'CPIs',columns_name,start_inflation)
  df_growth=(df/df.shift(12)-1)*100
  df_growth=df_growth.dropna()
  df_growth=round(df_growth,2)

  list_items=[]
  for x in columns_name:
    dic={}
    dic['name']=x
    dic['current']=df_growth.iloc[-1][x]
    dic['min']=df_growth[x].min()
    dic['max']=df_growth[x].max()
    list_items.append(dic)

  fig2 = go.Figure(data=go.Heatmap(
                x=df_growth.index,
                y=columns_name,
                z=df_growth.T,
                hoverongaps = False,
                zmin=-15, zmax=15,colorscale = 'turbo',
                hovertemplate= '%{z}%',
                xgap =1,
                ygap =1,))

  fig2.update_traces(name='', selector=dict(type='heatmap')) 
  fig2["layout"]["margin"] = {"l": 10, "r": 10, "b": 10, "t": 10}
  fig2.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig2.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig2.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
      
  return fig2, list_items