# img_i.py

import base64
import os

def encode_image(image_path):
    """
    將圖片檔案轉換為 Base64 編碼的字符串。

    :param image_path: 圖片檔案的路徑
    :return: 圖片的 Base64 編碼字符串
    """
    try:
        with open(image_path, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_img}"
    except Exception as e:
        print(f"轉換圖片為 Base64 編碼時發生錯誤：{e}")
        return None

def display_mango_images(location):
    """
    根據位置返回對應的圖片 Base64 編碼列表。

    :param location: 位置名稱
    :return: 圖片 Base64 編碼字符串列表
    """
    if location == "台北一":
        image_paths = [
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\box_dis_1.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\acf_pacf_plot_1.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\residuals_qq_plot_1.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\sarima_model_analysis_1.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\train_test_plot_1.png"
        ]
    elif location == "台北二":
        image_paths = [
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\box_dis_2.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\acf_pacf_plot_2.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\residuals_qq_plot_2.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\sarima_model_analysis_2.png",
            "C:\\Users\\win\\Documents\\vicky_window\\2024-M-3\\analy_irwin_imgs\\train_test_plot_2.png"
        ]
    else:
        image_paths = []

    # 將圖片路徑轉換為 Base64 編碼字符串
    image_base64_list = [encode_image(path) for path in image_paths if os.path.isfile(path)]
    
    return image_base64_list
