import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
import os
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib import font_manager

rcParams['font.family'] = 'SimHei'  # 設置為支持中文的字型名稱
rcParams['axes.unicode_minus'] = False  # 正確顯示負號
# 指定中文字型
font_path = '/usr/share/fonts/truetype/arphic/ukai.ttc'  # 這是中文字型的路徑，根據實際情況調整
font_prop = font_manager.FontProperties(fname=font_path)

# 處理台北二市場的芒果愛文數據
def taipei_mk2(file_path, market):
    # 讀取CSV資料
    data = pd.read_csv(file_path)

    # 將資料轉換為DataFrame
    df = pd.DataFrame(data)
    
    # 篩選出 "台北二" 市場的所有資料並使用 .loc 進行操作
    df_taipei = df.loc[df['市場'] == market].copy()

    # 將'日期'轉換為datetime格式
    df_taipei['日期'] = pd.to_datetime(df_taipei['日期'])
    # 從'日期'中提取年, 月, 日
    df_taipei['年份'] = df_taipei['日期'].dt.year
    df_taipei['月份'] = df_taipei['日期'].dt.month
    df_taipei['日'] = df_taipei['日期'].dt.day

    # 移除交易量中的逗號，並轉換為數值型態
    df_taipei['交易量(公斤)'] = df_taipei['交易量(公斤)'].str.replace(',', '').astype(float)

    # 檢查日期欄位是否有重複值，並移除重複日期
    df_taipei = df_taipei.drop_duplicates(subset=['日期'])

    # 按年份分組並收集日期資料到字典中
    year_datas = {}
    for year, group in df_taipei.groupby('年份'):
        year_datas[year] = {
            '日期': group['日期'].dt.strftime('%Y/%m/%d').tolist(),
            '市場': group['市場'].tolist(),
            '產品': group['產品'].tolist(),
            '上價': group['上價'].tolist(),
            '中價': group['中價'].tolist(),
            '下價': group['下價'].tolist(),
            '平均價(元/公斤)': group['平均價(元/公斤)'].tolist(),
            '交易量(公斤)': group['交易量(公斤)'].tolist()    
        }

    # 創建空的DataFrame來存儲結果
    df_taipei_mk2 = pd.DataFrame()

    # 迴圈處理每個年份的資料
    for year, year_data in year_datas.items():
        df_year_data = pd.DataFrame(year_data)
        df_year_data['日期'] = pd.to_datetime(df_year_data['日期'])
        
        # 生成完整的日期範圍（這裡假設所有資料都是4月到9月的）
        start_date = f'{year}-04-01'
        end_date = f'{year}-09-30'
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 將日期設置為索引
        df_year_data.set_index('日期', inplace=True)

        # 重新索引以包含所有日期
        df_year_data = df_year_data.reindex(date_range)

        # 使用線性插值法填補缺失值
        df_year_data = df_year_data.infer_objects()
        df_year_data = df_year_data.interpolate(method='linear')

        # 使用前向填充和後向填充來處理剩餘的缺失值
        df_year_data = df_year_data.ffill().bfill()

        # 將交易量(公斤)轉換為整數
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].astype(int)

        # 填充市場和產品欄位
        df_year_data['市場'] = df_year_data['市場'].ffill().bfill()
        df_year_data['產品'] = df_year_data['產品'].ffill().bfill()

        # 重置索引並添加年份列
        df_year_data.reset_index(inplace=True)
        
        # 將索引顯示到日期欄位
        df_year_data.rename(columns={'index': '日期'}, inplace=True)
        
        # 將處理好的數據添加到結果DataFrame中
        df_taipei_mk2 = pd.concat([df_taipei_mk2, df_year_data], ignore_index=True)

    return df_taipei_mk2

# 計算四分位數據
def calculate_quartiles(df):
    price = df['平均價(元/公斤)']
    Q1 = price.quantile(0.25)
    Q3 = price.quantile(0.75)
    IQR = Q3 - Q1
    Upper = Q3 + 1.5 * IQR
    Lower = Q1 - 1.5 * IQR
    return {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'Upper': Upper,
        'Lower': Lower
    }

# 生成盒鬚圖、常態分布圖等
def generate_plots(df, output_dir='analy_irwin_imgs'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    price = df['平均價(元/公斤)']

    # 箱型圖
    plt.figure(figsize=(8, 6))
    plt.boxplot(price, showmeans=True)
    plt.title('平均價(元/公斤) 箱型圖')
    plt.ylabel('價格 (元/公斤)')
    box_plot = os.path.join(output_dir, 'box_plot_2.png')
    plt.savefig(box_plot)
    plt.close()

    # 常態分布圖
    plt.figure(figsize=(10, 6))
    sns.histplot(price, kde=True, stat="density")
    plt.title('平均價(元/公斤) 分布圖')
    plt.xlabel('價格 (元/公斤)')
    plt.ylabel('密度')
    distribution_plot = os.path.join(output_dir, 'distribution_plot_2.png')
    plt.savefig(distribution_plot)
    plt.close()

    return box_plot, distribution_plot

# 時間序列分析和SARIMA模型
def time_series_analysis(df, output_dir='analy_irwin_imgs'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
   
    # 目標值
    y = df['平均價(元/公斤)']

    # 分割資料為訓練集和測試集
    train_size = int(len(y) * 0.8)
    train, test = y.iloc[:train_size], y.iloc[train_size:]

    # 建立和訓練SARIMA模型
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))  # Example of reducing seasonal periods to 7 days
    model_fit = model.fit(disp=False)

    # 預測
    y_pred_train = model_fit.predict(start=train.index[0], end=train.index[-1], dynamic=False)
    y_pred_test = model_fit.predict(start=test.index[0], end=test.index[-1], dynamic=False)

    # 計算評估指標
    mse_train = mean_squared_error(train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(train, y_pred_train)

    mse_test = mean_squared_error(test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(test, y_pred_test)

    # 繪製SARIMA模型結果
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label='訓練資料')
    plt.plot(test.index, test, label='測試資料')
    plt.plot(train.index, y_pred_train, color='red', linestyle='--', label='訓練預測')
    plt.plot(test.index, y_pred_test, color='green', linestyle='--', label='測試預測')
    plt.xlabel('時間')
    plt.ylabel('平均價(元/公斤)')
    plt.title('SARIMA模型的時間序列分析和預測')
    plt.legend()

    sarima_plot = os.path.join(output_dir, 'sarima_model_analysis_2.png')
    plt.savefig(sarima_plot)
    plt.close()

    return {
        'mse_train': mse_train,
        'rmse_train': rmse_train,
        'mae_train': mae_train,
        'mse_test': mse_test,
        'rmse_test': rmse_test,
        'mae_test': mae_test,
        'sarima_plot': sarima_plot
    }

# 主函數
def main():
    file_path = r'C:\Users\user\Documents\vicky_window\2024-M-2\mangodata\MangoIrwin.csv'
    df_taipei_mk2 = taipei_mk2(file_path, '台北二')
    
    quartiles = calculate_quartiles(df_taipei_mk2)
    box_plot, distribution_plot = generate_plots(df_taipei_mk2)
    time_series_results = time_series_analysis(df_taipei_mk2)

    print("四分位數統計:", quartiles)
    print("生成的圖表:")
    print("盒鬚圖:", box_plot)
    print("常態分布圖:", distribution_plot)
    print("SARIMA模型分析結果:", time_series_results)

if __name__ == "__main__":
    main()
