#匯入模組：
#匯入 tkinter 相關模組以及自定義的 data 模組和 tkintermapview 模組。
from tkinter.simpledialog import Dialog
from tkinter import ttk
from tkinter import Misc
import tkinter as tk
from data import Info
import tkintermapview as tkmap

#CustomMessagebox 類別：繼承自 tkinter.simpledialog.Dialog，用於創建自定義訊息框。/初始化方法中設置站點資訊並調用父類別的初始化方法。
class CustomMessagebox(Dialog):
    # 自定義訊息框，繼承自 tkinter 的 Dialog 類
    def __init__(self, parent: Misc, title: str, site: Info):
        self.site: Info = site
        # 初始化父類別 Dialog
        super().__init__(parent=parent, title=title)
     
    #body 方法： 創建對話框的主體，包括包含框架和地圖框架/使用 tkintermapview.TkinterMapView 創建地圖小工具，設置標記和路徑，並設置地圖縮放級別
    def body(self, master):
        # 創建對話框主體。返回應具有初始焦點的控件。
        contain_frame = ttk.Frame(master)
        
        # 創建地圖框架
        map_frame = ttk.Frame(contain_frame)
        # 創建地圖小工具，設置寬度、高度和圓角半徑
        map_widget = tkmap.TkinterMapView(map_frame,
                                          width=800,
                                          height=600,
                                          corner_radius=0)
        map_widget.pack()
        
        # 設置地圖上的標記位置
        marker = map_widget.set_position(self.site.lat, self.site.lng, marker=True) #加上定位標置
        # 設置標記的文本內容
        marker.set_text(f'{self.site.sarea}\n{self.site.sna}\n總車輛:{self.site.total}\n可借:{self.site.rent_bikes}\n可還:{self.site.retuen_bikes}') 
        
        # 畫路徑用於表示位置範圍
        start_point = self.site.lat + 0.0005, self.site.lng + 0.0005   #畫線以這點為基礎
        end_point = start_point[0], start_point[1] - 0.001
        down_point = end_point[0] - 0.001, end_point[1]
        left_point = down_point[0], down_point[1] + 0.001
        up_point = left_point[0] + 0.001, left_point[1]
        path = map_widget.set_path([start_point, end_point, down_point, left_point, up_point])
        
        # 設置地圖縮放級別
        map_widget.set_zoom(20) #設定顯示大小
        map_frame.pack(expand=True, fill='both')
        
        # 包含框架設置
        contain_frame.pack(expand=True, fill='both', pady=10, padx=30)

    #apply 方法：
    def apply(self):
        # 當用戶按下確定時處理數據（此處為空，根據需要實現）
        pass

    #buttonbox 方法：
    def buttonbox(self):
        # 添加自定義按鈕（覆蓋默認的按鈕框）
        box = ttk.Frame(self)
        # 創建確定按鈕，並設置命令為調用 self.ok 方法
        self.ok_button = tk.Button(box, text="確定", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def ok(self):
        # 覆蓋 ok 方法，調用父類別的 ok 方法
        super().ok()




