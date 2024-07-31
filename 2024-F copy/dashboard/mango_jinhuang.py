# dashboard/mango_jinhuang.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# 讀取芒果金煌北一的數據
df = pd.read_csv('芒果金煌北一.csv')

# 創建Dash應用
mango_jinhuang_app = dash.Dash(__name__, url_base_pathname='/dashboard/mango-jinhuang/')

# 定義布局
mango_jinhuang_app.layout = html.Div([
    html.H1('芒果金煌台北一數據分析'),
    dcc.Graph(id='price-trend'),
    dcc.Graph(id='volume-trend'),
    dcc.DatePickerRange(
        id='date-range',
        start_date=df['日期'].min(),
        end_date=df['日期'].max(),
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
    filtered_df = df[(df['日期'] >= start_date) & (df['日期'] <= end_date)]
    
    price_fig = px.line(filtered_df, x='日期', y='價格', title='價格趨勢')
    volume_fig = px.bar(filtered_df, x='日期', y='交易量', title='交易量趨勢')
    
    return price_fig, volume_fig

# 如果直接運行此文件，啟動服務器
if __name__ == '__main__':
    mango_jinhuang_app.run_server(debug=True)