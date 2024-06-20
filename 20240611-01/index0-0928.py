#用物件導向寫法
import tkinter as tk
from ttkthemes import ThemedTk

class Window(ThemedTk):
    def __init__(self,theme:str|None,**kwargs): #父類別  自訂
        super().__init__(**kwargs)


def main():
    window = Window(theme='arc')   #01建立實体
    window.mainloop()

if __name__ == '__main__':   #01
    main()


