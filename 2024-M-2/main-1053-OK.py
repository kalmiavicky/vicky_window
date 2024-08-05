import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

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
        file_path = r'C:\Users\user\Documents\vicky_window\2024-M-2\mangodata\MangoIrwin.csv'
        
        # 使用數據處理函數
        df = process_mango_data(file_path, market)
        
        print(f"成功加載 {market} 的數據，共 {len(df)} 行")
        print(df.head())  # 打印前幾行數據
        
        return df
    except Exception as e:
        print(f"載入數據時發生錯誤：{e}")
        return None

# 創建一個函數來生成常態分布圖
def generate_distribution_plot(df, column='平均價(元/公斤)'):
    try:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[column], kde=True, element='step', stat="density", kde_kws=dict(cut=3), alpha=.4, edgecolor=(1, 1, 1, .4))
        plt.ylabel('密度')
        plt.xlabel(column)
        
        # 將圖像保存到內存中
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        
        # 將圖像轉換為 base64 字符串
        img_str = base64.b64encode(buf.getvalue()).decode()
        return f'data:image/png;base64,{img_str}'
    except Exception as e:
        print(f"生成分布圖時發生錯誤：{e}")
        return None

# 創建箱型圖的函數
def create_box_plot(df, column='平均價(元/公斤)'):
    """
    創建箱型圖的函數

    參數:
    df (pandas.DataFrame): 包含數據的 DataFrame
    column (str): 用於創建箱型圖的列名

    返回:
    plotly.graph_objs._figure.Figure: Plotly 圖形對象
    """
    try:
        fig = px.box(df, y=column, title=f'{column}箱型圖')
        fig.update_layout(
            yaxis_title=column,
            xaxis_title='',
            showlegend=False,
            height=400
        )
        return fig
    except Exception as e:
        print(f"創建箱型圖時發生錯誤：{e}")
        return None

# 創建數據表格
def create_data_table(df, market):
    if df is None:
        return html.Div("無法載入數據，請檢查數據源。", style={'textAlign': 'center', 'color': 'red'})
    elif df.empty:
        return html.Div(f"{market} 數據為空。", style={'textAlign': 'center', 'color': 'orange'})
    
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

# 創建區塊函數
def create_data_block(title, id):
    return html.Div([
        html.H3(title, style={'textAlign': 'center', 'fontSize': '16px', 'marginBottom': '10px'}),
        html.Div(id=id, children=[
            html.P("尚未實現", style={'textAlign': 'center', 'color': 'gray'})
        ])
    ], style={
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'padding': '15px',
        'margin': '10px',
        'boxShadow': '0 0 5px rgba(0,0,0,0.1)',
        'backgroundColor': '#f9f9f9'
    })

# 創建區塊組
def create_block_group(market):
    return html.Div([
        html.Div([
            create_data_block(f"{market} 平均價格資料", f"{market}-average-price"),
            create_data_block(f"{market} 箱型圖", f"{market}-box-plot"),
            create_data_block(f"{market} 常態分布", f"{market}-normal-distribution"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}),
        html.Div([
            create_data_block(f"{market} 四分位數距數據", f"{market}-quartile-data"),
            create_data_block(f"{market} 實際值與預測值", f"{market}-actual-predicted"),
            create_data_block(f"{market} 實際值與預測值圖", f"{market}-actual-predicted-plot"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}),
        html.Div([
            create_data_block(f"{market} SARIMA模型的時間序列分析與預測數據", f"{market}-sarima-data"),
            create_data_block(f"{market} SARIMA模型的時間序列分析與預測", f"{market}-sarima-plot"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
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

# MT1-1 平均價資料處理函數
def process_average_price(df):
    """
    處理平均價資料的函數
    
    參數:
    df (pandas.DataFrame): 包含原始數據的DataFrame
    
    返回:
    pandas.DataFrame: 處理後的平均價資料
    """
    try:
        # 提取平均價格列
        price = df['平均價(元/公斤)']
        
        # 特徵欄位: 平均價(元/公斤)
        anal_data = pd.DataFrame(price, columns=['平均價(元/公斤)'])
        
        # 計算基本統計資訊
        stats = anal_data['平均價(元/公斤)'].describe()
        
        # 創建一個新的DataFrame來存儲統計資訊
        stats_df = pd.DataFrame({
            '統計量': stats.index,
            '值': stats.values
        })
        
        return stats_df
    except Exception as e:
        print(f"處理平均價資料時發生錯誤：{e}")
        return None

# 更新回調函數
@app.callback(
    [Output('台北二-normal-distribution', 'children'),
     Output('台北二-box-plot', 'children'),
     Output('台北二-average-price', 'children')],  # 新增這行
    Input('url', 'pathname')
)
def update_taipei_mk2_plots(pathname):
    if pathname == '/taipei_mk2_irwin':
        df = load_data('台北二')
        if df is not None:
            # 常態分布圖
            dist_img_src = generate_distribution_plot(df)
            dist_img = html.Img(src=dist_img_src, style={'width': '100%'}) if dist_img_src else html.P("無法生成分布圖", style={'textAlign': 'center', 'color': 'red'})
            
            # 箱型圖
            box_plot = create_box_plot(df)
            box_plot_div = dcc.Graph(figure=box_plot) if box_plot is not None else html.P("無法生成箱型圖", style={'textAlign': 'center', 'color': 'red'})
            
            # 平均價資料
            avg_price_data = process_average_price(df)
            avg_price_table = dash_table.DataTable(
                data=avg_price_data.to_dict('records'),
                columns=[{"name": i, "id": i} for i in avg_price_data.columns],
                style_cell={'textAlign': 'left'},
                style_header={'fontWeight': 'bold'}
            ) if avg_price_data is not None else html.P("無法處理平均價資料", style={'textAlign': 'center', 'color': 'red'})
            
            return dist_img, box_plot_div, avg_price_table
    return html.P("數據未加載", style={'textAlign': 'center', 'color': 'gray'}), html.P("數據未加載", style={'textAlign': 'center', 'color': 'gray'}), html.P("數據未加載", style={'textAlign': 'center', 'color': 'gray'})

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(f"當前路徑: {pathname}")  # 添加這行來檢查路徑
    if pathname == '/taipei_mk1_irwin':
        df = load_data('台北一')
        return html.Div([
            create_data_table(df, '台北一'),
            create_block_group('台北一')
        ])
    elif pathname == '/taipei_mk2_irwin':
        df = load_data('台北二')
        return html.Div([
            create_data_table(df, '台北二'),
            create_block_group('台北二')
        ])
    elif pathname == '/':
        return html.Div(html.H3("歡迎來到機器學習芒果分析系統", style={'textAlign': 'center', 'fontSize': '20px'}))
    elif pathname == '/taipei_mk1_chiinhwang':
        df = load_data('台北一')  # 注意：這裡可能需要修改數據加載邏輯以適應金煌芒果
        return html.Div([
            create_data_table(df, '台北一金煌'),
            create_block_group('台北一金煌')
        ])
    elif pathname == '/taipei_mk2_chiinhwang':
        df = load_data('台北二')  # 注意：這裡可能需要修改數據加載邏輯以適應金煌芒果
        return html.Div([
            create_data_table(df, '台北二金煌'),
            create_block_group('台北二金煌')
        ])
    else:
        return html.Div(html.H3("404 頁面未找到", style={'textAlign': 'center', 'fontSize': '20px'}))

if __name__ == '__main__':
    app.run_server(debug=True)