# main.py
# 首頁+

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot

# 載入數據的函數
def load_data():
    try:
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

        # 將'日期'轉換為datetime格式
        df_taipei['日期'] = pd.to_datetime(df_taipei['日期'])
        # 從'日期'中提取年、月、日
        df_taipei['年份'] = df_taipei['日期'].dt.year
        df_taipei['月份'] = df_taipei['日期'].dt.month
        df_taipei['日'] = df_taipei['日期'].dt.day

        return df_taipei
    except Exception as e:
        print(f"載入數據時發生錯誤：{e}")
        return None

# 創建 Dash 應用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# 定義應用佈局
def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div([  # 主容器
            html.H1("機器學習芒果分析", style={'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '24px'}),
            dbc.ButtonGroup([
                dbc.Button("首頁", color="primary", className="me-1", href="/", size="sm"),
                dbc.Button("芒果愛文 台北一", color="secondary", className="me-1", href="/taipei_mk1_irwin", size="sm"),
                dbc.Button("芒果愛文 台北二", color="secondary", className="me-1", href="/taipei_mk2_irwin", size="sm"),
                dbc.Button("芒果金煌 台北一", color="secondary", className="me-1", href="/taipei_mk1_chiinhwang", size="sm"),
                dbc.Button("芒果金煌 台北二", color="secondary", className="me-1", href="/taipei_mk2_chiinhwang", size="sm"),
            ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),
            html.Div(id='page-content')
        ], style={'maxWidth': '1000px', 'margin': '0 auto', 'padding': '20px'})  # 主容器樣式
    ])

app.layout = create_layout()

# 創建數據表格
def create_data_table(df):
    if df is None or df.empty:
        return html.Div("無法載入數據，請檢查數據源。", style={'textAlign': 'center', 'color': 'red'})
    
    return html.Div([
        html.H2("芒果愛文台北一 數據", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={
                'height': '400px',  # 設置表格高度
                'overflowY': 'auto'  # 允許垂直滾動
            },
            style_cell={
                'textAlign': 'left',
                'padding': '5px',
                'fontSize': '12px',
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',  # 設置列寬
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'lightgrey',
                'position': 'sticky',
                'top': 0,  # 固定表頭
                'zIndex': 1000
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
            ],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
            fixed_rows={'headers': True},  # 固定表頭
        )
    ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '15px', 'marginBottom': '20px'})

# 創建按鈕
def create_button(text, id):
    return dbc.Button(text, id=id, color="primary", className="me-1", style={'margin': '5px', 'fontSize': '12px'}, size="sm")

# 創建按鈕組
def create_button_group():
    return html.Div([
        html.Div([
            create_button("MT1-1 未出現分補充 (IQR)*Q3-Q1 與上邊界(下限)低於這界(上限) 數據", "button-1"),
            create_button("MT1-1實際值與預測值", "button-2"),
            create_button("MT1-1實際值與預測值圖", "button-3"),
            create_button("MT1-1 SARIMA模型的時間序列分析與預測數據", "button-4"),
            create_button("MT1-1 SARIMA模型的時間序列分析與預測", "button-5"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
    ], style={'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '15px'})

# 回調函數用於更新頁面內容
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/taipei_mk1_irwin':
        df = load_data()
        return html.Div([
            create_data_table(df),
            create_button_group()
        ])
    elif pathname == '/':
        return html.Div(html.H3("歡迎來到機器學習芒果分析系統", style={'textAlign': 'center', 'fontSize': '20px'}))
    else:
        return html.Div(html.H3("404 頁面未找到", style={'textAlign': 'center', 'fontSize': '20px'}))

if __name__ == '__main__':
    app.run_server(debug=True)