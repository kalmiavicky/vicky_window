# test_script_C.py

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
import numpy as np
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot

# 設置中文字體，以正確顯示中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 將圖像保存為檔案並轉換為 Base64 編碼的字符串
def save_plot_as_image(plot_func, file_name):
    if plot_func is not None:
        try:
            buf = io.BytesIO()
            plot_func.savefig(buf, format='png')
            buf.seek(0)
            with open(file_name, 'wb') as f:
                f.write(buf.getvalue())
            buf.close()
            print(f"圖像已保存為 '{file_name}'")
            
            # 將圖像轉換為 Base64 編碼
            buf.seek(0)
            encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{encoded_img}"
        except Exception as e:
            print(f"保存圖像時發生錯誤：{e}")
            return None
    else:
        print(f"圖像 '{file_name}' 無法保存，因為 plot_func 為 None")
        return None

# 處理指定市場的資料
def taipei_mk1(file_path, market):
    """
    處理台北一市場的芒果數據。

    參數:
    file_path (str): CSV 文件的路徑
    market (str): 市場名稱，例如 '台北一'

    返回:
    pd.DataFrame: 處理後的數據框
    """
    # 讀取CSV資料    
    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)
    
    # 篩選出指定市場的所有資料
    df_taipei = df.loc[df['市場'] == market].copy()

    # 將'日期'轉換為datetime格式並提取年、月、日
    df_taipei['日期'] = pd.to_datetime(df_taipei['日期'])
    df_taipei['年份'] = df_taipei['日期'].dt.year
    df_taipei['月份'] = df_taipei['日期'].dt.month
    df_taipei['日'] = df_taipei['日期'].dt.day

    # 處理交易量數據
    df_taipei['交易量(公斤)'] = df_taipei['交易量(公斤)'].str.replace(',', '').astype(float)

    # 移除重複日期
    df_taipei = df_taipei.drop_duplicates(subset=['日期'])

    # 按年份分組處理資料
    df_taipei_mk1 = pd.DataFrame()
    for year, group in df_taipei.groupby('年份'):
        # 生成完整的日期範圍（4月到9月）
        date_range = pd.date_range(start=f'{year}-04-01', end=f'{year}-09-30', freq='D')
        
        # 重新索引並填充缺失值
        df_year_data = group.set_index('日期').reindex(date_range)
        for col in ['平均價(元/公斤)', '上價', '中價', '下價', '交易量(公斤)']:
            df_year_data[col] = df_year_data[col].interpolate(method='linear').ffill().bfill()
        
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].astype(int)
        df_year_data['市場'] = market
        df_year_data['產品'] = group['產品'].iloc[0] if not group['產品'].empty else '未知產品'
        
        df_taipei_mk1 = pd.concat([df_taipei_mk1, df_year_data.reset_index()])

    return df_taipei_mk1

# 進行數據分析
def anal_mk1_data(df_taipei_mk1, output_dir='analy_irwin_imgs'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 調整欄位順序
    df = df_taipei_mk1[['index', '上價', '中價', '下價', '平均價(元/公斤)', '交易量(公斤)']]
    df = df.rename(columns={'index': '日期'})  # 將 'index' 列重命名為 '日期'

    # 全部資料分布狀況
    all_descr = df.describe()

    price = df['平均價(元/公斤)']
    anal_data = pd.DataFrame(price, columns=['平均價(元/公斤)'])

    # 價位分布狀況
    descr = anal_data.describe()

    # 計算四分位距(IQR)與上下邊界
    Q1 = anal_data['平均價(元/公斤)'].quantile(0.25)
    Q3 = anal_data['平均價(元/公斤)'].quantile(0.75)
    IQR = Q3 - Q1
    Upper = Q3 + 1.5 * IQR
    Lower = Q1 - 1.5 * IQR

    # 箱型圖
    plt.figure(figsize=(3, 5))
    plt.boxplot(anal_data['平均價(元/公斤)'], showmeans=True)
    plt.title('平均價(元/公斤)')
    box_plot = plt.gcf()
    plt.close()

    # 計算偏態和峰度
    skew = f"偏態(Skewness):{anal_data['平均價(元/公斤)'].skew():.2f}"
    kurt = f"峰度(Kurtosis):{anal_data['平均價(元/公斤)'].kurt():.2f}"

    # 常態分布圖
    plt.figure()
    sns.histplot(anal_data['平均價(元/公斤)'], kde=True, element='step', stat="density", kde_kws=dict(cut=3), alpha=.4, edgecolor=(1, 1, 1, .4))
    plt.ylabel('密度')
    plt.xlabel('平均價(元/公斤)')
    distribution_plot = plt.gcf()
    plt.close()

    return all_descr, descr, box_plot, skew, kurt, distribution_plot

# 主函數
def main():
    # 設定市場名稱和檔案路徑
    market = '台北一'
    file_path = r'C:\Users\win\Documents\vicky_window\Mango_ML\mangodata\MangoChiinHwang.csv'
    
    # 獲取處理後的資料
    df_taipei_mk1 = taipei_mk1(file_path, market)
    
    # 打印 DataFrame 的內容
    print("DataFrame df_taipei_mk1 的內容:")
    print(df_taipei_mk1)
    
    # 進行數據分析
    all_descr, descr, box_plot, skew, kurt, distribution_plot = anal_mk1_data(df_taipei_mk1)
    
    # 顯示數據描述統計
    print("數據描述統計:")
    print(all_descr.to_string())
    print("\n價格描述統計:")
    print(descr.to_string())
    print(f"\n{skew}")
    print(f"{kurt}")


if __name__ == "__main__":
    main()
# 芒果金煌 台北一 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
import os

# 請整後的 "台北一" 市場資料
def taipei_mk1(file_path, market):
    # 讀取CSV資料    
    data = pd.read_csv(file_path)

    # 將資料轉換為DataFrame
    df = pd.DataFrame(data)
    
    # 篩選出 "台北一" 市場的所有資料並使用 .loc 進行操作
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
            # 將datetime轉換為字串列表
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
    df_taipei_mk1 = pd.DataFrame()

    # 迴圈處理每個年份的資料
    for year, year_data in year_datas.items():
        # 將資料轉換為DataFrame並將日期轉換為datetime格式
        df_year_data = pd.DataFrame(year_data)
        df_year_data['日期'] = pd.to_datetime(df_year_data['日期'])
        
        # 生成完整的日期範圍（這裡假設所有資料都是4月到8月的）
        start_date = f'{year}-04-01'
        end_date = f'{year}-08-31'
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 將日期設置為索引
        df_year_data.set_index('日期', inplace=True)

        # 重新索引以包含所有日期
        df_year_data = df_year_data.reindex(date_range)

        # 或者使用平均值插補
        df_year_data['平均價(元/公斤)'] = df_year_data['平均價(元/公斤)'].interpolate(method='linear')
        df_year_data['上價'] = df_year_data['上價'].interpolate(method='linear')
        df_year_data['中價'] = df_year_data['中價'].interpolate(method='linear')
        df_year_data['下價'] = df_year_data['下價'].interpolate(method='linear')
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].interpolate(method='linear')

        # 使用前向填充和後向填充來處理剩餘的缺失值
        df_year_data['平均價(元/公斤)'] = df_year_data['平均價(元/公斤)'].ffill().bfill()
        df_year_data['上價'] = df_year_data['上價'].ffill().bfill()
        df_year_data['中價'] = df_year_data['中價'].ffill().bfill()
        df_year_data['下價'] = df_year_data['下價'].ffill().bfill()
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].ffill().bfill()

        # 將交易量(公斤)轉換為整數
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].astype(int)

        # 填充市場和產品欄位
        market_value = year_data['市場'][0] if '市場' in year_data else '未知市場'
        product_value = year_data['產品'][0] if '產品' in year_data else '未知產品'
        df_year_data['市場'] = market_value
        df_year_data['產品'] = product_value

        # 重置索引並添加年份列
        df_year_data.reset_index(inplace=True)
        
        # 將索引顯示到日期欄位
        df_year_data.rename(columns={'index': '日期'}, inplace=True)
        
        # 將處理好的數據添加到結果DataFrame中
        df_taipei_mk1 = pd.concat([df_taipei_mk1, df_year_data], ignore_index=True)
    return df_taipei_mk1

# 盒鬚圖, 資料分布狀況, 偏態＆峰度, 常態分佈圖
def anal_mk1_data(df_taipei_mk1, output_dir='analy_chiinhwang_imgs'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 調整欄位順序
    df = df_taipei_mk1[['日期', '上價', '中價', '下價', '平均價(元/公斤)', '交易量(公斤)']]

    # 全部資料分布狀況
    all_descr = df.describe()

   
