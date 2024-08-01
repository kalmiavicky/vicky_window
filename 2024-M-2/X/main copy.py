# main.py

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask

# 導入各個芒果品種的數據處理模塊
import taipei_mk1_irwin
import taipei_mk1_chiinhwang
import taipei_mk2_irwin
import taipei_mk2_chiinhwang

# 初始化 Flask 應用
server = Flask(__name__)

# 初始化 Dash 應用
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義按鈕樣式
button_style = {
    'color': 'black',
    'backgroundColor': 'white',
    'border': '1px solid black',
    'margin': '5px'
}

# 定義標題樣式
title_style = {
    'textAlign': 'center',
    'marginBottom': '20px'
}

# 定義按鈕容器樣式
button_container_style = {
    'display': 'flex',
    'justifyContent': 'center',
    'marginBottom': '20px'
}

# 創建按鈕函數
def create_button(text, href):
    return dbc.Button(text, href=href, style=button_style)

# 定義應用佈局函數
def create_layout():
    return html.Div([
        html.H1("機器學習芒果分析", style=title_style),
        dcc.Location(id='url', refresh=False),
        html.Div([
            create_button("首頁", "/"),
            create_button("芒果愛文 台北一", "/taipei_mk1_irwin"),
            create_button("芒果金煌 台北一", "/taipei_mk1_chiinhwang"),
            create_button("芒果愛文 台北二", "/taipei_mk2_irwin"),
            create_button("芒果金煌 台北二", "/taipei_mk2_chiinhwang"),
        ], style=button_container_style),
        html.Div(id='page-content', style={'textAlign': 'center'})
    ])

# 設置應用佈局
app.layout = create_layout()

# 回調函數用於更新頁面內容
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return html.Div()  # 空白首頁
    elif pathname == '/taipei_mk1_irwin':
        return taipei_mk1_irwin.layout
    elif pathname == '/taipei_mk1_chiinhwang':
        return taipei_mk1_chiinhwang.layout
    elif pathname == '/taipei_mk2_irwin':
        return taipei_mk2_irwin.layout
    elif pathname == '/taipei_mk2_chiinhwang':
        return taipei_mk2_chiinhwang.layout
    else:
        return '404 頁面未找到'

if __name__ == '__main__':
    app.run_server(debug=True)