import pandas_datareader.data as web
import plotly.graph_objects as go
from datetime import date, timedelta


end_time = date.today()
start_time = end_time - timedelta(days=365 * 3)
end = end_time.strftime("%Y-%m-%d")
start = start_time.strftime("%Y-%m-%d")


def psRatio():
  df_stock = web.DataReader('AAPL', data_source="yahoo", start=start, end=end)
  fig = go.Figure()
  fig["layout"]["margin"] = {"l": 20, "r": 20, "b": 20, "t": 20}
  fig["layout"]["legend"] = {"x": 0.01, "y": 1, "xanchor": "left"}
  fig.add_trace(go.Scatter(x=df_stock.index, y=df_stock["Close"], mode="lines", marker=dict(size=7, color='#FFCC1D'), fill='tozeroy',))
  fig.update_layout(plot_bgcolor='#424642',paper_bgcolor  ='#424642',legend_font_color='#fff',font_color='#fff') #314E52 #082032 #424642
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#808080')
  fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#808080')
  return fig