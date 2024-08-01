import os

csv_path = r'C:\Users\win\Documents\vicky_window\2024-F copy\mangodata\MangoIrwin-2.csv'
if not os.path.exists(csv_path):
    print(f"檔案 {csv_path} 不存在。")
else:
    print(f"檔案 {csv_path} 存在。")