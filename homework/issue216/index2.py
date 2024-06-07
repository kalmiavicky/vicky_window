from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog
from ttkthemes import ThemedTk

class BMIApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="black")
        self.title("BMI 計算器")

        # 建立Label和Entry元件
        ttk.Label(self, text="姓名:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self, text="身高 (公分):").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self, text="體重 (公斤):").grid(row=2, column=0, padx=10, pady=5)

        self.name_entry = ttk.Entry(self)
        self.height_entry = ttk.Entry(self)
        self.weight_entry = ttk.Entry(self)

        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        # 建立計算按鈕
        self.calc_button = ttk.Button(self, text="計算 BMI", command=self.calculate_bmi)
        self.calc_button.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            height_cm = float(self.height_entry.get())
            weight_kg = float(self.weight_entry.get())
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)

            if bmi < 18.5:
                status = '過輕'
                color = 'red'
            elif 18.5 <= bmi < 24:
                status = '健康'
                color = 'green'
            elif 24 <= bmi < 27:
                status = '過重'
                color = 'red'
            elif 27 <= bmi < 30:
                status = '輕度肥胖'
                color = 'red'
            elif 30 <= bmi < 35:
                status = '中度肥胖'
                color = 'red'
            else:
                status = '重度肥胖'
                color = 'red'

            ResultDialog(self, name, bmi, status, color)
        except ValueError:
            messagebox.showerror("輸入錯誤", "請輸入有效的數字")

class ResultDialog(Dialog):
    def __init__(self, parent, name, bmi, status, color):
        self.name = name
        self.bmi = bmi
        self.status = status
        self.color = color
        super().__init__(parent, title="BMI 結果")

    def body(self, master):
        label1 = ttk.Label(master, text=f"{self.name}你好：", font=('Helvetica', 14), foreground='black')
        label1.pack(padx=20, pady=5)
        
        label2 = ttk.Label(master, text=f"BMI: {self.bmi:.2f}", font=('Helvetica', 14), foreground='black')
        label2.pack(padx=20, pady=5)
        
        label3 = ttk.Label(master, text=f"體重狀態：{self.status}", font=('Helvetica', 14), foreground=self.color)
        label3.pack(padx=20, pady=5)

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
