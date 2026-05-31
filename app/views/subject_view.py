# ==============================================================
# subject_view.py — Quản lý môn học (Xem / Thêm / Sửa / Xoá)
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import subject_model
from app.views.bang_du_lieu import BangDuLieu


class MonHocView(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self._tao_giao_dien()
        self._tai_du_lieu()

    def _tao_giao_dien(self):
        ttk.Label(self, text="QUẢN LÝ MÔN HỌC",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=12, pady=4)
        if self.user.get('role') != 'viewer':
            ttk.Button(toolbar, text="+ Thêm", command=self._them).pack(side='left', padx=2)
            ttk.Button(toolbar, text="✎ Sửa",  command=self._sua).pack(side='left', padx=2)
            ttk.Button(toolbar, text="✕ Xoá",  command=self._xoa).pack(side='left', padx=2)

        # Thanh tìm kiếm
        khung_tk = ttk.Frame(self)
        khung_tk.pack(fill='x', padx=12, pady=(0, 4))
        ttk.Label(khung_tk, text="Tìm kiếm:").pack(side='left')
        self.o_tim = ttk.Entry(khung_tk, width=30)
        self.o_tim.pack(side='left', padx=6)
        self.o_tim.bind('<KeyRelease>', self._tim_kiem)
        ttk.Button(khung_tk, text="✕", width=2,
                   command=self._xoa_tim).pack(side='left')

        self.bang = BangDuLieu(self, cac_cot=[
            ('subject_code', 'Mã môn',   120),
            ('name',         'Tên môn',  280),
            ('credits',      'Tín chỉ',   80),
        ])
        self.bang.pack(fill='both', expand=True, padx=12, pady=(4, 10))

    def _tai_du_lieu(self):
        self._du_lieu_goc = subject_model.lay_tat_ca()
        self._loc_va_hien(self.o_tim.get() if hasattr(self, 'o_tim') else '')

    def _loc_va_hien(self, tu_khoa):
        tu_khoa = tu_khoa.strip().lower()
        if tu_khoa:
            ds = [m for m in self._du_lieu_goc
                  if tu_khoa in m['subject_code'].lower()
                  or tu_khoa in m['name'].lower()]
        else:
            ds = self._du_lieu_goc
        self.bang.hien_du_lieu(ds)

    def _tim_kiem(self, _=None):
        self._loc_va_hien(self.o_tim.get())

    def _xoa_tim(self):
        self.o_tim.delete(0, 'end')
        self._loc_va_hien('')

    def _them(self):
        FormMonHoc(self, on_luu=self._tai_du_lieu)

    def _sua(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 môn để sửa.")
            return
        FormMonHoc(self, mon=dong, on_luu=self._tai_du_lieu)

    def _xoa(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 môn để xoá.")
            return
        if messagebox.askyesno("Xác nhận", f"Xoá môn '{dong['name']}'?"):
            try:
                subject_model.xoa(dong['id'])
                self._tai_du_lieu()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xoá (môn đang có điểm).\n{e}")


class FormMonHoc(tk.Toplevel):
    def __init__(self, master, mon=None, on_luu=None):
        super().__init__(master)
        self.mon    = mon
        self.on_luu = on_luu
        self.title("Thêm môn học" if mon is None else "Sửa môn học")
        self.resizable(False, False)
        self.grab_set()
        self._tao_giao_dien()
        if mon:
            self.o_ma.insert(0, mon.get('subject_code', ''))
            self.o_ma.config(state='disabled')   # không cho đổi mã môn khi sửa
            self.o_ten.insert(0, mon.get('name', ''))
            self.o_tc.insert(0, str(mon.get('credits', 3)))

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        ttk.Label(f, text="Mã môn:").grid(row=0, column=0, sticky='w', pady=5)
        self.o_ma = ttk.Entry(f, width=28)
        self.o_ma.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Tên môn:").grid(row=1, column=0, sticky='w', pady=5)
        self.o_ten = ttk.Entry(f, width=28)
        self.o_ten.grid(row=1, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Số tín chỉ:").grid(row=2, column=0, sticky='w', pady=5)
        self.o_tc = ttk.Entry(f, width=28)
        self.o_tc.grid(row=2, column=1, padx=(10, 0), pady=5)

        ttk.Button(f, text="  Lưu  ", command=self._luu).grid(
            row=3, column=0, columnspan=2, pady=14)

        self.o_ma.focus()

    def _luu(self):
        ma  = self.o_ma.get().strip()
        ten = self.o_ten.get().strip()
        tc  = self.o_tc.get().strip()

        if not ma or not ten:
            messagebox.showerror("Lỗi", "Mã môn và tên môn không được để trống", parent=self)
            return
        try:
            so_tc = int(tc)
            if so_tc <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên dương", parent=self)
            return

        try:
            if self.mon is None:
                subject_model.them(ma, ten, so_tc)
            else:
                subject_model.cap_nhat(self.mon['id'], ten, so_tc)
            if self.on_luu:
                self.on_luu()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
