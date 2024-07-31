from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# 创建 Dash 应用
dash_app = Dash(__name__)

# 加载数据
df = pd.read_csv('2024-F copy\ME1.csv')

   # 這裡可以添加數據處理和圖表生成的邏輯
    figure = {
        'data': [{'x': df['日期'], 'y': df['價格'], 'type': 'line'}],
        'layout': {'title': '芒果價格趨勢'}
    }
# 设置布局
dash_app.layout = html.Div(
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
)

if __name__ == "__main__":
    # 启动应用，指定不同的端口
    dash_app.run_server(debug=True, port=8052)



server = Flask(__name__)
app = dash.Dash(__name__, server=server)
