from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# 创建 Dash 应用
dash_app = Dash(__name__)

# 加载数据
df = pd.read_csv('https://plotly.github.io/datasets/gapminderDataFiveYear.csv')

# 创建图形
fig = px.scatter(df,
                  x="gdpPercap",
                  y="lifeExp",
                  color="continent",
                  size="pop",
                  log_x=True,
                  size_max=60)

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
