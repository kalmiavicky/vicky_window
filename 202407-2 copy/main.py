from flask import Flask, render_template, request
import data
from dash import Dash, dcc, html, Input, Output, callback

app = Flask(__name__)


# 嵌入 Dash 应用
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

all_options = {
    '芒果品種': ['芒果愛文', '芒果金煌'],
    '市場': ['台北一', '台北二'],
    '圖': ['常態分析圖', '盒鬚圖'],
}

dash_app.layout = html.Div([
    dcc.Checklist(
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value=['芒果品種'],
        id='countries-radio',
        # inline=True,  # 使选项水平显示
        labelStyle={'font-size': '20px', 'margin-right': '20px'}  # 字体加大并增加右边距
    ),
    html.Hr(),
    dcc.Checklist(id='cities-radio', inline=True, labelStyle={'font-size': '20px', 'margin-right': '20px'}),  # 字体加大并增加右边距
    html.Div(id='display-selected-values')
])

@callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value')
)
def set_cities_options(selected_country):
    if not selected_country or len(selected_country) != 1:
        return []
    selected_country = selected_country[0]
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options')
)
def set_cities_value(available_options):
    if available_options:
        return [available_options[0]['value']]
    return []



@app.route("/")
def index():
    selected_area = request.args.get('area')
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '士林區' if selected_area is None else selected_area
    detail_snaes = data.get_snaOfArea(area=selected_area)
    
    return render_template('index.html.jinja', areas=areas, show_area=selected_area, detail_snaes=detail_snaes)

if __name__ == '__main__':
    app.run(debug=True)
