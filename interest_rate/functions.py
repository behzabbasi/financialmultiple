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





