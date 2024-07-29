from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

app1 = Dash(__name__, requests_pathname_prefix='/dashboard/app1/')
app1.title = '芒果愛文 台北一 資料'

# 使用与“芒果愛文 台北一”相关的数据集
df = pd.read_csv('https://path_to_your_dataset/mango_aiwen_taipei1.csv')

app1.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': col, 'value': col} for col in df.columns],
                placeholder='Select X Axis Indicator'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': col, 'value': col} for col in df.columns],
                placeholder='Select Y Axis Indicator'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic', style={'display': 'none'}),  # 初始状态隐藏图表
])

@app1.callback(
    Output('indicator-graphic', 'figure'),
    Output('indicator-graphic', 'style'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value')
)
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type):
    if not xaxis_column_name or not yaxis_column_name:
        return {}, {'display': 'none'}
    
    fig = px.scatter(df, x=xaxis_column_name, y=yaxis_column_name)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
    
    return fig, {'display': 'block'}

