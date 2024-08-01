import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np

# 創建 Dash 應用
app = dash.Dash(__name__)

# 創建範例 DataFrame
data = {
    '平均價(元/公斤)': [10, 12, 15, 20, 22, 30, 45, 50, 60, 70]
}
df = pd.DataFrame(data)

# 計算四分位距 (IQR) 和邊界的函數
def process_average_price(dataframe):
    """
    處理平均價格數據，計算四分位距 (IQR) 和邊界
    
    參數：
    dataframe: pd.DataFrame，包含數據的 DataFrame
    
    回傳：
    pd.DataFrame，包含 IQR 和邊界數據的 DataFrame
    """
    if dataframe.empty or '平均價(元/公斤)' not in dataframe.columns:
        return None
    
    Q1 = dataframe['平均價(元/公斤)'].quantile(0.25)
    Q3 = dataframe['平均價(元/公斤)'].quantile(0.75)
    IQR = Q3 - Q1
    Upper = Q3 + 1.5 * IQR
    Lower = Q1 - 1.5 * IQR
    
    # 創建結果 DataFrame
    result_df = pd.DataFrame({
        '指標': ['四分位距 (IQR)', '上邊界 (天花板)', '下邊界 (地板)'],
        '值': [IQR, Upper, Lower]
    })
    
    return result_df

# 定義應用佈局
app.layout = html.Div([
    html.H1("四分位距計算結果"),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # 每分鐘觸發一次回調
        n_intervals=0
    ),
    html.Div(id='table-container')
])

# 定義回調函數
@app.callback(
    Output('table-container', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_table(n_intervals):
    """
    回調函數，根據數據更新表格
    
    參數：
    n_intervals: int，間隔計數器
    
    回傳：
    html.Div，包含表格或錯誤信息的內容
    """
    interquartile_range_data = process_average_price(df)
    if interquartile_range_data is not None:
        interquartile_range_table = dash_table.DataTable(
            data=interquartile_range_data.to_dict('records'),
            columns=[{"name": i, "id": i} for i in interquartile_range_data.columns],
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'}
        )
        return interquartile_range_table
    else:
        return html.P("無法處理平均價資料", style={'textAlign': 'center', 'color': 'red'})

# 運行應用
if __name__ == '__main__':
    app.run_server(debug=True)
