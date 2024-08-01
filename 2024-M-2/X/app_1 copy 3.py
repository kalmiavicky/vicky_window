# app_1.py
# 芒果愛文 台北一

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io
from data_1c import process_uploaded_file, plot_acf_pacf, sarima_analysis, create_box_plot, create_distribution_plot, create_time_series_plot

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

# 頁面路由
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.H2('歡迎使用機器學習芒果分析系統'),
            html.P('請選擇上方的按鈕以查看不同類型的芒果分析結果。')
        ])
    elif pathname == '/taipei_mk1_irwin':
        return create_analysis_layout('芒果愛文 台北一')
    elif pathname == '/taipei_mk2_irwin':
        return create_analysis_layout('芒果愛文 台北二')
    elif pathname == '/taipei_mk1_chiinhwang':
        return create_analysis_layout('芒果金煌 台北一')
    elif pathname == '/taipei_mk2_chiinhwang':
        return create_analysis_layout('芒果金煌 台北二')
    else:
        return '404 Page Not Found'

# 創建分析頁面的佈局
def create_analysis_layout(title):
    file_path = r'C:\Users\win\Documents\vicky_window\2024-M-1\mangodata\MangoIrwin.csv'
    
    # 讀取CSV資料
    df = pd.read_csv(file_path)
    
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
    
    # 這裡應該添加更多的分析內容，例如圖表、統計資訊等
    fig_time_series = create_time_series_plot(df_taipei)
    fig_acf_pacf = plot_acf_pacf(df_taipei['平均價(元/公斤)'])
    fig_box = create_box_plot(df_taipei)
    fig_distribution = create_distribution_plot(df_taipei)
    
    return html.Div([
        html.H2(title),
        html.P(f"分析結果將在這裡顯示。目前已處理 {len(df_taipei)} 筆資料。"),
        dcc.Graph(figure=fig_time_series),
        dcc.Graph(figure=fig_acf_pacf),
        dcc.Graph(figure=fig_box),
        dcc.Graph(figure=fig_distribution)
    ])

# 主程式
if __name__ == '__main__':
    app.run_server(debug=True)
