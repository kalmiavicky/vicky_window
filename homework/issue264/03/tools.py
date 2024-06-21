from tkinter.simpledialog import Dialog
from tkinter import ttk
from tkinter import Misc
import tkinter as tk
import tkintermapview as tkmap

# 自定義訊息框類別：顯示選擇的餐廳詳細資訊
class CustomMessagebox(Dialog):
    def __init__(self, parent: Misc, title: str, place: dict):
        self.place = place
        super().__init__(parent=parent, title=title)

    # 對話框主體：顯示地圖和餐廳資訊
    def body(self, master):
        contain_frame = ttk.Frame(master)
        
        map_frame = ttk.Frame(contain_frame)
        map_widget = tkmap.TkinterMapView(map_frame, width=800, height=600, corner_radius=0)
        map_widget.pack()
        
        location = self.place['geometry']['location']
        marker = map_widget.set_position(location['lat'], location['lng'], marker=True)
        marker.set_text(f"{self.place['name']}\n{self.place['formatted_address']}\n評分:{self.place.get('rating', 'N/A')}\n評價數:{self.place.get('user_ratings_total', 'N/A')}")
        
        map_widget.set_zoom(18)
        map_frame.pack(expand=True, fill='both')
        contain_frame.pack(expand=True, fill='both', pady=10, padx=30)

    def apply(self):
        pass

    # 自定義按鈕框：添加確認按鈕
    def buttonbox(self):
        box = ttk.Frame(self)
        self.ok_button = tk.Button(box, text="確定", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def ok(self):
        super().ok()
