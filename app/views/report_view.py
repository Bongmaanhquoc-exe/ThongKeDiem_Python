# ==============================================================
# report_view.py — Thống kê báo cáo (theo môn + bảng xếp hạng)
# ==============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from app.models import subject_model, class_model
from app.services import report_service
from app.utils.exporter import xuat_excel
from app.views.bang_du_lieu import BangDuLieu


class ThongKeView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        ttk.Label(self, text="THỐNG KÊ BÁO CÁO",
                  font=('Arial', 13, 'bold')).pack(pady=(10, 4))

        # Dùng Notebook (tab) để chứa 2 chức năng
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=12, pady=4)

        # Tab 1: Thống kê theo môn
        tab_mon = ttk.Frame(nb)
        nb.add(tab_mon, text="  📊 Theo môn học  ")
        self._tao_tab_mon(tab_mon)

        # Tab 2: Bảng xếp hạng
        tab_hang = ttk.Frame(nb)
        nb.add(tab_hang, text="  🏆 Bảng xếp hạng  ")
        self._tao_tab_xep_hang(tab_hang)

    # ════════════════════════════════════════════════════════
    # TAB 1 — Thống kê theo môn học
    # ════════════════════════════════════════════════════════
    def _tao_tab_mon(self, parent):
        # Chọn môn
        khung = ttk.Frame(parent)
        khung.pack(fill='x', padx=10, pady=8)

        ttk.Label(khung, text="Môn học:").pack(side='left')
        self.combo_mon = ttk.Combobox(khung, width=30)
        self.combo_mon.pack(side='left', padx=8)
        self.combo_mon.bind('<KeyRelease>', self._loc_mon)
        ttk.Button(khung, text="Xem thống kê", command=self._xem_thong_ke_mon).pack(side='left')
        ttk.Button(khung, text="🔄", width=3,
                   command=self._lam_moi_mon).pack(side='left', padx=4)
        self._lam_moi_mon()  # load lần đầu

        # Nhãn tóm tắt
        self.lbl_tomtat = ttk.Label(parent, text="", font=('Arial', 10),
                                     foreground='#2c3e50')
        self.lbl_tomtat.pack(fill='x', padx=10, pady=4)

        # Bảng chi tiết điểm
        ttk.Label(parent, text="Chi tiết điểm từng sinh viên:",
                  font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
        self.bang_mon = BangDuLieu(parent, cac_cot=[
            ('student_code', 'Mã SV',    100),
            ('full_name',    'Họ tên',   200),
            ('midterm_score','Giữa kỳ',   90),
            ('final_score',  'Cuối kỳ',   90),
        ])
        self.bang_mon.pack(fill='both', expand=True, padx=10, pady=4)

    def _lam_moi_mon(self):
        mon_list = subject_model.lay_tat_ca()
        self.mon_map = {m['name']: m['id'] for m in mon_list}
        self.combo_mon['values'] = list(self.mon_map.keys())

    def _loc_mon(self, _=None):
        tu_khoa = self.combo_mon.get().lower()
        tat_ca = list(self.mon_map.keys())
        loc = [m for m in tat_ca if tu_khoa in m.lower()] if tu_khoa else tat_ca
        self.combo_mon['values'] = loc
        if loc:
            self.combo_mon.event_generate('<Down>')

    def _xem_thong_ke_mon(self):
        subject_id = self.mon_map.get(self.combo_mon.get())
        if not subject_id:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn môn học.")
            return
        ks = report_service.thong_ke_theo_mon(subject_id)
        if not ks:
            self.lbl_tomtat.config(text="Môn này chưa có điểm.")
            self.bang_mon.hien_du_lieu([])
            return

        self.lbl_tomtat.config(
            text=(
                f"Tổng: {ks['tong_sv']} SV  |  "
                f"Điểm TB: {ks['diem_tb']}  |  "
                f"Cao nhất: {ks['cao_nhat']}  |  "
                f"Thấp nhất: {ks['thap_nhat']}  |  "
                f"Tỉ lệ qua: {ks['ti_le_qua']}%"
            )
        )
        self.bang_mon.hien_du_lieu(ks['chi_tiet'])

    # ════════════════════════════════════════════════════════
    # TAB 2 — Bảng xếp hạng GPA
    # ════════════════════════════════════════════════════════
    def _tao_tab_xep_hang(self, parent):
        # Bộ lọc
        khung = ttk.Frame(parent)
        khung.pack(fill='x', padx=10, pady=8)

        ttk.Label(khung, text="Lọc theo lớp:").pack(side='left')
        self.combo_lop = ttk.Combobox(khung, width=20)
        self.combo_lop.pack(side='left', padx=8)
        self.combo_lop.bind('<KeyRelease>', self._loc_lop)
        ttk.Button(khung, text="Xem xếp hạng", command=self._xem_xep_hang).pack(side='left')
        ttk.Button(khung, text="🔄", width=3,
                   command=self._lam_moi_lop).pack(side='left', padx=4)
        ttk.Button(khung, text="📥 Xuất Excel",  command=self._xuat_excel).pack(side='left', padx=6)
        self._lam_moi_lop()  # load lần đầu

        # Bảng xếp hạng
        self.bang_hang = BangDuLieu(parent, cac_cot=[
            ('thu_hang', '#',         45),
            ('ma_sv',    'Mã SV',    100),
            ('ho_ten',   'Họ tên',   220),
            ('ten_lop',  'Lớp',      120),
            ('gpa',      'GPA',       70),
            ('xep_loai', 'Xếp loại',  80),
        ])
        self.bang_hang.pack(fill='both', expand=True, padx=10, pady=4)
        self._du_lieu_hang = []

    def _lam_moi_lop(self):
        lop_list = class_model.lay_tat_ca()
        self.lop_map = {'-- Tất cả --': None}
        self.lop_map.update({c['name']: c['id'] for c in lop_list})
        self.combo_lop['values'] = list(self.lop_map.keys())
        self.combo_lop.set('-- Tất cả --')

    def _loc_lop(self, _=None):
        tu_khoa = self.combo_lop.get().lower()
        tat_ca = list(self.lop_map.keys())
        loc = [l for l in tat_ca if tu_khoa in l.lower()] if tu_khoa else tat_ca
        self.combo_lop['values'] = loc
        if loc:
            self.combo_lop.event_generate('<Down>')

    def _xem_xep_hang(self):
        class_id = self.lop_map.get(self.combo_lop.get())
        self._du_lieu_hang = report_service.bang_xep_hang(class_id)
        self.bang_hang.hien_du_lieu(self._du_lieu_hang)

    def _xuat_excel(self):
        if not self._du_lieu_hang:
            messagebox.showwarning("Chưa có dữ liệu", "Nhấn 'Xem xếp hạng' trước.")
            return
        ten_cot = {
            'thu_hang': 'Thứ hạng', 'ma_sv': 'Mã SV', 'ho_ten': 'Họ tên',
            'ten_lop': 'Lớp', 'gpa': 'GPA', 'xep_loai': 'Xếp loại',
        }
        duong_dan = xuat_excel(self._du_lieu_hang, 'bang_xep_hang.xlsx', ten_cot)
        messagebox.showinfo("Thành công", f"Đã xuất file:\n{duong_dan}")
