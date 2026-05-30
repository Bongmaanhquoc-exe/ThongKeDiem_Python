# ==============================================================
# bang_du_lieu.py — Widget bảng dữ liệu dùng chung (Treeview)
# ==============================================================
import tkinter as tk
from tkinter import ttk


class BangDuLieu(ttk.Frame):
    """
    Bảng dữ liệu có thanh cuộn, hỗ trợ:
      - hien_du_lieu(list_dict)  : điền dữ liệu vào bảng
      - lay_dong_chon()          : trả về dict của dòng đang chọn (hoặc None)
    """

    def __init__(self, master, cac_cot):
        """
        cac_cot: list các tuple (key, tieu_de, do_rong)
        Ví dụ: [('full_name', 'Họ tên', 200), ('email', 'Email', 150)]
        """
        super().__init__(master)
        self._cac_key = [c[0] for c in cac_cot]
        self._du_lieu  = []    # lưu lại để get_selected có thể dùng

        # Tạo Treeview
        self._tree = ttk.Treeview(
            self,
            columns=self._cac_key,
            show='headings',
            selectmode='browse'   # chỉ chọn 1 dòng mỗi lần
        )

        # Cấu hình từng cột
        for key, tieu_de, do_rong in cac_cot:
            self._tree.heading(key, text=tieu_de)
            self._tree.column(key, width=do_rong, minwidth=40, anchor='w')

        # Thanh cuộn dọc
        cuon_doc = ttk.Scrollbar(self, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=cuon_doc.set)

        self._tree.pack(side='left', fill='both', expand=True)
        cuon_doc.pack(side='right', fill='y')

        # Màu xen kẽ cho dễ đọc
        self._tree.tag_configure('le',  background='#f0f4f8')
        self._tree.tag_configure('chan', background='#ffffff')

    def hien_du_lieu(self, du_lieu):
        """Xoá bảng cũ và điền dữ liệu mới."""
        self._tree.delete(*self._tree.get_children())
        self._du_lieu = du_lieu
        for i, dong in enumerate(du_lieu):
            gia_tri = [dong.get(k, '') for k in self._cac_key]
            tag = 'le' if i % 2 == 0 else 'chan'
            self._tree.insert('', 'end', iid=str(i), values=gia_tri, tags=(tag,))

    def lay_dong_chon(self):
        """Trả về dict của dòng đang được chọn, hoặc None nếu chưa chọn."""
        chon = self._tree.selection()
        if not chon:
            return None
        return self._du_lieu[int(chon[0])]
