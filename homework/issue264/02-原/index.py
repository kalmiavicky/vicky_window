#匯入模組和類別：匯入 ttkthemes、tkinter 相關模組以及自定義的 data、tools 模組。
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import data
from data import FilterData, Info
from tools import CustomMessagebox

#Window 類別的初始化：嘗試從 data 模組中載入資料，若發生異常則顯示警告訊息。
class Window(ThemedTk):
    def __init__(self, theme: str = 'arc', **kwargs):
        # 初始化父類別 ThemedTk，設定主題
        super().__init__(theme=theme, **kwargs)
        self.title('台北市YouBike2.0及時資料') #設定主視窗的標題為 "台北市YouBike2.0及時資料"。
        try:
            # 嘗試載入資料
            self.__data = data.load_data()
        except Exception as e:
            # 如果發生異常，顯示警告訊息
            messagebox.showwarning(title='警告', message=str(e))
        
        # 呼叫介面顯示方法
        self._display_interface()
        
    @property
    def data(self) -> list[dict]:
        # 定義一個只讀屬性來獲取資料
        return self.__data

    #_display_interface 方法：

    def _display_interface(self):
        # 建立主框架並設置邊框樣式
        mainFrame = ttk.Frame(borderwidth=1, relief='groove')
        # 添加標題標籤
        ttk.Label(mainFrame, text="台北市YouBike2.0及時資料", font=('arial', 25)).pack(pady=(20, 10))
        
        # 建立表格框架
        tableFrame = ttk.Frame(mainFrame)
        # 定義表格的欄位
        columns = ('sna', 'sarea', 'mday', 'ar', 'total', 'rent_bikes', 'retuen_bikes')
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings', selectmode='browse')  #Treeview 小工具 將資料添加到 Treeview，並設置滾動條。
        
        # 定義表頭
        tree.heading('sna', text='站點')
        tree.heading('sarea', text='行政區')
        tree.heading('mday', text='時間')
        tree.heading('ar', text='地址')
        tree.heading('total', text='總數')
        tree.heading('rent_bikes', text='可借')
        tree.heading('retuen_bikes', text='可還')

        # 定義欄位寬度
        tree.column('sarea', width=70, anchor=tk.CENTER)
        tree.column('mday', width=120, anchor=tk.CENTER)
        tree.column('ar', minwidth=100)
        tree.column('total', width=50, anchor=tk.CENTER)
        tree.column('rent_bikes', width=50, anchor=tk.CENTER)
        tree.column('retuen_bikes', width=50, anchor=tk.CENTER)

        # 綁定使用者選擇事件
        tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # 將數據添加到 Treeview
        for site in self.data:
            tree.insert('', tk.END,
                        values=(site['sna'], site['sarea'], site['mday'], site['ar'], site['total'], site['rent_bikes'], site['retuen_bikes']))
        
        # 設置 Treeview 的布局
        tree.grid(row=0, column=0, sticky='nsew')

        # 添加垂直滾動條
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # 將表格框架放置到主框架中
        tableFrame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # 將主框架放置到主視窗中
        mainFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    #item_selected 方法： 
    def item_selected(self, event):
        # 當使用者選擇某項時觸發此方法
        tree = event.widget
        print(isinstance(tree, ttk.Treeview))  # 確認事件的來源是 Treeview
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record: list = item['values']
            site_data: Info = FilterData.get_selected_coordinate(sna=record[0], data=self.data)
            # 顯示自定義訊息框
            CustomMessagebox(self, title=site_data.sna, site=site_data)
#主函數：
def main():
    # 創建 Window 類別的實例並啟動主事件循環
    window = Window(theme='breeze')
    window.mainloop()

if __name__ == '__main__':
    main()
