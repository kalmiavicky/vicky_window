from flask import Flask, render_template, request, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.boxplot import boxplot_app
import data
import pandas as pd

app = Flask(__name__)

area_mapping = {
    '芒果愛文 台北一': '士林區',
    '芒果愛文 台北二': '臺大公館校區',
    '芒果金煌 台北一': '大安區',
    '芒果金煌 台北二': '文山區',
    '常態分析圖': '/dashboard/app1/',
    '盒鬚圖': '/dashboard/boxplot/'
}

@app.route("/")
def index():
    selected_areas = request.args.getlist('area')
    areas = ['芒果愛文 台北一', '芒果愛文 台北二', '芒果金煌 台北一', '芒果金煌 台北二', '常態分析圖', '盒鬚圖']
    
    if '常態分析圖' in selected_areas:
        return redirect('/dashboard/app1/')
    elif '盒鬚圖' in selected_areas:
        return redirect('/dashboard/boxplot/')
    
    detail_snaes = []
    for area in selected_areas:
        mapped_area = area_mapping.get(area, area)
        if area == '芒果金煌 台北一':
            # 使用新的 CSV 文件
            df = pd.read_csv('芒果金煌北一.csv')
            detail_snaes.extend(df.to_dict('records'))
        else:
            detail_snaes.extend(data.get_snaOfArea(area=mapped_area))
    
    return render_template('index.html.jinja', areas=areas, selected_areas=selected_areas, detail_snaes=detail_snaes)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/dashboard/app1': app1.server,
    '/dashboard/boxplot': boxplot_app.server
})

if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)