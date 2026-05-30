# ==============================================================
# subject_model.py — Truy vấn bảng subjects (môn học)
# ==============================================================
from app.database import lay_nhieu, lay_mot, thuc_thi


def lay_tat_ca():
    return lay_nhieu("SELECT * FROM subjects ORDER BY subject_code")


def lay_theo_id(subject_id):
    return lay_mot("SELECT * FROM subjects WHERE id = %s", (subject_id,))


def them(ma_mon, ten_mon, tin_chi):
    return thuc_thi(
        "INSERT INTO subjects (subject_code, name, credits) VALUES (%s, %s, %s)",
        (ma_mon, ten_mon, tin_chi)
    )


def cap_nhat(subject_id, ten_mon, tin_chi):
    thuc_thi(
        "UPDATE subjects SET name = %s, credits = %s WHERE id = %s",
        (ten_mon, tin_chi, subject_id)
    )


def xoa(subject_id):
    thuc_thi("DELETE FROM subjects WHERE id = %s", (subject_id,))
