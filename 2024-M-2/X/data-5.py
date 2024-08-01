# data.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
import os
import io
import base64

def load_and_process_data(file_path, market):
    # 讀取並處理數據的函數
    # 這裡包含taipei_mk1函數的邏輯
    pass

def analyze_data(df_taipei_mk1):
    # 數據分析函數
    # 這裡包含anal_mk1_data函數的邏輯
    pass

def time_series_analysis(df_taipei_mk1):
    # 時間序列分析函數
    # 這裡包含time_series函數的邏輯
    pass

def plot_to_base64(fig):
    # 將matplotlib圖形轉換為base64編碼
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')