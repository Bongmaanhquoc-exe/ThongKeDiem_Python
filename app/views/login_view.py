# ==============================================================
# login_view.py — Màn hình đăng nhập
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.services import auth_service


class LoginView(tk.Toplevel):
    def __init__(self, root, callback_thanh_cong):
        super().__init__(root)
        self.callback = callback_thanh_cong

        self.title("Đăng nhập")
        self.resizable(False, False)
        self.grab_set()                   # khoá tương tác lên cửa sổ khác

        self._can_giua(340, 220)
        self._tao_giao_dien()

        # Nhấn X → thoát hẳn chương trình
        self.protocol("WM_DELETE_WINDOW", root.destroy)

    def _can_giua(self, w, h):
        """Đặt cửa sổ vào giữa màn hình."""
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=28)
        f.pack(fill='both', expand=True)

        ttk.Label(f, text="QUẢN LÝ ĐIỂM SINH VIÊN",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 18))

        ttk.Label(f, text="Tài khoản:").grid(row=1, column=0, sticky='w')
        self.o_tk = ttk.Entry(f, width=22)
        self.o_tk.grid(row=1, column=1, padx=(8, 0), pady=4)

        ttk.Label(f, text="Mật khẩu:").grid(row=2, column=0, sticky='w')
        self.o_mk = ttk.Entry(f, width=22, show='*')
        self.o_mk.grid(row=2, column=1, padx=(8, 0), pady=4)

        ttk.Button(f, text="  Đăng nhập  ", command=self._xu_ly_dang_nhap).grid(
            row=3, column=0, columnspan=2, pady=16)

        self.o_tk.focus()
        self.bind('<Return>', lambda _: self._xu_ly_dang_nhap())

    def _xu_ly_dang_nhap(self):
        try:
            user = auth_service.dang_nhap(self.o_tk.get(), self.o_mk.get())
            self.destroy()
            self.callback(user)
        except ValueError as loi:
            messagebox.showerror("Đăng nhập thất bại", str(loi), parent=self)
            self.o_mk.delete(0, 'end')
            self.o_mk.focus()
