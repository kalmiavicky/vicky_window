#01.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot

# 資料路徑
file_path = r'C:\Users\win\Documents\vicky_window\2024-M-1\mangodata\MangoIrwin.csv'

# 讀取CSV資料
data = pd.read_csv(file_path)

# 將資料轉換為DataFrame
df = pd.DataFrame(data)

# 指定市場
market = '台北一'

# 篩選出 "台北一" 市場的所有資料並使用 .loc 進行操作
df_taipei = df.loc[df['市場'] == market].copy()

# 顯示篩選出的資料
print(df_taipei)

# 如果需要進一步處理數據，如轉換日期格式和提取年、月、日，請取消以下註釋

# 將'日期'轉換為datetime格式
df_taipei['日期'] = pd.to_datetime(df_taipei['日期'])
# 從'日期'中提取年、月、日
df_taipei['年份'] = df_taipei['日期'].dt.year
df_taipei['月份'] = df_taipei['日期'].dt.month
df_taipei['日'] = df_taipei['日期'].dt.day

# 顯示處理後的資料
print(df_taipei)






