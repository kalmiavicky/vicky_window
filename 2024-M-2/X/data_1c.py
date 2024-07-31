# data_1c.py
# 芒果愛文 台北一

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
import io
import base64

def load_and_process_data(file_path, market):
    """
    讀取CSV文件並處理數據
    """
    # 讀取CSV資料
    df = pd.read_csv(file_path)
    
    # 篩選出指定市場的所有資料
    df_market = df.loc[df['市場'] == market].copy()
    
    # 將'日期'轉換為datetime格式
    df_market['日期'] = pd.to_datetime(df_market['日期'])
    
    # 從'日期'中提取年、月、日
    df_market['年份'] = df_market['日期'].dt.year
    df_market['月份'] = df_market['日期'].dt.month
    df_market['日'] = df_market['日期'].dt.day
    
    return df_market

def process_uploaded_file(contents, filename):
    """
    處理上傳的文件
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, '不支持的文件格式'
        
        return df, None
    except Exception as e:
        print(f'處理文件時發生錯誤：{e}')
        return None, '處理文件時發生錯誤'

def plot_acf_pacf(data):
    """
    繪製ACF和PACF圖
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plot_acf(data, ax=axs[0])
    plot_pacf(data, ax=axs[1])
    return fig

def sarima_analysis(train, test):
    """
    進行SARIMA分析
    """
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    
    # 計算指標
    mse_train = mean_squared_error(train, results.fittedvalues)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(train, results.fittedvalues)
    
    mse_test = mean_squared_error(test, forecast)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(test, forecast)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(test.index, test, label='實際數據')
    ax.plot(test.index, forecast, label='預測數據')
    ax.legend()
    ax.set_title('SARIMA 預測結果')
    
    return fig, mse_train, rmse_train, mae_train, mse_test, rmse_test, mae_test

def create_box_plot(df):
    """
    創建箱型圖
    """
    fig = plt.figure(figsize=(10, 6))
    sns.boxplot(y=df['平均價(元/公斤)'])
    plt.title('平均價(元/公斤) 箱型圖')
    return fig

def create_distribution_plot(df):
    """
    創建分布圖
    """
    fig = plt.figure(figsize=(10, 6))
    sns.histplot(df['平均價(元/公斤)'], kde=True)
    plt.title('平均價(元/公斤) 分布圖')
    return fig

def create_time_series_plot(df):
    """
    創建時間序列圖
    """
    fig = plt.figure(figsize=(12, 6))
    plt.plot(df['日期'], df['平均價(元/公斤)'])
    plt.title('時間序列分析')
    plt.xlabel('日期')
    plt.ylabel('平均價(元/公斤)')
    return fig

# 可以在此處添加其他需要的數據處理或分析函數

if __name__ == '__main__':
    # 主程序入口點
    pass