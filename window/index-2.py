
import tkinter as tk


def get_names() -> list[str]:
    with open('names.txt',encoding='utf-8') as file:
        content:str = file.read()      #回傳字串
    names:list[str] = content.split()  #算出有幾個名字 
    return names
# names:list[str]=get_names()   #文件變數 所以和上面不會起充突
class window(tk.Tk):
    def __init__(self):
    super().__init__() #呼叫父類別
    #多做一些事
    self.title("我的第一個GUI程式")  #視窗標題



if __name__ == '__main__':
    names:list[str] = get_names()
    window:window = window()  
   
    window.mainloop()   

