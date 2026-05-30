import tkinter as tk
import sys
import os

# Thêm thư mục gốc vào đường dẫn để import được app.*
sys.path.insert(0, os.path.dirname(__file__))

from app.views.login_view import LoginView


def main():
    root = tk.Tk()
    root.withdraw()   # ẩn cửa sổ gốc, chỉ hiện cửa sổ login

    def khi_dang_nhap_thanh_cong(user):
        from app.views.main_window import MainWindow
        MainWindow(root, user)

    LoginView(root, khi_dang_nhap_thanh_cong)
    root.mainloop()


if __name__ == '__main__':
    main()
