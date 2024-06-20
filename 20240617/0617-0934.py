import tkinter as tk
from tkinter import ttk
from tkinter import Misc
from PIL import Image, ImageTk

class Example1(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        # 呼叫父類別的初始化方法
        super().__init__(master=master, **kwargs)
        # 設定主視窗標題
        master.title('Colors')
        # 設定框架的邊框寬度和樣式
        self.configure({'borderwidth': 2, 'relief': 'groove'})
        
        # 建立畫布
        canvas = tk.Canvas(self)
        # 繪製矩形
        canvas.create_rectangle(30, 10, 120, 80, outline='#000', fill='#fb0')
        # 繪製文字
        canvas.create_text(40, 40, text='中文測試', anchor='nw', fill='#0a0', font=('Arial', 12, 'bold', 'italic'))
        # 繪製橢圓形
        canvas.create_oval(150, 10, 200, 60, outline='#000', fill='#1f1', width=2)
        
        # 加載並顯示圖片
        self.img = Image.open('tvdi.png')
        self.tvdi = ImageTk.PhotoImage(self.img)
        canvas.create_image(210, 10, anchor='nw', image=self.tvdi)
        
        # 設定畫布填滿框架
        canvas.pack(expand=True, fill='both')
        # 設定框架填滿主視窗
        self.pack(expand=True, fill='both')

def main():
    # 建立主視窗
    window = tk.Tk()
    # 建立並顯示 Example1 框架
    Example1(window)
    # 設定主視窗的大小
    window.geometry("400x100")
    # 進入主迴圈
    window.mainloop()

if __name__ == "__main__":
    main()
