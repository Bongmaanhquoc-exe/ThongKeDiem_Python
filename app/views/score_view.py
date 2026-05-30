# ==============================================================
# score_view.py — Nhập điểm thi cho sinh viên
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import student_model, subject_model, score_model
from app.services import score_service
from app.views.bang_du_lieu import BangDuLieu


class NhapDiemView(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        ttk.Label(self, text="NHẬP ĐIỂM THI",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        # ── Chọn sinh viên ────────────────────────────────────
        khung_chon = ttk.LabelFrame(self, text="Chọn sinh viên", padding=8)
        khung_chon.pack(fill='x', padx=12, pady=4)

        ttk.Label(khung_chon, text="Sinh viên:").pack(side='left')
        self.combo_sv = ttk.Combobox(khung_chon, state='readonly', width=38)
        self.combo_sv.pack(side='left', padx=8)
        self.combo_sv.bind('<<ComboboxSelected>>', self._hien_diem_sv)
        ttk.Button(khung_chon, text="🔄", width=3,
                   command=self._lam_moi_sv).pack(side='left')
        self._lam_moi_sv()   # load lần đầu

        # Nhãn GPA
        self.lbl_gpa = ttk.Label(khung_chon, text="GPA: —",
                                  font=('Arial', 11, 'bold'), foreground='#2980b9')
        self.lbl_gpa.pack(side='right', padx=10)

        # ── Nút thao tác ──────────────────────────────────────
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=12, pady=4)
        if self.user.get('role') != 'viewer':
            ttk.Button(toolbar, text="+ Nhập điểm", command=self._them_diem).pack(side='left', padx=2)
            ttk.Button(toolbar, text="✎ Sửa điểm",  command=self._sua_diem).pack(side='left', padx=2)
            ttk.Button(toolbar, text="✕ Xoá điểm",  command=self._xoa_diem).pack(side='left', padx=2)

        # ── Bảng điểm ─────────────────────────────────────────
        self.bang = BangDuLieu(self, cac_cot=[
            ('ten_mon',       'Môn học',    200),
            ('credits',       'Tín chỉ',    70),
            ('semester',      'Học kỳ',     90),
            ('midterm_score', 'Giữa kỳ',    80),
            ('final_score',   'Cuối kỳ',    80),
            ('diem_tb',       'Điểm TB',    80),
            ('xep_loai',      'Xếp loại',   80),
        ])
        self.bang.pack(fill='both', expand=True, padx=12, pady=(4, 10))

    def _lam_moi_sv(self):
        """Tải lại danh sách sinh viên vào combo (dùng khi thêm SV mới)."""
        svien = student_model.lay_tat_ca()
        self.sv_map = {
            f"{s['student_code']} — {s['full_name']}": s['id']
            for s in svien
        }
        self.combo_sv['values'] = list(self.sv_map.keys())

    def _lay_student_id(self):
        """Lấy id của sinh viên đang chọn, hoặc None."""
        return self.sv_map.get(self.combo_sv.get())

    def _hien_diem_sv(self, _=None):
        """Khi chọn sinh viên → hiện bảng điểm của họ."""
        sid = self._lay_student_id()
        if not sid:
            return
        rows = score_service.lay_diem_sinh_vien(sid)
        self.bang.hien_du_lieu(rows)

        gpa = score_service.tinh_gpa(sid)
        self.lbl_gpa.config(text=f"GPA: {gpa:.2f}  ({score_service.xep_loai(gpa)})")

    def _them_diem(self):
        sid = self._lay_student_id()
        if not sid:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên trước.")
            return
        FormNhapDiem(self, student_id=sid, on_luu=self._hien_diem_sv)

    def _sua_diem(self):
        sid = self._lay_student_id()
        if not sid:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên trước.")
            return
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 dòng điểm để sửa.")
            return
        FormNhapDiem(self, student_id=sid, diem=dong, on_luu=self._hien_diem_sv)

    def _xoa_diem(self):
        dong = self.bang.lay_dong_chon()
        if not dong:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 dòng điểm để xoá.")
            return
        if messagebox.askyesno("Xác nhận", f"Xoá điểm môn '{dong['ten_mon']}'?"):
            score_model.xoa(dong['id'])
            self._hien_diem_sv()


# ── Form nhập / sửa điểm ──────────────────────────────────────
class FormNhapDiem(tk.Toplevel):
    def __init__(self, master, student_id, diem=None, on_luu=None):
        super().__init__(master)
        self.student_id = student_id
        self.diem    = diem      # None = thêm mới, có data = sửa
        self.on_luu  = on_luu

        self.title("Nhập điểm" if diem is None else "Sửa điểm")
        self.resizable(False, False)
        self.grab_set()

        # Lấy danh sách môn học
        mon_list = subject_model.lay_tat_ca()
        self.ten_mon_sang_id = {m['name']: m['id'] for m in mon_list}

        self._tao_giao_dien()
        if diem:
            self._dien_du_lieu()
            # Khi sửa: khoá combo môn, chỉ cho sửa điểm số
            self.combo_mon.config(state='disabled')

    def _tao_giao_dien(self):
        f = ttk.Frame(self, padding=20)
        f.pack()

        ttk.Label(f, text="Môn học:").grid(row=0, column=0, sticky='w', pady=5)
        self.combo_mon = ttk.Combobox(
            f, values=list(self.ten_mon_sang_id.keys()),
            state='readonly', width=26
        )
        self.combo_mon.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Học kỳ:").grid(row=1, column=0, sticky='w', pady=5)
        self.o_hk = ttk.Entry(f, width=28)
        self.o_hk.grid(row=1, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Điểm giữa kỳ (0–10):").grid(row=2, column=0, sticky='w', pady=5)
        self.o_gk = ttk.Entry(f, width=28)
        self.o_gk.grid(row=2, column=1, padx=(10, 0), pady=5)

        ttk.Label(f, text="Điểm cuối kỳ (0–10):").grid(row=3, column=0, sticky='w', pady=5)
        self.o_ck = ttk.Entry(f, width=28)
        self.o_ck.grid(row=3, column=1, padx=(10, 0), pady=5)

        # Hiển thị điểm TB tự động khi nhập
        ttk.Label(f, text="Điểm TB (tự tính):").grid(row=4, column=0, sticky='w', pady=5)
        self.lbl_tb = ttk.Label(f, text="—", foreground='blue', font=('Arial', 10, 'bold'))
        self.lbl_tb.grid(row=4, column=1, sticky='w', padx=(10, 0))

        self.o_gk.bind('<KeyRelease>', self._tinh_thu)
        self.o_ck.bind('<KeyRelease>', self._tinh_thu)

        ttk.Button(f, text="  Lưu điểm  ", command=self._luu).grid(
            row=5, column=0, columnspan=2, pady=16)

    def _tinh_thu(self, _=None):
        """Tính điểm TB thử ngay khi gõ."""
        try:
            gk = float(self.o_gk.get())
            ck = float(self.o_ck.get())
            tb = score_service.tinh_diem_tb(gk, ck)
            loai = score_service.xep_loai(tb)
            self.lbl_tb.config(text=f"{tb}  →  {loai}")
        except ValueError:
            self.lbl_tb.config(text="—")

    def _kiem_tra_diem(self, gia_tri, ten_truong):
        """
        Kiểm tra điểm hợp lệ: không rỗng, là số, trong khoảng 0-10.
        Trả về float nếu hợp lệ, None nếu không hợp lệ (đã hiện thông báo).
        """
        gia_tri = gia_tri.strip()
        if not gia_tri:
            messagebox.showerror("Lỗi nhập liệu",
                                 f"{ten_truong} không được để trống.", parent=self)
            return None
        try:
            diem = float(gia_tri)
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu",
                                 f"{ten_truong} phải là số (ví dụ: 7.5).", parent=self)
            return None
        if not (0 <= diem <= 10):
            messagebox.showerror("Lỗi nhập liệu",
                                 f"{ten_truong} phải từ 0 đến 10.", parent=self)
            return None
        return diem

    def _dien_du_lieu(self):
        self.combo_mon.set(self.diem.get('ten_mon', ''))
        self.o_hk.insert(0, self.diem.get('semester', ''))
        self.o_gk.insert(0, str(self.diem.get('midterm_score', '')))
        self.o_ck.insert(0, str(self.diem.get('final_score', '')))
        self._tinh_thu()

    def _luu(self):
        ten_mon = self.combo_mon.get()
        subject_id = self.ten_mon_sang_id.get(ten_mon)
        hoc_ky  = self.o_hk.get().strip()

        if not subject_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn môn học", parent=self)
            return
        if not hoc_ky:
            messagebox.showerror("Lỗi", "Vui lòng nhập học kỳ", parent=self)
            return
        gk = self._kiem_tra_diem(self.o_gk.get(), "Điểm giữa kỳ")
        if gk is None:
            return
        ck = self._kiem_tra_diem(self.o_ck.get(), "Điểm cuối kỳ")
        if ck is None:
            return

        score_model.them_hoac_cap_nhat(
            self.student_id, subject_id, hoc_ky, gk, ck
        )
        if self.on_luu:
            self.on_luu()
        self.destroy()
