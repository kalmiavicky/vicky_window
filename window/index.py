#自動開檔案
# with open('names.txt',encoding='utf-8') as file:
#     content:str = file.read()  #回傳字串
# #print(content)   #加print(content)可以列印出換行的名子
# names:list[str]=content.split() #算出有幾個名字 
# len(names)                       #算出有幾個名字  
# for name in names:
#     print(name)

import tkinter as tk


def get_names() -> list[str]:
    with open('names.txt',encoding='utf-8') as file:
        content:str = file.read()      #回傳字串
    names:list[str] = content.split()  #算出有幾個名字 
    return names
# names:list[str]=get_names()   #文件變數 所以和上面不會起充突
if __name__ == '__main__':
    names:list[str] = get_names()
    window:tk.Tk=tk.Tk()  #開視窗
    window.title("我的第一個GUI程式")  #視窗標題
    window.mainloop()     #開視窗

