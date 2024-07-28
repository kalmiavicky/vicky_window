from flask import Flask, render_template, request
import data
from dash import Dash, dcc, html, Input, Output, State, callback
import pandas as pd  # 添加这一行导入 pandas 库
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

# 嵌入第一个 Dash 应用 (芒果品种选择)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

dash_app.layout = html.Div([
    html.Div([
        html.H4('芒果品種'),
        dcc.Checklist(
            options=[
                {'label': '芒果愛文', 'value': '芒果愛文'},
                {'label': '芒果金煌', 'value': '芒果金煌'}
            ],
            value=[],  # 默认不选中任何选项
            id='mango-types-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字体加大并增加右边距
        )
    ]),
    html.Div([
        html.H4('市場'),
        dcc.Checklist(
            options=[
                {'label': '台北一', 'value': '台北一'},
                {'label': '台北二', 'value': '台北二'}
            ],
            value=[],  # 默认不选中任何选项
            id='markets-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字体加大并增加右边距
        )
    ]),
    html.Div([
        html.H4('圖'),
        dcc.Checklist(
            options=[
                {'label': '常態分析圖', 'value': '常態分析圖'},
                {'label': '盒鬚圖', 'value': '盒鬚圖'}
            ],
            value=[],  # 默认不选中任何选项
            id='charts-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字体加大并增加右边距
        )
    ]),
    html.Button('執行', id='execute-button', n_clicks=0),  # 添加执行按钮
    html.Div(id='display-selected-values')
])

@callback(
    Output('display-selected-values', 'children'),
    Input('execute-button', 'n_clicks'),  # 使用按钮的点击次数作为输入
    State('mango-types-checklist', 'value'),
    State('markets-checklist', 'value'),
    State('charts-checklist', 'value')
)
def update_output(n_clicks, selected_mango_types, selected_markets, selected_charts):
    if n_clicks == 0:
        return ""
    selected_values = selected_mango_types + selected_markets + selected_charts
    return html.Div([html.P(f'Selected: {", ".join(selected_values)}')])

# 嵌入第二个 Dash 应用 (全球表单)
app1 = Dash(__name__, server=app, url_base_pathname='/dashboard/app1/')

# 原始全球表单数据
df_original = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# 新的全球表单数据
df_new = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app1.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
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
    dcc.Slider(
        min=df_original['Year'].min(),
        max=df_original['Year'].max(),
        step=None,
        id='year--slider',
        value=df_original['Year'].max(),
        marks={str(year): str(year) for year in df_original['Year'].unique()}
    )
])

@app1.callback(
    [Output('xaxis-column', 'options'),
     Output('yaxis-column', 'options'),
     Output('indicator-graphic', 'figure'),
     Output('indicator-graphic', 'style')],
    [Input('execute-button', 'n_clicks'),
     Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')],
    [State('mango-types-checklist', 'value'),
     State('markets-checklist', 'value')]
)
def update_graph(n_clicks, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value, selected_mango_types, selected_markets):
    if '芒果愛文' in selected_mango_types and '台北一' in selected_markets:
        dff = df_new
        x_options = [{'label': col, 'value': col} for col in dff.columns]
        y_options = [{'label': col, 'value': col} for col in dff.columns]
        if not xaxis_column_name or not yaxis_column_name:
            return x_options, y_options, {}, {'display': 'none'}
        
        fig = px.scatter(dff, x=xaxis_column_name, y=yaxis_column_name)
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
        fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
        fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
        
        return x_options, y_options, fig, {'display': 'block'}
    else:
        dff = df_original[df_original['Year'] == year_value]
        x_options = [{'label': col, 'value': col} for col in dff['Indicator Name'].unique()]
        y_options = [{'label': col, 'value': col} for col in dff['Indicator Name'].unique()]
        if not xaxis_column_name or not yaxis_column_name:
            return x_options, y_options, {}, {'display': 'none'}
        
        xValue = dff[dff['Indicator Name'] == xaxis_column_name]['Value']
        yValue = dff[dff['Indicator Name'] == yaxis_column_name]['Value']
        hoverValue = dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
        fig = px.scatter(x=xValue, y=yValue, hover_name=hoverValue)
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
        fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
        fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
        
        return x_options, y_options, fig, {'display': 'block'}

@app.route("/")
def index():
    selected_area = request.args.get('area')
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '士林區' if selected_area is None else selected_area
    detail_snaes = data.get_snaOfArea(area=selected_area)
    
    return render_template('index.html.jinja', areas=areas, show_area=selected_area, detail_snaes=detail_snaes)

# 使用 DispatcherMiddleware 将 Flask 和两个 Dash 应用合并
application = DispatcherMiddleware(app, {
    '/dash': dash_app.server,
    '/dashboard/app1': app1.server
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application, use_reloader=True, use_debugger=True)
