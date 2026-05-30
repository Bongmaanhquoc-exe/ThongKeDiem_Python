# ==============================================================
# student_view.py — Quản lý sinh viên (Xem / Thêm / Sửa / Xoá / Tìm)
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import student_model, class_model
from app.views.bang_du_lieu import BangDuLieu


class SinhVienView(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self._tao_giao_dien()
        self._tai_du_lieu()

    def _tao_giao_dien(self):
        # ── Tiêu đề ──────────────────────────────────────────
        ttk.Label(self, text="QUẢN LÝ SINH VIÊN",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        # ── Thanh công cụ ─────────────────────────────────────
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=12, pady=4)

        ttk.Button(toolbar, text="+ Thêm", command=self._them).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✎ Sửa",  command=self._sua).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✕ Xoá",  command=self._xoa).pack(side='left', padx=2)

        # Ô tìm kiếm bên phải
        ttk.Label(toolbar, text="Tìm:").pack(side='left', padx=(20, 4))
        self.o_tim = ttk.Entry(toolbar, width=22)
        self.o_tim.pack(side='left')
        ttk.Button(toolbar, text="🔍", command=self._tim_kiem).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✕", command=self._xoa_tim, width=3).pack(side='left')
        self.o_tim.bind('<Return>', lambda _: self._tim_kiem())

        # ── Bảng dữ liệu ──────────────────────────────────────
        self.bang = BangDuLieu(self, cac_cot=[
            ('student_code', 'Mã SV',      100),
            ('full_name',    'Họ và tên',  200),
            ('dob',          'Ngày sinh',  100),
            ('gender',       'Giới tính',   80),
            ('ten_lop',      'Lớp',        120),
            ('email',        'Email',      180),
            ('phone',        'Điện thoại', 110),
        ])
        self.bang.pack(fill='both', expand=True, padx=12, pady=(4, 10))

    def _tai_du_lieu(self, du_lieu=None):
        """Nạp dữ liệu vào bảng. Nếu không truyền thì lấy tất cả."""
        data = du_lieu if du_lieu is not None else student_model.lay_tat_ca()
        self.bang.hien_du_lieu(data)

    def _tim_kiem(self):
        tu_khoa = self.o_tim.get().strip()
        if tu_khoa:
            self._tai_du_lieu(student_model.tim_kiem(tu_khoa))
        else:
            self._tai_du_lieu()

    def _xoa_tim(self):
        self.o_tim.delete(0, 'end')
        self._tai_du_lieu()

    def _them(self):
        FormSinhVien(self, on_luu=self._tai_du_lieu)

    def _sua(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 sinh viên để sửa.")
            return
        FormSinhVien(self, sinh_vien=dong, on_luu=self._tai_du_lieu)

    def _xoa(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 sinh viên để xoá.")
            return
        xac_nhan = messagebox.askyesno(
            "Xác nhận xoá",
            f"Bạn có chắc muốn xoá sinh viên:\n{dong.get('full_name', '')}?"
        )
        if xac_nhan:
            student_model.xoa(dong['id'])
            self._tai_du_lieu()


# ── Form Thêm / Sửa sinh viên ─────────────────────────────────
class FormSinhVien(tk.Toplevel):
    def __init__(self, master, sinh_vien=None, on_luu=None):
        super().__init__(master)
        self.sinh_vien = sinh_vien   # None = thêm mới, có data = sửa
        self.on_luu    = on_luu

        self.title("Thêm sinh viên" if sinh_vien is None else "Sửa sinh viên")
        self.resizable(False, False)
        self.grab_set()

        self._lay_danh_sach_lop()
        self._tao_giao_dien()
        if sinh_vien:
            self._dien_du_lieu()

    def _lay_danh_sach_lop(self):
        """Lấy danh sách lớp cho Combobox."""
        lop_list = class_model.lay_tat_ca()
        self.ten_lop_sang_id = {c['name']: c['id'] for c in lop_list}
        self.id_sang_ten_lop = {c['id']:   c['name'] for c in lop_list}

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        cac_truong = [
            ('Mã sinh viên',             'ma_sv'),
            ('Họ và tên',               'ho_ten'),
            ('Ngày sinh (YYYY-MM-DD)',   'ngay_sinh'),
            ('Giới tính',               'gioi_tinh'),
            ('Email',                   'email'),
            ('Số điện thoại',           'sdt'),
            ('Lớp',                     'lop'),
        ]

        self.o = {}   # lưu các widget nhập liệu
        for i, (nhan, key) in enumerate(cac_truong):
            ttk.Label(f, text=nhan + ':').grid(row=i, column=0, sticky='w', pady=4)

            if key == 'gioi_tinh':
                w = ttk.Combobox(f, values=['Nam', 'Nữ', 'Khác'],
                                 state='readonly', width=24)
            elif key == 'lop':
                w = ttk.Combobox(f, values=list(self.ten_lop_sang_id.keys()),
                                 state='readonly', width=24)
            else:
                w = ttk.Entry(f, width=26)

            w.grid(row=i, column=1, padx=(10, 0), pady=4)
            self.o[key] = w

        ttk.Button(f, text="  Lưu  ", command=self._luu).grid(
            row=len(cac_truong), column=0, columnspan=2, pady=16)

    def _dien_du_lieu(self):
        """Điền thông tin sinh viên vào form khi sửa."""
        sv = self.sinh_vien
        anh_xa = {
            'ma_sv':     sv.get('student_code', ''),
            'ho_ten':    sv.get('full_name', ''),
            'ngay_sinh': str(sv.get('dob', '') or ''),
            'gioi_tinh': sv.get('gender', ''),
            'email':     sv.get('email', '') or '',
            'sdt':       sv.get('phone', '') or '',
            'lop':       self.id_sang_ten_lop.get(sv.get('class_id'), ''),
        }
        for key, gia_tri in anh_xa.items():
            w = self.o[key]
            if isinstance(w, ttk.Combobox):
                w.set(str(gia_tri))
            else:
                w.delete(0, 'end')
                w.insert(0, str(gia_tri))

    def _lay_du_lieu_form(self):
        """Đọc giá trị từ form, trả về dict."""
        ten_lop = self.o['lop'].get()
        return {
            'ma_sv':     self.o['ma_sv'].get().strip(),
            'ho_ten':    self.o['ho_ten'].get().strip(),
            'ngay_sinh': self.o['ngay_sinh'].get().strip() or None,
            'gioi_tinh': self.o['gioi_tinh'].get(),
            'email':     self.o['email'].get().strip() or None,
            'sdt':       self.o['sdt'].get().strip() or None,
            'class_id':  self.ten_lop_sang_id.get(ten_lop),
        }

    def _kiem_tra(self, d):
        if not d['ma_sv']:
            raise ValueError("Mã sinh viên không được để trống")
        if not d['ho_ten']:
            raise ValueError("Họ tên không được để trống")
        if not d['class_id']:
            raise ValueError("Vui lòng chọn lớp")
        # Kiểm tra định dạng ngày sinh
        if d['ngay_sinh']:
            from datetime import datetime
            try:
                datetime.strptime(d['ngay_sinh'], '%Y-%m-%d')
            except ValueError:
                raise ValueError(
                    "Ngày sinh sai định dạng!\n"
                    "Vui lòng nhập theo dạng: YYYY-MM-DD\n"
                    "Ví dụ: 2003-05-21"
                )

    def _luu(self):
        try:
            d = self._lay_du_lieu_form()
            self._kiem_tra(d)

            if self.sinh_vien is None:
                # Kiểm tra mã SV trùng
                if student_model.lay_theo_ma(d['ma_sv']):
                    raise ValueError(f"Mã SV '{d['ma_sv']}' đã tồn tại")
                student_model.them(
                    d['ma_sv'], d['ho_ten'], d['ngay_sinh'],
                    d['gioi_tinh'], d['email'], d['sdt'], d['class_id']
                )
            else:
                student_model.cap_nhat(
                    self.sinh_vien['id'],
                    d['ho_ten'], d['ngay_sinh'],
                    d['gioi_tinh'], d['email'], d['sdt'], d['class_id']
                )

            if self.on_luu:
                self.on_luu()
            self.destroy()

        except ValueError as loi:
            messagebox.showerror("Lỗi nhập liệu", str(loi), parent=self)
