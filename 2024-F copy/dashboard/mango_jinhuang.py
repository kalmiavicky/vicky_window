# dashboard/mango_jinhuang.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# 打印當前工作目錄
print("當前工作目錄:", os.getcwd())



# 使用正斜線的路徑
csv_path = r'C:\Users\user\Documents\vicky_window\2024-F copy\mangodata\MangoIrwin-2.csv'
print("嘗試讀取的文件路徑:", csv_path)

# 檢查文件是否存在
if os.path.exists(csv_path):
    print("文件存在")
    df = pd.read_csv(csv_path)
    print("CSV 文件列名:", df.columns.tolist())
    print("CSV 文件的前幾行:")
    print(df.head())
else:
    print("文件不存在")
    df = pd.DataFrame()  # 創建一個空的 DataFrame

# 根據實際的列名調整這些變量
date_column = 'date'  # 替換為實際的日期列名
price_column = 'price'  # 替換為實際的價格列名
volume_column = 'volume'  # 替換為實際的交易量列名

# 創建Dash應用
mango_jinhuang_app = dash.Dash(__name__, url_base_pathname='/dashboard/mango-jinhuang/')

# 定義布局
mango_jinhuang_app.layout = html.Div([
    html.H1('芒果金煌台北一數據分析'),
    dcc.Graph(id='price-trend'),
    dcc.Graph(id='volume-trend'),
    dcc.DatePickerRange(
        id='date-range',
        start_date=df[date_column].min() if date_column in df.columns and not df.empty else None,
        end_date=df[date_column].max() if date_column in df.columns and not df.empty else None,
        display_format='YYYY-MM-DD'
    )
])

# 回調函數來更新圖表
@mango_jinhuang_app.callback(
    [Output('price-trend', 'figure'),
     Output('volume-trend', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    if df.empty or date_column not in df.columns or price_column not in df.columns or volume_column not in df.columns:
        # 如果 DataFrame 為空或缺少必要的列，返回空圖表
        return px.line(title="數據不可用"), px.bar(title="數據不可用")
    
    filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
    
    price_fig = px.line(filtered_df, x=date_column, y=price_column, title='價格趨勢')
    volume_fig = px.bar(filtered_df, x=date_column, y=volume_column, title='交易量趨勢')
    
    return price_fig, volume_fig

# 如果直接運行此文件，啟動服務器
if __name__ == '__main__':
    mango_jinhuang_app.run_server(debug=True)