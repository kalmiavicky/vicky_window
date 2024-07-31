# main.py
import os
from dash import Dash, html, dcc
from flask import Flask, render_template
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from MangoIrwin1_2 import load_data, process_mango_data

# 創建Flask應用
server = Flask(__name__, template_folder='templates')

# 創建Dash應用，並使用Flask server
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 獲取當前腳本的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(current_dir, 'mangodata', 'MangoIrwin1_2.csv')

# 檢查檔案是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"找不到CSV檔案：{file_path}")

# 讀取數據
df = load_data(file_path)

# 處理芒果數據
mango_results = process_mango_data(df)

# 定義頁面佈局
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='app-content')
])

# 設置 Dash 應用的回調
@app.callback(
    Output('app-content', 'children'),
    [Input('url', 'pathname')]
)
def update_layout(pathname):
    return html.Div([
        html.H1("機器學習芒果分析", className="text-center mt-4 mb-4"),

        # 導航欄
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("首頁", href="#", active=True)),
            dbc.NavItem(dbc.NavLink("芒果愛文 台北一", href="#")),
            dbc.NavItem(dbc.NavLink("芒果愛文 台北二", href="#")),
            dbc.NavItem(dbc.NavLink("芒果金煌 台北一", href="#")),
            dbc.NavItem(dbc.NavLink("芒果全項 台北一", href="#")),
        ], className="nav justify-content-center mb-4"),

        # 主要內容區域
        dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("芒果愛文 台北一.csv 數據", className="card-title"),
                    html.Div([
                        dbc.Table.from_dataframe(df.head(10), striped=True, bordered=True, hover=True)
                    ])
                ])), width=12, className="mb-4"),
            ]),

            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 平均價資料"),
                    html.P(mango_results["平均價資料"])
                ])), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 箱型圖"),
                    html.P(mango_results["箱型圖"])
                ])), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 常態分布"),
                    html.P(mango_results["常態分布"])
                ])), width=4),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 四分位距資料"),
                    html.P(mango_results["四分位距資料"])
                ])), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 實際值 vs 預測值"),
                    html.P(mango_results["實際值_vs_預測值"])
                ])), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 實際值 vs 預測值 圖"),
                    html.P(mango_results["實際值_vs_預測值_圖"])
                ])), width=4),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 SARIMA 模型的時間序列分析和預測數據"),
                    html.P(mango_results["SARIMA_分析資料"])
                ])), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5("MT1-1 SARIMA 模型的時間序列分析和預測"),
                    html.P(mango_results["SARIMA_分析圖"])
                ])), width=8),
            ]),
        ]),
    ])

@server.route('/')
def index():
    return render_template('index.html.jinja')

if __name__ == '__main__':
    app.run_server(debug=True)