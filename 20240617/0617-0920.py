import tkinter as tk
from tkinter import ttk
from tkinter import Misc

class Example(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        # 初始化父類別 (ttk.Frame)
        super().__init__(master=master, **kwargs)
        # 可以在這裡添加更多的初始化程式碼
        # 例如，創建子部件或設置屬性

        # 建立一個標籤 (Label) 作為示例
        label = ttk.Label(self, text="這是一個範例")
        label.pack(pady=20)  # 添加一些間距

        # 建立一個按鈕 (Button) 作為示例
        button = ttk.Button(self, text="按鈕")
        button.pack(pady=10)  # 添加一些間距

def main():
    # 創建主視窗 (window)
    window = tk.Tk()
    window.title("Frame的繼承")
    window.geometry("400x250")

    # 創建並顯示 Example 框架
    example_frame = Example(master=window)
    example_frame.pack(fill="both", expand=True)

    # 開始主事件循環
    window.mainloop()

if __name__ == "__main__":
    main()
