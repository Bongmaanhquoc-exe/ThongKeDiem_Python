# ==============================================================
# class_model.py — Truy vấn bảng classes (lớp học)
# ==============================================================
from app.database import lay_nhieu, lay_mot, thuc_thi


def lay_tat_ca():
    return lay_nhieu("SELECT * FROM classes ORDER BY name")


def lay_theo_id(class_id):
    return lay_mot("SELECT * FROM classes WHERE id = %s", (class_id,))


def them(ten_lop, khoa):
    return thuc_thi(
        "INSERT INTO classes (name, faculty) VALUES (%s, %s)",
        (ten_lop, khoa)
    )


def cap_nhat(class_id, ten_lop, khoa):
    thuc_thi(
        "UPDATE classes SET name = %s, faculty = %s WHERE id = %s",
        (ten_lop, khoa, class_id)
    )


def xoa(class_id):
    thuc_thi("DELETE FROM classes WHERE id = %s", (class_id,))
