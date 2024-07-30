# dashboard/boxplot.py
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# 創建 Dash 應用
boxplot_app = Dash(__name__, requests_pathname_prefix='/dashboard/boxplot/')

# 加載數據
df = pd.read_csv('https://plotly.github.io/datasets/gapminderDataFiveYear.csv')

# 創建圖形
fig = px.scatter(df,
                 x="gdpPercap",
                 y="lifeExp",
                 color="continent",
                 size="pop",
                 log_x=True,
                 size_max=60)

# 設置布局
boxplot_app.layout = html.Div([
    html.H1("全球 GDP 與壽命關係圖", style={'text-align': 'center'}),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])