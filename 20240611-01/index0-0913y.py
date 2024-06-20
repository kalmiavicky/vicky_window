#用物件導向寫法
import tkinter as tk

class Window(tk.Tk):   
    pass


def main():
    window = Window()
    window.mainloop()

if __name__ == '__main__':
    main()