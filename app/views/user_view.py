# ==============================================================
# user_view.py — Quản lý tài khoản (chỉ admin dùng được)
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import user_model
from app.services import auth_service
from app.views.bang_du_lieu import BangDuLieu

ROLES = ['admin', 'teacher', 'viewer']


class TaiKhoanView(ttk.Frame):
    def __init__(self, master, user_hien_tai=None):
        super().__init__(master)
        self.user_hien_tai = user_hien_tai   # tài khoản đang đăng nhập
        self._tao_giao_dien()
        self._tai_du_lieu()

    def _tao_giao_dien(self):
        ttk.Label(self, text="QUẢN LÝ TÀI KHOẢN",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=12, pady=4)
        ttk.Button(toolbar, text="+ Thêm tài khoản",  command=self._them).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🔓 Đổi mật khẩu",   command=self._doi_mk).pack(side='left', padx=2)
        ttk.Button(toolbar, text="⏸ Khoá / Mở khoá", command=self._doi_trang_thai).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✕ Xoá",             command=self._xoa).pack(side='left', padx=2)

        self.bang = BangDuLieu(self, cac_cot=[
            ('id',         'ID',         50),
            ('username',   'Tên đăng nhập', 140),
            ('full_name',  'Họ tên',     220),
            ('role',       'Quyền',       90),
            ('is_active',  'Kích hoạt',   80),
            ('created_at', 'Ngày tạo',   140),
        ])
        self.bang.pack(fill='both', expand=True, padx=12, pady=(4, 10))

    def _tai_du_lieu(self):
        self.bang.hien_du_lieu(user_model.lay_tat_ca())

    def _them(self):
        FormTaiKhoan(self, on_luu=self._tai_du_lieu)

    def _doi_mk(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn tài khoản.")
            return
        FormDoiMatKhau(self, user_id=dong['id'], on_luu=self._tai_du_lieu)

    def _doi_trang_thai(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn tài khoản.")
            return
        # Không cho khoá tài khoản đang đăng nhập
        if self.user_hien_tai and dong['id'] == self.user_hien_tai['id']:
            messagebox.showerror("Không thể khoá",
                                 "Bạn không thể khoá tài khoản đang dùng để đăng nhập.")
            return
        hien_tai = bool(dong['is_active'])
        hanh_dong = "khoá" if hien_tai else "mở khoá"
        if messagebox.askyesno("Xác nhận", f"Bạn muốn {hanh_dong} tài khoản '{dong['username']}'?"):
            user_model.doi_trang_thai(dong['id'], not hien_tai)
            self._tai_du_lieu()

    def _xoa(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn tài khoản.")
            return
        # Không cho xoá tài khoản đang đăng nhập
        if self.user_hien_tai and dong['id'] == self.user_hien_tai['id']:
            messagebox.showerror("Không thể xoá",
                                 "Bạn không thể xoá tài khoản đang dùng để đăng nhập.")
            return
        if messagebox.askyesno("Xác nhận xoá", f"Xoá tài khoản '{dong['username']}'?"):
            user_model.xoa(dong['id'])
            self._tai_du_lieu()


# ── Form tạo tài khoản mới ────────────────────────────────────
class FormTaiKhoan(tk.Toplevel):
    def __init__(self, master, on_luu=None):
        super().__init__(master)
        self.on_luu = on_luu
        self.title("Thêm tài khoản")
        self.resizable(False, False)
        self.grab_set()
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        cac_truong = [
            ("Tên đăng nhập:",  "username"),
            ("Họ và tên:",      "full_name"),
            ("Mật khẩu:",       "password"),
        ]
        self.o = {}
        for i, (nhan, key) in enumerate(cac_truong):
            ttk.Label(f, text=nhan).grid(row=i, column=0, sticky='w', pady=5)
            show = '*' if key == 'password' else ''
            e = ttk.Entry(f, width=26, show=show)
            e.grid(row=i, column=1, padx=(10, 0), pady=5)
            self.o[key] = e

        ttk.Label(f, text="Quyền:").grid(row=3, column=0, sticky='w', pady=5)
        self.combo_role = ttk.Combobox(f, values=ROLES, state='readonly', width=24)
        self.combo_role.set('teacher')
        self.combo_role.grid(row=3, column=1, padx=(10, 0), pady=5)

        ttk.Button(f, text="  Tạo tài khoản  ", command=self._luu).grid(
            row=4, column=0, columnspan=2, pady=14)

        self.o['username'].focus()

    def _luu(self):
        try:
            auth_service.tao_tai_khoan(
                self.o['username'].get(),
                self.o['password'].get(),
                self.o['full_name'].get(),
                self.combo_role.get()
            )
            if self.on_luu:
                self.on_luu()
            self.destroy()
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi), parent=self)


# ── Form đặt lại mật khẩu (admin không cần biết mật khẩu cũ) ─
class FormDoiMatKhau(tk.Toplevel):
    def __init__(self, master, user_id, on_luu=None):
        super().__init__(master)
        self.user_id = user_id
        self.on_luu  = on_luu
        self.title("Đặt lại mật khẩu")
        self.resizable(False, False)
        self.grab_set()
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        ttk.Label(f, text="Mật khẩu mới:", font=('Arial', 10)).grid(
            row=0, column=0, sticky='w', pady=5)
        self.o_moi = ttk.Entry(f, width=26, show='*')
        self.o_moi.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Nhập lại:", font=('Arial', 10)).grid(
            row=1, column=0, sticky='w', pady=5)
        self.o_xn = ttk.Entry(f, width=26, show='*')
        self.o_xn.grid(row=1, column=1, padx=(10, 0), pady=5)

        ttk.Button(f, text="  Đặt lại  ", command=self._luu).grid(
            row=2, column=0, columnspan=2, pady=14)

        self.o_moi.focus()

    def _luu(self):
        mk_moi = self.o_moi.get()
        mk_xn  = self.o_xn.get()
        if mk_moi != mk_xn:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp.", parent=self)
            return
        try:
            auth_service.dat_lai_mat_khau(self.user_id, mk_moi)
            messagebox.showinfo("Thành công", "Đặt lại mật khẩu thành công!", parent=self)
            if self.on_luu:
                self.on_luu()
            self.destroy()
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi), parent=self)
