# main.py
#首頁+
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

# 假設我們有一個函數來加載數據
def load_data():
    # 這裡應該是實際加載數據的代碼
    # 為了示例，我們使用一個假數據
    df = pd.DataFrame({
        '日期': ['2014/4/1', '2014/4/3', '2014/4/4', '2014年4月8日', '2014年4月9日', '2014/4/10', '2014/4/11', '2014/4/12', '2014/4/13', '2014/4/15'],
        '市場': ['台北二'] * 10,
        '產品展示': ['芒果愛文'] * 10,
        '上價': [108.3, 120, 123.9, 90, 60, 90, 95, 103.3, 97.8, 66.5],
        '中價': [73.5, 116.7, 95.7, 69.8, 46.8, 80.4, 76.7, 60.6, 58.4, 45],
        '下價': [43.7, 105, 55.6, 51.3, 32.5, 72, 50, 48.4, 35, 33.8],
        '平均價(元/公斤)': [74.5, 115, 93.3, 70.2, 46.6, 80.7, 75, 66.7, 61.6, 47.1],
        '交易量(公斤)': [36, 18, 45, 34, 50, 18, 18, 305, 278, '第772筆']
    })
    return df

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
    return html.Div([
        html.H2("芒果愛文台北一.csv 數據", style={'textAlign': 'center', 'marginBottom': '15px', 'fontSize': '20px'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': '12px'},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
            ],
            page_size=10  # 設置每頁顯示的行數
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