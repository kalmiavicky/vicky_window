# main.py
from flask import Flask, render_template, request, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.boxplot import boxplot_app
from dashboard.mango_jinhuang import mango_jinhuang_app
import data

app = Flask(__name__)

area_mapping = {
    '芒果愛文 台北一': '士林區',
    '芒果愛文 台北二': '臺大公館校區',
    '芒果金煌 台北一': '/dashboard/mango-jinhuang/',
    '芒果金煌 台北二': '文山區',
    '常態分析圖': '/dashboard/app1/',
    '盒鬚圖': '/dashboard/boxplot/'
}

@app.route("/")
def index():
    selected_areas = request.args.getlist('area')
    areas = ['芒果愛文 台北一', '芒果愛文 台北二', '芒果金煌 台北一', '芒果金煌 台北二', '常態分析圖', '盒鬚圖']
    
    # 檢查是否選擇了特定的分析頁面
    for area in selected_areas:
        if area in ['常態分析圖', '盒鬚圖', '芒果金煌 台北一']:
            return redirect(area_mapping[area])
    
    detail_snaes = []
    for area in selected_areas:
        mapped_area = area_mapping.get(area, area)
        if mapped_area.startswith('/'):
            continue  # 跳過需要重定向的選項
        detail_snaes.extend(data.get_snaOfArea(area=mapped_area))
    
    return render_template('index.html.jinja', areas=areas, selected_areas=selected_areas, detail_snaes=detail_snaes)

# 將所有Dash應用整合到Flask應用中
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/dashboard/app1': app1.server,
    '/dashboard/boxplot': boxplot_app.server,
    '/dashboard/mango-jinhuang': mango_jinhuang_app.server
})

if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)