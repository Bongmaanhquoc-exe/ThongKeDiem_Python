# ==============================================================
# student_model.py — Truy vấn bảng students (sinh viên)
# ==============================================================
from app.database import lay_nhieu, lay_mot, thuc_thi


def lay_tat_ca():
    """Lấy tất cả sinh viên kèm tên lớp."""
    return lay_nhieu(
        "SELECT s.*, c.name AS ten_lop "
        "FROM students s "
        "LEFT JOIN classes c ON s.class_id = c.id "
        "ORDER BY s.student_code"
    )


def lay_theo_id(student_id):
    return lay_mot("SELECT * FROM students WHERE id = %s", (student_id,))


def lay_theo_ma(ma_sv):
    return lay_mot("SELECT * FROM students WHERE student_code = %s", (ma_sv,))


def tim_kiem(tu_khoa):
    """Tìm theo mã SV hoặc họ tên (dùng LIKE)."""
    kw = f"%{tu_khoa}%"
    return lay_nhieu(
        "SELECT s.*, c.name AS ten_lop "
        "FROM students s "
        "LEFT JOIN classes c ON s.class_id = c.id "
        "WHERE s.student_code LIKE %s OR s.full_name LIKE %s",
        (kw, kw)
    )


def them(ma_sv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, class_id):
    return thuc_thi(
        "INSERT INTO students "
        "(student_code, full_name, dob, gender, email, phone, class_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (ma_sv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, class_id)
    )


def cap_nhat(student_id, ho_ten, ngay_sinh, gioi_tinh, email, sdt, class_id):
    thuc_thi(
        "UPDATE students "
        "SET full_name=%s, dob=%s, gender=%s, email=%s, phone=%s, class_id=%s "
        "WHERE id = %s",
        (ho_ten, ngay_sinh, gioi_tinh, email, sdt, class_id, student_id)
    )


def xoa(student_id):
    thuc_thi("DELETE FROM students WHERE id = %s", (student_id,))
