import pandas as pd
import numpy as np
from datetime import date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
import pandas_datareader.data as web
import os, time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
path_name = os.path.join(BASE_DIR, 'data/beta/')


end_time = date.today()
start_time = end_time - timedelta(days=365 * 3)
end = end_time.strftime("%Y-%m-%d")
start = start_time.strftime("%Y-%m-%d")


def check_data_exist(data_name):
    if (os.path.isfile(f"{path_name}{data_name}.csv")) and time.strftime(
        "%Y-%m-%d", time.gmtime(os.path.getmtime(f"{path_name}{data_name}.csv"))
    ) == str(date.today()):
        return True
    else:
        return False

# read data every day
def read_data(symb, data_name, start=start, end=end):
    if check_data_exist(data_name):
        df = pd.read_csv(f"{path_name}{data_name}.csv", index_col=0) 

    else:
        df = web.DataReader(symb, "yahoo", start=start, end=end)
        df=df.dropna()
        df.to_csv(f"{path_name}{data_name}.csv")

    return df


def correlation(stock_ticker, benchmark_ticker):
    stock_df = web.DataReader(stock_ticker, data_source="yahoo", start=start, end=end)
    benchmark_df = web.DataReader(benchmark_ticker, data_source="yahoo", start=start, end=end)
    stock_df["returns"] = np.log(stock_df["Adj Close"] / stock_df["Adj Close"].shift(1))
    stock_df.dropna(inplace=True)
    benchmark_df["returns"] = np.log(
        benchmark_df["Adj Close"] / benchmark_df["Adj Close"].shift(1)
    )
    benchmark_df.dropna(inplace=True)
    x = np.array(benchmark_df["returns"]).reshape((-1, 1))
    y = np.array(stock_df["returns"])
    model = LinearRegression().fit(x, y)
    beta = round(model.coef_[0], 2)
    corr = round(benchmark_df["returns"].corr(stock_df["returns"]), 2)
    intercept = round(model.intercept_, 4)
    x = np.linspace(np.amin(benchmark_df["returns"]), np.amax(benchmark_df["returns"]))
    y = beta * x + intercept
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=benchmark_df["returns"],
            y=stock_df["returns"],
            mode="markers",
            marker=dict(size=7,color='#FFE194', opacity=0.7),
            name=f"return {stock_ticker} vs {benchmark_ticker}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=f"< y={beta}x+{intercept} > < Correlation: {corr} >",
        )
    )
    fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 10}
    fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}

    min_max_range = (
        max(
            abs(min(stock_df["returns"])),
            max(stock_df["returns"]),
            abs(min(benchmark_df["returns"])),
            max(benchmark_df["returns"]),
        )
    ) + 0.02
    fig.update_xaxes(range=[-min_max_range, min_max_range])
    fig.update_yaxes(range=[-min_max_range, min_max_range])
    fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')

    return (
        beta,
        corr,
        intercept,
        fig,
    )



def volatility():
    #vix = web.DataReader("^VIX", data_source="yahoo", start=start, end=end)
    #vxn = web.DataReader("^VXN", data_source="yahoo", start=start, end=end)
    vix=read_data("^VIX", 'VIX')
    vxn=read_data("^VXN", 'VXN')
    vix = vix[["Adj Close"]]
    vxn = vxn[["Adj Close"]]

    list_items=[]
    dic={}
    dic['name']='VIX'
    dic['current']=round(vix.iloc[-1]['Adj Close'],2)
    dic['min']=round(vix['Adj Close'].min(),2)
    dic['max']=round(vix['Adj Close'].max(),2)
    dic['std']=round(vix['Adj Close'].std(),2)
    list_items.append(dic)
    dic={}
    dic['name']='VXN'
    dic['current']=round(vxn.iloc[-1]['Adj Close'],2)
    dic['min']=round(vxn['Adj Close'].min(),2)
    dic['max']=round(vxn['Adj Close'].max(),2)
    dic['std']=round(vxn['Adj Close'].std(),2)
    list_items.append(dic)

    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(go.Scatter(x=vix.index,y=vix["Adj Close"],name="CBOE Volatility Index - VIX",line=dict(color="#E1578A", width=1),),secondary_y=False,)
    fig.add_trace(go.Scatter(x=vxn.index,y=vxn["Adj Close"],name="CBOE NASDAQ 100 Volatility - VXN",line=dict(color="#aefeff", width=1),),secondary_y=False,)
    fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 10, "t": 10}
    fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
    fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
    # fig.update_layout(height=400)
    return fig, list_items