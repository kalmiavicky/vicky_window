# main.py

# 導入必要的庫
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask, render_template, send_from_directory
import taipei_mk1_irwin  # 導入自定義模組 taipei_mk1_irwin
import os
from jinja2 import Environment, FileSystemLoader
from img_i import display_mango_images  # 導入圖片處理函數

# 初始化 Flask 伺服器
server = Flask(__name__)

# 設置 Jinja2 環境
env = Environment(loader=FileSystemLoader('templates'))

# 初始化 Dash 應用
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# 設定圖片目錄
IMAGES_FOLDER = 'static/images'

# 載入數據
def load_data(market):
    """
    根據市場名稱載入數據和描述統計。

    :param market: 市場名稱
    :return: DataFrame、數據描述統計
    """
    try:
        file_path = r'C:\Users\win\Documents\vicky_window\Mango_ML\mangodata\MangoIrwin.csv'
        df = taipei_mk1_irwin.taipei_mk1(file_path, market)
        all_descr, _, _, _, _, _ = taipei_mk1_irwin.anal_mk1_data(df)
        return df, all_descr
    except Exception as e:
        print(f"載入數據時發生錯誤：{e}")
        return None, None

# 創建數據表格
def create_data_table(df, market):
    """
    創建數據表格的 HTML。

    :param df: 數據 DataFrame
    :param market: 市場名稱
    :return: 表格的 HTML 區段
    """
    if df is None:
        return html.Div("無法載入數據，請檢查數據源。", style={'textAlign': 'center', 'color': 'red'})
    elif df.empty:
        return html.Div(f"{market} 數據為空。", style={'textAlign': 'center', 'color': 'orange'})
    
    return html.Div([
        html.H2(f"愛文{market} 數據", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        dash_table.DataTable(
            id=f'table-{market}',
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

# 創建數據描述部分
def create_description_section(all_descr, market):
    """
    創建數據描述統計區段的 HTML。

    :param all_descr: 數據描述統計的 DataFrame
    :param market: 市場名稱
    :return: 描述統計的 HTML 區段
    """
    if all_descr is None:
        return html.Div("無法載入數據描述統計。", style={'textAlign': 'center', 'color': 'red'})
    
    # 重新排版描述統計，與愛文台北二數據格式一致
    descr_str = all_descr.to_string()  # 使用 to_string() 以避免亂碼
    
    return html.Div([
        html.H2(f"{market} 數據描述統計", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        html.Div([
            html.Pre(descr_str, style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all',
                'fontFamily': 'monospace',
                'fontSize': '12px',
                'padding': '10px',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'backgroundColor': '#f8f9fa'
            })
        ], style={
            'border': '2px solid #ddd',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 0 5px rgba(0,0,0,0.1)'
        })
    ])

# 創建圖片顯示部分
def create_image_section(market):
    """
    創建圖片顯示區段的 HTML。

    :param market: 市場名稱
    :return: 圖片顯示的 HTML 區段
    """
    images = display_mango_images(market)
    if not images:
        return html.Div(f"無法載入 {market} 的圖片。", style={'textAlign': 'center', 'color': 'red'})
    
    return html.Div([
        html.H2(f"{market} 芒果分析圖", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        html.Div([
            html.Img(src=img, style={'width': '100%', 'marginBottom': '20px', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'})
            for img in images
        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '20px'
        })
    ], style={
        'border': '2px solid #ddd',
        'borderRadius': '10px',
        'padding': '20px',
        'marginBottom': '20px',
        'boxShadow': '0 0 5px rgba(0,0,0,0.1)'
    })

# 定義應用佈局
app.layout = html.Div([
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

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """
    根據 URL 路徑顯示不同的頁面內容。

    :param pathname: URL 路徑
    :return: 對應的 HTML 區段
    """
    if pathname == '/taipei_mk1_irwin':
        df, all_descr = load_data('台北一')
        return html.Div([
            create_data_table(df, '台北一'),
            create_description_section(all_descr, '台北一'),
            create_image_section('台北一')
        ])
    elif pathname == '/taipei_mk2_irwin':
        df, all_descr = load_data('台北二')
        return html.Div([
            create_data_table(df, '台北二'),
            create_description_section(all_descr, '台北二'),
            create_image_section('台北二')
        ])
    elif pathname == '/':
        return html.Div(html.H3("歡迎來到機器學習芒果分析系統", style={'textAlign': 'center', 'fontSize': '20px'}))
    else:
        return html.Div(html.H3("404 頁面未找到", style={'textAlign': 'center', 'fontSize': '20px'}))

if __name__ == '__main__':
    app.run_server(debug=True)
