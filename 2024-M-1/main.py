from dash import Dash, html, dcc
from flask import Flask
import dash_bootstrap_components as dbc

# 創建Flask應用
server = Flask(__name__)

# 創建Dash應用，並使用Flask server
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義頁面佈局
app.layout = html.Div([
    html.H1("機器學習芒果分析", className="text-center mt-4 mb-4"),

    # 導航欄
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("首頁", href="#", active=True)),
        dbc.NavItem(dbc.NavLink("芒果愛文 台北一", href="#")),
        dbc.NavItem(dbc.NavLink("芒果愛文 台北二", href="#")),
        dbc.NavItem(dbc.NavLink("芒果金煌 台北一", href="#")),
        dbc.NavItem(dbc.NavLink("芒果全項 台北一", href="#")),
    ], className="mb-4"),

    # 主要內容區域
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("芒果愛文 台北一.csv 資料")), width=12, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n平均值資料")), width=4),
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n箱型圖")), width=4),
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n常態分布")), width=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n未出現分位數\n(IQR)*Q3-Q1 與上\n邊界(下限)低於\n邊界(上限) 資料")), width=4),
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n實際值 vs 預測值")), width=4),
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\n實際值 vs 預測值 圖")), width=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\nSARIMA 模型的時間序列分析和預測資料")), width=4),
            dbc.Col(dbc.Card(dbc.CardBody("MT1-1\nSARIMA 模型的時間序列分析和預測")), width=8),
        ]),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)