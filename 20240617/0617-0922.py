import tkinter as tk
from tkinter import ttk
from tkinter import Misc
from PIL import Image, ImageTk

class Example(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        # 呼叫父類別的初始化方法
        super().__init__(master=master, **kwargs)
        # 設定主視窗標題
        master.title('Lines')
        # 設定框架的邊框寬度和樣式
        self.configure({'borderwidth': 2, 'relief': 'groove'})
        
        # 建立畫布
        canvas = tk.Canvas(self)
        # 繪製各種線條  X1,Y1 , X2,y2
        canvas.create_line(15, 30, 80, 30)  # 水平線 X1,Y1 , X2,y2
        canvas.create_line(120, 30, 185, 30)  # 水平線 X1,Y1 , X2,y2
        canvas.create_line(300, 35, 300, 200, dash=(8, 2))  # 垂直虛線 
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)  # 三角形
        canvas.create_line(300, 35, 250, 85, 350, 85, 300, 35)  # 菱形
        # 設定畫布填滿框架
        canvas.pack(expand=True, fill='both')
        # 設定框架填滿主視窗
        self.pack(expand=True, fill='both')

def main():
    # 建立主視窗
    window = tk.Tk()
    # 建立並顯示 Example 框架
    Example(window)
    # 設定主視窗的大小
    window.geometry("400x250")
    # 進入主迴圈
    window.mainloop()

if __name__ == "__main__":
    main()
