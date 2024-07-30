# main.py
from flask import Flask, render_template, request, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.boxplot import boxplot_app  # 導入新的盒鬚圖 Dash 應用
import data

app = Flask(__name__)

# 區域名稱映射
area_mapping = {
    '芒果愛文 台北一': '士林區',
    '芒果愛文 台北二': '臺大公館校區',
    '芒果金煌 台北一': '大安區',
    '芒果金煌 台北二': '文山區',
    '常態分析圖': '/dashboard/app1/',
    '盒鬚圖': '/dashboard/boxplot/'  # 添加盒鬚圖的映射
}

@app.route("/")
def index():
    # 從請求中獲取選擇的區域列表
    selected_areas = request.args.getlist('area')
    # 定義所有可選的區域
    areas = ['芒果愛文 台北一', '芒果愛文 台北二', '芒果金煌 台北一', '芒果金煌 台北二', '常態分析圖', '盒鬚圖']
    
    # 如果選擇了 '常態分析圖' 或 '盒鬚圖'，則重定向到相應的 Dash 應用
    if '常態分析圖' in selected_areas:
        return redirect('/dashboard/app1/')
    elif '盒鬚圖' in selected_areas:
        return redirect('/dashboard/boxplot/')
    
    detail_snaes = []
    # 根據選擇的區域獲取對應的數據
    for area in selected_areas:
        mapped_area = area_mapping.get(area, area)
        detail_snaes.extend(data.get_snaOfArea(area=mapped_area))
    
    # 渲染模板，並傳遞區域列表、選擇的區域和詳細數據
    return render_template('index.html.jinja', areas=areas, selected_areas=selected_areas, detail_snaes=detail_snaes)

# 將 Dash 應用集成到 Flask 應用中
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/dashboard/app1': app1.server,
    '/dashboard/boxplot': boxplot_app.server  # 添加盒鬚圖 Dash 應用
})

if __name__ == "__main__":
    # 啟動 Flask 應用
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)