# ==============================================================
# class_view.py — Quản lý lớp học (Xem / Thêm / Sửa / Xoá)
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import class_model
from app.views.bang_du_lieu import BangDuLieu


class LopHocView(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self._tao_giao_dien()
        self._tai_du_lieu()

    def _tao_giao_dien(self):
        ttk.Label(self, text="QUẢN LÝ LỚP HỌC",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=12, pady=4)
        ttk.Button(toolbar, text="+ Thêm", command=self._them).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✎ Sửa",  command=self._sua).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✕ Xoá",  command=self._xoa).pack(side='left', padx=2)

        self.bang = BangDuLieu(self, cac_cot=[
            ('id',      'ID',    60),
            ('name',    'Tên lớp',  200),
            ('faculty', 'Khoa / Ngành', 300),
        ])
        self.bang.pack(fill='both', expand=True, padx=12, pady=(4, 10))

    def _tai_du_lieu(self):
        self.bang.hien_du_lieu(class_model.lay_tat_ca())

    def _them(self):
        FormLopHoc(self, on_luu=self._tai_du_lieu)

    def _sua(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 lớp để sửa.")
            return
        FormLopHoc(self, lop=dong, on_luu=self._tai_du_lieu)

    def _xoa(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 lớp để xoá.")
            return
        if messagebox.askyesno("Xác nhận", f"Xoá lớp '{dong['name']}'?"):
            try:
                class_model.xoa(dong['id'])
                self._tai_du_lieu()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xoá (có thể lớp đang có sinh viên).\n{e}")


class FormLopHoc(tk.Toplevel):
    def __init__(self, master, lop=None, on_luu=None):
        super().__init__(master)
        self.lop    = lop
        self.on_luu = on_luu
        self.title("Thêm lớp" if lop is None else "Sửa lớp")
        self.resizable(False, False)
        self.grab_set()
        self._tao_giao_dien()
        if lop:
            self.o_ten.insert(0, lop.get('name', ''))
            self.o_khoa.insert(0, lop.get('faculty', '') or '')

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        ttk.Label(f, text="Tên lớp:").grid(row=0, column=0, sticky='w', pady=5)
        self.o_ten = ttk.Entry(f, width=28)
        self.o_ten.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Khoa / Ngành:").grid(row=1, column=0, sticky='w', pady=5)
        self.o_khoa = ttk.Entry(f, width=28)
        self.o_khoa.grid(row=1, column=1, padx=(10, 0), pady=5)

        ttk.Button(f, text="  Lưu  ", command=self._luu).grid(
            row=2, column=0, columnspan=2, pady=14)

        self.o_ten.focus()

    def _luu(self):
        ten  = self.o_ten.get().strip()
        khoa = self.o_khoa.get().strip()
        if not ten:
            messagebox.showerror("Lỗi", "Tên lớp không được để trống", parent=self)
            return
        try:
            if self.lop is None:
                class_model.them(ten, khoa)
            else:
                class_model.cap_nhat(self.lop['id'], ten, khoa)
            if self.on_luu:
                self.on_luu()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
