#02.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

import matplotlib
import warnings
import matplotlib.pyplot as plt
import matplotlib

# 設定字型為 SimHei 或 Noto Sans CJK
matplotlib.rcParams['font.family'] = 'SimHei'
# matplotlib.rcParams['font.family'] = 'Noto Sans CJK'

# 測試圖形
plt.figure(figsize=(12, 6))
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('測試標題')
plt.xlabel('時間')
plt.ylabel('數值')
plt.show()


#SARIMA模型的時間序列分析與預測數據
def train_and_predict_sarima(train, test, output_dir):
    """
    使用SARIMA模型進行時間序列預測，並評估模型表現。

    參數:
    train (pd.Series): 訓練資料集。
    test (pd.Series): 測試資料集。
    output_dir (str): 儲存模型結果圖表的目錄路徑。
    """
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # 建立和訓練SARIMA模型
    # 設置季節性順序為(1, 1, 1, 180)，因為季節性是每年6個月（4到9月）
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 180))
    model_fit = model.fit(method='lbfgs', maxiter=200, disp=False)

    # 預測訓練集和測試集
    y_pred_train = model_fit.predict(start=train.index[0], end=train.index[-1], dynamic=False)
    y_pred_test = model_fit.predict(start=test.index[0], end=test.index[-1], dynamic=False)

    # 計算評估指標
    mse_train = mean_squared_error(train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(train, y_pred_train)

    mse_test = mean_squared_error(test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(test, y_pred_test)

    # 四捨五入到小數點後四位
    mse_train_rounded = round(mse_train, 4)
    rmse_train_rounded = round(rmse_train, 4)
    mae_train_rounded = round(mae_train, 4)

    mse_test_rounded = round(mse_test, 4)
    rmse_test_rounded = round(rmse_test, 4)
    mae_test_rounded = round(mae_test, 4)

    # 記錄評估指標
    Training_MSE = f"Training MSE: {mse_train_rounded}"
    Training_RMSE = f"Training RMSE: {rmse_train_rounded}"
    Training_MAE = f"Training MAE: {mae_train_rounded}"
    Testing_MSE = f"Testing MSE: {mse_test_rounded}"
    Testing_RMSE = f"Testing RMSE: {rmse_test_rounded}"
    Testing_MAE = f"Testing MAE: {mae_test_rounded}"

    # 輸出評估指標
    print(Training_MSE)
    print(Training_RMSE)
    print(Training_MAE)
    print(Testing_MSE)
    print(Testing_RMSE)
    print(Testing_MAE)

    # SARIMA模型結果視覺化
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label='Training data')  # 繪製訓練資料
    plt.plot(test.index, test, label='Testing data')    # 繪製測試資料
    plt.plot(train.index, y_pred_train, color='red', linestyle='--', label='Training prediction')  # 繪製訓練預測
    plt.plot(test.index, y_pred_test, color='green', linestyle='--', label='Testing prediction')   # 繪製測試預測
    plt.xlabel('Time')  # 設置x軸標籤
    plt.ylabel('Average Price (元/公斤)')  # 設置y軸標籤
    plt.title('SARIMA Model Time Series Analysis and Forecast')  # 設置圖表標題
    plt.legend()

    # 儲存圖表
    sarima_model_plot = os.path.join(output_dir, 'sarima_model_analysis_1.png')
    plt.savefig(sarima_model_plot)
    plt.close()
print(train.dtypes)
print(test.dtypes)