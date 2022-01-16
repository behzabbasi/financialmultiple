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





def yield_curve():
  symbols=['DFF','DTB3','DTB6','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30'] 
  columns_name=['Fed_Funds_Eff._Rate','3_Month_TBill','6_Month_TBill','1Y_Treasury','2Y_Treasury','3Y_Treasury','5Y_Treasury','7Y_Treasury','10Y_Treasury','20Y_Treasury','30Y_Treasury']
  df_data=read_data_fred(symbols,'US_yield_curve',columns_name)
  df_data=df_data.dropna()
  #print(df_data)
  color = ['#396EB0', '#811A0E','#B82514', '#E73623','#EF796C']
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  for i in range(0,5):
    df=df_data.iloc[[-365*i-1]].T
    col=str(df.columns[0])
    fig.add_trace(
        go.Scatter(x=df.index, y=df[col].values,name=col,mode='lines+markers',marker_color=color[i]),secondary_y=True,
    )
  fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 30}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  return fig