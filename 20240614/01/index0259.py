from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import data
from data import FilterData,Info




class Window(ThemedTk):
    def __init__(self,theme:str='arc',**kwargs):  #-1-theme--#1-呼叫隱數(引數值呼叫)/建立參數 - default value
        super().__init__(theme=theme,**kwargs)    #-0-theme 傳回上面
        self.title('台北市YouBike2.0及時資料')
        try:
            self.__data = data.load_data()       #呼叫DATA檔執行一次 #data 變數 #實體-attribute(可讀寫)/property（唯謮）/method
               
        except Exception as e:
            messagebox.showwarning(title='警告',message=str(e)) #呼叫DATA檔-如果網址錯誤出現警告
        
        self._display_interface()    #-1-呼叫  _display_interface 

    @property
    def data(self)->list[dict]:
        return self.__data
            
    def _display_interface(self):     #-0-呼叫  _display_interface  
         
        mainFrame = ttk.Frame(borderwidth=1,relief='groove')  # mainFrame = ttk.Frame(width=500,height=800) #視窗的長高 （沒有內容才有用）
        ttk.Label(mainFrame,text="台北市YouBike2.0及時資料",font=('arial',25)).pack(pady=(20,10))   #-1-ttk.Label放在mainFrame
        #=================================
        tableFrame = ttk.Frame(mainFrame)   #-0-tableFrame放在 mainFrame
        columns = ('sna', 'sarea', 'mday','ar','total','rent_bikes','retuen_bikes')
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings',selectmode='browse') #selectmode='browse' 單選
        # define headings # 定義表頭
        tree.heading('sna', text='站點')
        tree.heading('sarea', text='行政區')
        tree.heading('mday', text='時間')
        tree.heading('ar', text='地址')
        tree.heading('total', text='總數')
        tree.heading('rent_bikes', text='可借')
        tree.heading('retuen_bikes', text='可還')

        #定義欄位寬度
        tree.column("sna",width=300)
        tree.column("sarea",width=70,anchor=tk.CENTER)
        tree.column("mday",width=180,anchor=tk.CENTER)
        tree.column("ar",width=300)
        tree.column("total",width=50,anchor=tk.CENTER)
        tree.column("rent_bikes",width=50,anchor=tk.CENTER)
        tree.column("retuen_bikes",width=50,anchor=tk.CENTER)

        #bind使用者事件
        tree.bind('<<TreeviewSelect>>', self.item_selected)



        
        # add data to the treeview
        for site in self.data:
            tree.insert('', tk.END,
                        values=(site['sna'],site['sarea'],site['mday'],site['ar'],site['total'],site['rent_bikes'],site['retuen_bikes']))
        
        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tableFrame.pack(expand=True,fill=tk.BOTH,padx=20,pady=20)
        #======================================
        mainFrame.pack(expand=True,fill=tk.BOTH,padx=10,pady=10)

    def item_selected(self,event):  #點資料會回傳 （上面的self可以抓到這裡的self）
        tree=event.widget   #event事件
        print(isinstance(tree,ttk.Treeview))
        for selected_item in tree.selection():  #elected_item所選項目
            item = tree.item(selected_item)
            record = item['values']
            site_data:Info = FilterData.get_selected_coordinate(sna=record[0],data=self.data)               #record記錄[1]欄位第二欄點資料會回傳
            # print(tree.selection())                #點資料會回傳
            print(site_data)
            # print(b)






def main():
    window = Window(theme='breeze') #呼叫Window #breeze（ThemedTk視窗顏色)
    window.mainloop()

if __name__ == '__main__':
    main()