# main.py
# 首頁+

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from flask import Flask

# 初始化 Flask 伺服器
server = Flask(__name__)

# 初始化 Dash 應用
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# 定義數據處理函數
def process_mango_data(file_path, market):
    """
    處理芒果數據的函數
    
    參數:
    file_path (str): CSV 文件的路徑
    market (str): 要篩選的市場名稱
    
    返回:
    pandas.DataFrame: 處理後的數據框
    """
    try:
        # 讀取 CSV 資料
        df = pd.read_csv(file_path)
        
        # 篩選指定市場的所有資料
        df_market = df.loc[df['市場'] == market].copy()
        
        # 將 '日期' 轉換為 datetime 格式
        df_market['日期'] = pd.to_datetime(df_market['日期'])
        
        # 從 '日期' 中提取年、月、日
        df_market['年份'] = df_market['日期'].dt.year
        df_market['月份'] = df_market['日期'].dt.month
        df_market['日'] = df_market['日期'].dt.day
        
        return df_market
    except Exception as e:
        print(f"處理數據時發生錯誤：{e}")
        return None

# 載入數據的函數
def load_data(market):
    try:
        # 資料路徑（請根據實際情況修改）
        file_path = r'C:\Users\win\Documents\vicky_window\2024-M-1\mangodata\MangoIrwin.csv'
        
        # 使用數據處理函數
        df = process_mango_data(file_path, market)
        
        return df
    except Exception as e:
        print(f"載入數據時發生錯誤：{e}")
        return None

# 創建數據表格
def create_data_table(df, market):
    if df is None or df.empty:
        return html.Div("無法載入數據，請檢查數據源。", style={'textAlign': 'center', 'color': 'red'})
    
    return html.Div([
        html.H2(f"愛文{market}.csv 數據", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={
                'height': '400px',
                'overflowY': 'auto',
                'border': '2px solid #ddd',
                'borderRadius': '5px',
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontSize': '14px',
                'minWidth': '100px', 'width': '100px', 'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'lightgrey',
                'position': 'sticky',
                'top': 0,
                'zIndex': 1000,
                'borderBottom': '2px solid #ddd',
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
            fixed_rows={'headers': True},
        )
    ], style={
        'border': '2px solid #ddd',
        'borderRadius': '10px',
        'padding': '20px',
        'marginBottom': '20px',
        'boxShadow': '0 0 5px rgba(0,0,0,0.1)'
    })

# 創建按鈕
def create_button(text, id):
    return dbc.Button(text, id=id, color="primary", className="me-1", style={'margin': '5px', 'fontSize': '12px'}, size="sm")

# 創建按鈕組
def create_button_group(market):
    return html.Div([
        html.Div([
            create_button(f"{market} 未出現分補充 (IQR)*Q3-Q1 與上邊界(下限)低於這界(上限) 數據", "button-1"),
            create_button(f"{market} 實際值與預測值", "button-2"),
            create_button(f"{market} 實際值與預測值圖", "button-3"),
            create_button(f"{market} SARIMA模型的時間序列分析與預測數據", "button-4"),
            create_button(f"{market} SARIMA模型的時間序列分析與預測", "button-5"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
    ], style={
        'border': '2px solid #ddd',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '20px',
        'boxShadow': '0 0 5px rgba(0,0,0,0.1)'
    })

# 定義應用佈局
def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div([
            html.H1("機器學習芒果分析", style={'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '24px'}),
            dbc.ButtonGroup([
                dbc.Button("首頁", color="primary", className="me-1", href="/", size="sm"),
                dbc.Button("芒果愛文 台北一", color="secondary", className="me-1", href="/taipei_mk1_irwin", size="sm"),
                dbc.Button("芒果愛文 台北二", color="secondary", className="me-1", href="/taipei_mk2_irwin", size="sm"),
                dbc.Button("芒果金煌 台北一", color="secondary", className="me-1", href="/taipei_mk1_chiinhwang", size="sm"),
                dbc.Button("芒果金煌 台北二", color="secondary", className="me-1", href="/taipei_mk2_chiinhwang", size="sm"),
            ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),
            html.Div(id='page-content')
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '30px',
            'border': '2px solid #ddd',
            'borderRadius': '10px',
            'boxShadow': '0 0 10px rgba(0,0,0,0.1)'
        })
    ])

app.layout = create_layout()

# 回調函數用於更新頁面內容
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/taipei_mk1_irwin':
        df = load_data('台北一')
        return html.Div([
            create_data_table(df, '台北一'),
            create_button_group('台北一')
        ])
    elif pathname == '/taipei_mk2_irwin':
        df = load_data('台北二')
        return html.Div([
            create_data_table(df, '台北二'),
            create_button_group('台北二')
        ])
    elif pathname == '/':
        return html.Div(html.H3("歡迎來到機器學習芒果分析系統", style={'textAlign': 'center', 'fontSize': '20px'}))
    else:
        return html.Div(html.H3("404 頁面未找到", style={'textAlign': 'center', 'fontSize': '20px'}))

if __name__ == '__main__':
    app.run_server(debug=True)