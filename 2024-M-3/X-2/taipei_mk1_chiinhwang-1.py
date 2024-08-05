# taipei_mk1_chiinhwang.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
from scipy import stats

def taipei_mk1(file_path, market):
    """
    讀取並處理指定市場的芒果數據。

    :param file_path: CSV 檔案路徑
    :param market: 市場名稱 ('台北一' 或 '台北二')
    :return: 處理後的 DataFrame
    """
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(file_path)
        
        # 印出列名，以便調試
        print("CSV 檔案的列名：", df.columns.tolist())
        
        # 檢查 '市場' 列是否存在
        if '市場' not in df.columns:
            raise ValueError("CSV 檔案中沒有 '市場' 列")
        
        # 根據指定市場篩選數據
        df = df[df['市場'] == market]
        
        # 檢查篩選後的數據是否為空
        if df.empty:
            raise ValueError(f"沒有找到 {market} 的數據")
        
        # 檢查 '日期' 列是否存在
        if '日期' not in df.columns:
            raise ValueError("CSV 檔案中沒有 '日期' 列")
        
        # 將日期轉換為 datetime 格式
        df['日期'] = pd.to_datetime(df['日期'])
        
        # 根據日期排序
        df = df.sort_values('日期')
        
        return df
    except Exception as e:
        print(f"讀取或處理數據時發生錯誤：{str(e)}")
        return None

def anal_mk1_data(df):
    """
    分析市場數據並生成統計摘要。

    :param df: 輸入的 DataFrame
    :return: 數據描述、相關係數矩陣、回歸模型、預測值、均方誤差和 R 平方值
    """
    try:
        # 檢查必要的列是否存在
        required_columns = ['平均價', '交易量', '平均重量']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 中缺少 '{col}' 列")

        # 生成數據描述統計
        all_descr = df.describe()
        
        # 計算相關係數矩陣
        correlation_matrix = df[required_columns].corr()
        
        # 準備回歸分析的數據
        X = df[['交易量', '平均重量']]
        y = df['平均價']
        
        # 分割訓練集和測試集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 建立線性回歸模型
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # 進行預測
        y_pred = model.predict(X_test)
        
        # 計算均方誤差和 R 平方值
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return all_descr, correlation_matrix, model, y_pred, mse, r2
    except Exception as e:
        print(f"分析數據時發生錯誤：{str(e)}")
        return None, None, None, None, None, None

# ... [其他函數保持不變] ...

# 主程式
if __name__ == "__main__":
    # 設定檔案路徑和市場名稱
    file_path = r'C:\Users\win\Documents\vicky_window\Mango_ML\mangodata\MangoChiinHwang.csv'
    market = '台北一'  # 或 '台北二'

    # 讀取和處理數據
    df = taipei_mk1(file_path, market)

    if df is not None:
        # 分析數據
        all_descr, correlation_matrix, model, y_pred, mse, r2 = anal_mk1_data(df)

        if all_descr is not None:
            # 繪製圖表
            plot_price_trend(df, market)
            plot_correlation_heatmap(correlation_matrix, market)
            plot_regression_results(df[['交易量', '平均重量']], df['平均價'], y_pred, market)
            plot_residuals(df['平均價'], y_pred, market)
            plot_qq_plot(df['平均價'], y_pred, market)

            # 輸出結果
            print(f"{market} 芒果金煌數據分析結果：")
            print(all_descr)
            print(f"\n均方誤差: {mse}")
            print(f"R 平方值: {r2}")
        else:
            print("無法完成數據分析")
    else:
        print("無法載入數據")