# test_script.py
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
    file_path = r'C:\Users\win\Documents\vicky_window\Mango_ML\mangodata\MangoIrwin.csv'
    
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