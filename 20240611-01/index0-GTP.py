import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

class Window(ThemedTk):
    def __init__(self, theme: str | None, **kwargs):
        super().__init__(**kwargs)
        self.title("BMI計算器")
        self.resizable(False, False)
        style = ttk.Style()
        style.configure('input.TFrame', background='#ffffff')
        style.configure('press.TButton', font=('arial', 16))
        
        # 標題的Label
        titleFrame = ttk.Frame(self)
        title_label = ttk.Label(self, text="BMI計算器", font=("Arial", 20))
        title_label.pack(pady=10)
        titleFrame.pack(padx=100, pady=(0, 20))
        
        # 建立輸入區的特殊背景框
        input_frame = ttk.Frame(self, style='input.TFrame')
        
        # 姓名
        label_name = ttk.Label(input_frame, text="姓名:")
        label_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_name = ttk.Entry(input_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # 身高體重
        label_height = ttk.Label(input_frame, text="身高 (cm):")
        label_height.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_height = ttk.Entry(input_frame)
        self.entry_height.grid(row=1, column=1, padx=5, pady=5)

        label_weight = ttk.Label(input_frame, text="體重 (kg):")
        label_weight.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_weight = ttk.Entry(input_frame)
        self.entry_weight.grid(row=2, column=1, padx=5, pady=5)

        input_frame.pack(pady=10, padx=30)
        
        # 計算按鈕
        button_calculate = ttk.Button(self, text="計算", command=self.show_bmi_result, style='press.TButton')
        button_calculate.pack(side=tk.RIGHT, padx=(0, 35), pady=10, ipadx=10, ipady=15)

    def show_bmi_result(self):
        try:
            name = self.entry_name.get().strip()
            height = float(self.entry_height.get().strip())
            weight = float(self.entry_weight.get().strip())

            if not name:
                raise ValueError("姓名不能為空")

            if height <= 0 or weight <= 0:
                raise ValueError("身高和體重必須是正數")

        except ValueError:
            messagebox.showwarning("Warning", f"格式錯誤")
        except Exception:
            messagebox.showwarning("Warning", f"未知的錯誤")
        else:
            self.show_result(name=name, height=height, weight=weight)

    def show_result(self, name, height, weight):
        bmi = weight / ((height / 100) ** 2)
        messagebox.showinfo("BMI計算結果", f"{name}，您的BMI是 {bmi:.2f}")

if __name__ == "__main__":
    app = Window(theme="breeze")
    app.mainloop()
