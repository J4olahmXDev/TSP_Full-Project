import tkinter as tk
import ui_module

if __name__ == "__main__":
    root = tk.Tk()
    # เรียกใช้ AppUI จาก ui_module
    app = ui_module.AppUI(root)
    # รันลูปโปรแกรม
    root.mainloop()
