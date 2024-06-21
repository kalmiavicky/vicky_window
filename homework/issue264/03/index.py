from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import googlemaps
from tools import CustomMessagebox

API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'  # 請替換為您的Google Maps API Key

# Window 類別的初始化：初始化主視窗，設定標題和Google Maps客戶端
class Window(ThemedTk):
    def __init__(self, theme: str = 'arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title('Google地圖美食搜尋')  # 修改標題
        self.gmaps = googlemaps.Client(key=API_KEY)  # 初始化Google Maps客戶端
        
        self._display_interface()  # 呼叫介面顯示方法
        
    # 介面顯示方法：建立搜尋框、結果表格等UI元件
    def _display_interface(self):
        mainFrame = ttk.Frame(borderwidth=1, relief='groove')
        ttk.Label(mainFrame, text="Google地圖美食搜尋", font=('arial', 25)).pack(pady=(20, 10))
        
        searchFrame = ttk.Frame(mainFrame)
        searchLabel = ttk.Label(searchFrame, text="搜尋地點：")
        searchLabel.pack(side=tk.LEFT, padx=(0, 5))
        self.searchVar = tk.StringVar()
        searchEntry = ttk.Entry(searchFrame, textvariable=self.searchVar)
        searchEntry.pack(side=tk.LEFT, padx=(0, 5))
        searchButton = ttk.Button(searchFrame, text="搜尋", command=self.search)
        searchButton.pack(side=tk.LEFT)
        searchFrame.pack(pady=(0, 20))

        tableFrame = ttk.Frame(mainFrame)
        columns = ('name', 'address', 'rating', 'user_ratings_total')
        self.tree = ttk.Treeview(tableFrame, columns=columns, show='headings', selectmode='browse')
        
        # 設定表頭
        self.tree.heading('name', text='餐廳名稱')
        self.tree.heading('address', text='地址')
        self.tree.heading('rating', text='評分')
        self.tree.heading('user_ratings_total', text='評價數')

        # 設定欄位寬度
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('address', minwidth=200)
        self.tree.column('rating', width=50, anchor=tk.CENTER)
        self.tree.column('user_ratings_total', width=70, anchor=tk.CENTER)

        # 綁定使用者選擇事件
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # 將表格顯示到界面上
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        tableFrame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        mainFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # 將資料載入到表格中
    def load_data_to_tree(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for place in data:
            self.tree.insert('', tk.END, values=(place['name'], place['formatted_address'], place.get('rating', 'N/A'), place.get('user_ratings_total', 'N/A')))

    # 搜尋方法：使用Google Maps API進行搜尋
    def search(self):
        keyword = self.searchVar.get().strip()
        if keyword:
            places = self.gmaps.places_nearby(location=(25.0330, 121.5654), keyword=keyword, radius=2000, type='restaurant')['results']
            self.load_data_to_tree(places)
        else:
            messagebox.showwarning('警告', '請輸入搜尋地點')

    # 使用者選擇事件處理
    def item_selected(self, event):
        tree = event.widget
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            name = record[0]
            place = next((place for place in self.places if place['name'] == name), None)
            if place:
                CustomMessagebox(self, title=place['name'], place=place)

# 主函數：創建並運行主視窗
def main():
    window = Window(theme='breeze')
    window.mainloop()

if __name__ == '__main__':
    main()
