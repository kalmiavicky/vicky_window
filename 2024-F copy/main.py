from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.boxplot import boxplot_app
import pandas as pd
import plotly
import plotly.express as px
import json
import data

app = Flask(__name__)

# 讀取 CSV 文件
csv_path = r'C:\Users\user\Documents\vicky_window\2024-F copy\mangodata\MangoIrwin-2.csv'
df = pd.read_csv(csv_path)

area_mapping = {
    '芒果愛文 台北一': '士林區',
    '芒果愛文 台北二': '臺大公館校區',
    '芒果金煌 台北一': '芒果金煌 台北一',
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
        if area in ['常態分析圖', '盒鬚圖']:
            return redirect(area_mapping[area])
    
    detail_snaes = []
    for area in selected_areas:
        mapped_area = area_mapping.get(area, area)
        if not mapped_area.startswith('/'):
            detail_snaes.extend(data.get_snaOfArea(area=mapped_area))
    
    return render_template('index.html', areas=areas, selected_areas=selected_areas, detail_snaes=detail_snaes)

@app.route("/mango_jinhuang_data")
def mango_jinhuang_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_df = df
    if start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    price_fig = px.line(filtered_df, x='date', y='price', title='價格趨勢')
    volume_fig = px.bar(filtered_df, x='date', y='volume', title='交易量趨勢')
    
    return jsonify({
        'price_chart': json.loads(json.dumps(price_fig, cls=plotly.utils.PlotlyJSONEncoder)),
        'volume_chart': json.loads(json.dumps(volume_fig, cls=plotly.utils.PlotlyJSONEncoder))
    })

# 將所有Dash應用整合到Flask應用中
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/dashboard/app1': app1.server,
    '/dashboard/boxplot': boxplot_app.server
})

if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)