from flask import Flask, render_template, request
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import data  # 引入 data 模組

app = Flask(__name__)

# 嵌入 Dash 應用
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

# 設置 Dash 應用的佈局
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
            value=[],  # 預設不選中任何選項
            id='mango-types-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字體加大並增加右邊距
        )
    ]),
    html.Div([
        html.H4('圖'),
        dcc.Checklist(
            options=[
                {'label': '常態分析圖', 'value': '常態分析圖'},
                {'label': '盒鬚圖', 'value': '盒鬚圖'}
            ],
            value=[],  # 預設不選中任何選項
            id='charts-checklist',
            labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字體加大並增加右邊距
        )
    ]),
    html.Button('執行', id='submit-button', n_clicks=0),  # 添加執行按鈕
    html.Div(id='display-selected-values')  # 顯示選中項目的容器
])

@app.route("/")
def index():
    selected_area = request.args.get('area')
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '未選擇任何資料' if selected_area is None else selected_area
    detail_snaes = data.get_snaOfArea(selected_area) if selected_area != '未選擇任何資料' else []

    return render_template('index.html.jinja', areas=areas, show_area=selected_area, detail_snaes=detail_snaes)

@dash_app.callback(
    Output('display-selected-values', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('mango-types-checklist', 'value')
)
def update_output(n_clicks, mango_types):
    if n_clicks > 0 and '芒果愛文 台北一' in mango_types:
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
        data = df.head().to_dict('records')
        table = html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(data[i][col]) for col in df.columns
                ]) for i in range(len(data))
            ])
        ])
        return table
    return html.P('未選擇任何資料')

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

application = DispatcherMiddleware(app, {
    '/dash': dash_app.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application, use_reloader=True, use_debugger=True)
