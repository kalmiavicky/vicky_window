
import tkinter as tk
from tkinter import ttk


def get_names() -> list[str]:
    with open('names.txt',encoding='utf-8') as file:
        content:str = file.read()      #回傳字串
    names:list[str] = content.split()  #算出有幾個名字 
    return names
# names:list[str]=get_names()   #文件變數 所以和上面不會起充突

class Window(tk.Tk):
    def __init__(self,title:str="hello! tkinter!",**kwargs): #**可有可無的隱數
        super().__init__(**kwargs) #呼叫父類別
        #多做一些事
        self.title(title)  #參數
        label:ttk.Label=ttk.Label(self,text="Hello! World!") #有內容所以視窗會依內容調整大小
        label.pack()



if __name__ == '__main__':
    names:list[str] = get_names()
    window:Window = Window(title="我的第一個GUI程式")  #沒有輸入會用上面hello! tkinter當預設視窗標題
    
    window.mainloop()   

