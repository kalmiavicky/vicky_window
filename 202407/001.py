from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    '芒果品種': ['芒果愛文', '芒果金煌'],
    '市場': ['台北一', '台北二'],
    '圖': ['常態分析圖', '盒鬚圖'],
}

app.layout = html.Div([
    dcc.Checklist(
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value=['芒果品種'],
        id='countries-radio',
        inline=True  # 使选项水平显示
    ),
    html.Hr(),
    dcc.Checklist(id='cities-radio', inline=True),  # 使选项水平显示
    html.Div(id='display-selected-values')
])

@callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value')
)
def set_cities_options(selected_country):
    # 检查 selected_country 是否为空列表或包含多个值
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

@callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value')
)
def set_display_children(selected_country, selected_city):
    if selected_country and selected_city:
        return f'{selected_city[0]}城市位於{selected_country[0]}'
    return '請選擇一個選項'

if __name__ == '__main__':
    app.run(debug=True)
