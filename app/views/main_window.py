# ==============================================================
# main_window.py — Cửa sổ chính sau khi đăng nhập
# ==============================================================
import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Toplevel):
    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user    # dict chứa thông tin người dùng đang đăng nhập

        self.title(f"Quản lý Điểm Sinh viên — {user['full_name']} ({user['role']})")
        self.geometry("1100x650")
        self.state('zoomed')  # mở rộng toàn màn hình

        # Khi nhấn X → thoát hẳn chương trình
        self.protocol("WM_DELETE_WINDOW", self._thoat)

        ttk.Style().theme_use('clam')
        self._tao_giao_dien()

    def _thoat(self):
        self.root.destroy()  # huỷ root → mainloop() kết thúc → chương trình thoát

    def _dang_xuat(self):
        from tkinter import messagebox
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.destroy()                          # đóng cửa sổ chính
            from app.views.login_view import LoginView
            LoginView(self.root, self._khi_dang_nhap_lai)  # mở lại màn hình login

    def _khi_dang_nhap_lai(self, user):
        MainWindow(self.root, user)                 # mở lại cửa sổ chính với user mới

    def _tao_giao_dien(self):
        # ── Thanh menu bên trái ──────────────────────────────
        sidebar = tk.Frame(self, bg='#2c3e50', width=155)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)   # giữ nguyên width = 155

        tk.Label(sidebar, text="MENU",
                 bg='#2c3e50', fg='white',
                 font=('Arial', 11, 'bold')).pack(pady=(18, 10))

        # Danh sách menu — mỗi phần tử: (nhãn, hàm xử lý)
        cac_menu = [
            ("👤  Sinh viên",  self._mo_sinh_vien),
            ("🏫  Lớp học",    self._mo_lop),
            ("📚  Môn học",    self._mo_mon_hoc),
            ("📝  Nhập điểm",  self._mo_nhap_diem),
            ("📊  Thống kê",   self._mo_thong_ke),
        ]
        # Chỉ admin mới thấy menu Tài khoản
        if self.user['role'] == 'admin':
            cac_menu.append(("🔑  Tài khoản", self._mo_tai_khoan))

        for nhan, ham in cac_menu:
            tk.Button(
                sidebar, text=nhan, command=ham,
                bg='#34495e', fg='white',
                font=('Arial', 10), relief='flat',
                pady=9, anchor='w', padx=12,
                activebackground='#1abc9c',
                activeforeground='white',
                cursor='hand2'
            ).pack(fill='x', padx=6, pady=2)

        # Nút Đăng xuất — đặt ở dưới cùng sidebar
        tk.Frame(sidebar, bg='#2c3e50').pack(fill='y', expand=True)  # đẩy nút xuống đáy
        tk.Button(
            sidebar, text="🚪  Đăng xuất", command=self._dang_xuat,
            bg='#c0392b', fg='white',
            font=('Arial', 10), relief='flat',
            pady=9, anchor='w', padx=12,
            activebackground='#e74c3c',
            activeforeground='white',
            cursor='hand2'
        ).pack(fill='x', padx=6, pady=(2, 12))

        # ── Vùng nội dung ─────────────────────────────────────
        self.vung = ttk.Frame(self)
        self.vung.pack(side='left', fill='both', expand=True)

        # ── Thanh trạng thái dưới ──────────────────────────────
        ttk.Label(
            self,
            text=f"  Người dùng: {self.user['full_name']}  |  Quyền: {self.user['role']}  ",
            relief='sunken', anchor='w'
        ).pack(side='bottom', fill='x')

        # Hiện màn hình sinh viên mặc định
        self._mo_sinh_vien()

    # ── Xoá nội dung cũ trước khi chuyển trang ────────────────
    def _xoa_vung(self):
        for widget in self.vung.winfo_children():
            widget.destroy()

    # ── Các hàm chuyển trang ──────────────────────────────────
    def _mo_sinh_vien(self):
        self._xoa_vung()
        from app.views.student_view import SinhVienView
        SinhVienView(self.vung, self.user).pack(fill='both', expand=True)

    def _mo_lop(self):
        self._xoa_vung()
        from app.views.class_view import LopHocView
        LopHocView(self.vung, self.user).pack(fill='both', expand=True)

    def _mo_mon_hoc(self):
        self._xoa_vung()
        from app.views.subject_view import MonHocView
        MonHocView(self.vung, self.user).pack(fill='both', expand=True)

    def _mo_nhap_diem(self):
        self._xoa_vung()
        from app.views.score_view import NhapDiemView
        NhapDiemView(self.vung, self.user).pack(fill='both', expand=True)

    def _mo_thong_ke(self):
        self._xoa_vung()
        from app.views.report_view import ThongKeView
        ThongKeView(self.vung).pack(fill='both', expand=True)

    def _mo_tai_khoan(self):
        self._xoa_vung()
        from app.views.user_view import TaiKhoanView
        TaiKhoanView(self.vung, user_hien_tai=self.user).pack(fill='both', expand=True)
