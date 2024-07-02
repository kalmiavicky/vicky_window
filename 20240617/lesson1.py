import tkinter as tk
from tkinter import ttk
from tkinter import Misc
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Example2(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        master.title('Plot')
        self.configure(borderwidth=2, relief='groove')
        
        # 繪製圖表
        figure = plt.figure(figsize=(5, 4), dpi=100)
        axes = figure.add_subplot()
        axes.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])
        axes.set_title("Sample Chart")
        axes.set_xlabel("X-axis")
        axes.set_ylabel("Y-axis")
        
        # 將圖表嵌入到 tkinter 中
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='both', padx=30, pady=30)
        self.pack(expand=True, fill='both')
        
        # 綁定窗口關閉事件
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # 清理 matplotlib 圖表
        plt.close('all')
        # 關閉 tkinter 窗口
        self.master.destroy()

def main():
    window = tk.Tk()
    
    Example2(window)
    window.geometry("600x500")
    window.mainloop()

if __name__ == "__main__":
    main()
