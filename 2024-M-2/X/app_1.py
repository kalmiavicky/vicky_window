# app_1.py
# 芒果愛文 台北一
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import base64
import io
from data_1c import plot_acf_pacf, sarima_analysis, load_and_process_data

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
    elif pathname in ['/taipei_mk1_irwin', '/taipei_mk2_irwin', '/taipei_mk1_chiinhwang', '/taipei_mk2_chiinhwang']:
        market = pathname.split('_')[-1]
        title = f"芒果{'愛文' if 'irwin' in pathname else '金煌'} 台北{'一' if 'mk1' in pathname else '二'}"
        return create_analysis_layout(title, market)
    else:
        return '404 Page Not Found'

# 創建分析頁面的佈局
def create_analysis_layout(title, market):
    return html.Div([
        html.H2(title),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                '拖放或 ',
                html.A('選擇檔案')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        dcc.Graph(id='box-plot'),
        dcc.Graph(id='distribution-plot'),
        dcc.Graph(id='time-series-plot'),
        dcc.Graph(id='acf-pacf-plot'),
        dcc.Graph(id='sarima-plot')
    ])

# 處理文件上傳並更新圖表
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('box-plot', 'figure'),
     Output('distribution-plot', 'figure'),
     Output('time-series-plot', 'figure'),
     Output('acf-pacf-plot', 'figure'),
     Output('sarima-plot', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('url', 'pathname')]
)
def update_output(contents, filename, pathname):
    if contents is None:
        return html.Div('請上傳CSV檔案'), {}, {}, {}, {}, {}
    
    try:
        df = parse_contents(contents, filename)
        if df is None:
            raise ValueError('無法解析文件內容')
        
        market = pathname.split('_')[-1]
        df = load_and_process_data(df, market)
        
        # 創建圖表
        box_plot = create_box_plot(df)
        distribution_plot = create_distribution_plot(df)
        time_series_plot = create_time_series_plot(df)
        acf_pacf_figure = create_acf_pacf_plot(df)
        sarima_figure = create_sarima_plot(df)
        
        return html.Div([
            html.H5(f'已上傳: {filename}'),
            html.Hr(),
            html.Div('數據分析結果將顯示在下方圖表中')
        ]), box_plot, distribution_plot, time_series_plot, acf_pacf_figure, sarima_figure
    
    except Exception as e:
        print(f'處理文件時發生錯誤：{e}')
        return html.Div(['處理文件時發生錯誤。']), {}, {}, {}, {}, {}

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return None

def create_box_plot(df):
    fig = go.Figure(data=[go.Box(y=df['平均價(元/公斤)'])])
    fig.update_layout(title='平均價(元/公斤) 箱型圖')
    return fig

def create_distribution_plot(df):
    fig = go.Figure(data=[go.Histogram(x=df['平均價(元/公斤)'])])
    fig.update_layout(title='平均價(元/公斤) 分布圖')
    return fig

def create_time_series_plot(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['日期'], y=df['平均價(元/公斤)'], mode='lines', name='實際數據'))
    fig.update_layout(title='時間序列分析')
    return fig

def create_acf_pacf_plot(df):
    acf_pacf_fig = plot_acf_pacf(df['平均價(元/公斤)'])
    fig = go.Figure(data=[go.Image(z=acf_pacf_fig)])
    fig.update_layout(title='ACF/PACF 圖')
    return fig

def create_sarima_plot(df):
    train, test = df['平均價(元/公斤)'][:int(len(df) * 0.8)], df['平均價(元/公斤)'][int(len(df) * 0.8):]
    sarima_fig, *_ = sarima_analysis(train, test)
    fig = go.Figure(data=[go.Image(z=sarima_fig)])
    fig.update_layout(title='SARIMA 分析圖')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    