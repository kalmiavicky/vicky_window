# main.py
import os
from dash import Dash, html, dcc
from flask import Flask, render_template
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# 從 taipei_mk1_irwin 導入需要的函數
from taipei_mk1_irwin import taipei_mk1, anal_mk1_data, time_series

# 創建 Flask 應用
server = Flask(__name__, template_folder='templates')

# 創建 Dash 應用，並使用 Flask server
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 獲取當前腳本的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'mangodata', 'MangoIrwin.csv')

# 檢查檔案是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"找不到CSV檔案：{file_path}")

# 讀取數據
df_taipei_mk1 = taipei_mk1(file_path, '台北一')

# 進行數據分析
all_descr, descr, box_plot, skew, kurt, distribution_plot = anal_mk1_data(df_taipei_mk1)

# 設置 Dash 應用的回調
@app.callback(
    Output('app-content', 'children'),
    [Input('url', 'pathname')]
)
def update_layout(pathname):
    if pathname == "/" or pathname == "/home":
        return render_home_page()
    elif pathname == "/taipei1-irwin":
        return render_taipei1_irwin_page()

def render_home_page():
    return html.Div([
        html.H1("歡迎來到芒果分析首頁"),
        html.P("請從上方導航欄選擇要查看的分析內容。")
    ])

def render_taipei1_irwin_page():
    # 進行時間序列分析
    acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot = time_series(df_taipei_mk1)
    
    return html.Div([
        html.H1("芒果愛文 台北一 分析結果"),
        html.Div([
            html.H2("數據描述"),
            dcc.Markdown(all_descr.to_markdown()),
            html.H2("偏態和峰度"),
            html.P(f"{skew}, {kurt}"),
            html.H2("箱型圖"),
            html.Img(src=box_plot),
            html.H2("分布圖"),
            html.Img(src=distribution_plot),
            html.H2("時間序列分析結果"),
            html.P(f"{Training_MSE}, {Training_RMSE}, {Training_MAE}"),
            html.P(f"{Testing_MSE}, {Testing_RMSE}, {Testing_MAE}"),
            html.Img(src=sarima_model_plot),
            html.Img(src=combined_train_test_plot),
            html.Img(src=residuals_plot),
        ])
    ])

@server.route('/')
def index():
    return render_template('index.html.jinja')

if __name__ == '__main__':
    app.run_server(debug=True)
