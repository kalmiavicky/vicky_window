import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs): #**可有可無的隱數
        super().__init__(**kwargs) #呼叫父類別
        #多做一些事
        self.title("pack1")  #參數
        self.geometry("500x200")  #視窗大小

        ttk.Button(self,text="Left").pack(side="left")  #靠左
       

        ttk.Button(self,text="This is the Center Button").pack(side="left")
        

        ttk.Button(self,text="Right").pack(side="left")
        
      
if __name__ == '__main__':
    window:Window = Window()  
    window.mainloop() 
