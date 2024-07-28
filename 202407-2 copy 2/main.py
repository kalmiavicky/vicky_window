from flask import Flask, render_template, request
import data
from dash import Dash, dcc, html, Input, Output, State, callback
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

# 嵌入 Dash 應用
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

dash_app.layout = html.Div([
    html.Div([
        html.H4('芒果品種/市場'),
        dcc.Checklist(
            options=[
                {'label': '芒果愛文 台北一', 'value': '芒果愛文 台北一'},
                {'label': '芒果愛文 台北二', 'value': '芒果愛文 台北二'},
                {'label': '芒果金煌 台北一', 'value': '芒果金煌 台北一'},
                {'label': '芒果金煌 台北二', 'value': '芒果金煌 台北二'}
            ],
            value=[],
            id='mango-types-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}
        )
    ]),
    html.Button('執行', id='submit-button', n_clicks=0),
    html.Div(id='display-selected-values')
])

@callback(
    Output('display-selected-values', 'children'),
    Input('submit-button', 'n_clicks'),
    State('mango-types-checklist', 'value')
)
def update_output(n_clicks, selected_mango_types):
    if n_clicks == 0:
        return ""
    if '芒果愛文 台北一' in selected_mango_types:
        return html.Iframe(src='/dashboard/app1/', width='100%', height='600', style={'border': 'none'})
    else:
        return html.P("請選擇 '芒果愛文 台北一' 來顯示資料")

# 嵌入第二个 Dash 应用 (全球表单)
app1 = Dash(__name__, server=app, url_base_pathname='/dashboard/app1/')

app1.layout = html.Div([
    html.H3("請選擇 '芒果愛文 台北一' 顯示資料")
])

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
