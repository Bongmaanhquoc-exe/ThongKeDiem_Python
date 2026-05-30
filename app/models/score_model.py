# ==============================================================
# score_model.py — Truy vấn bảng scores (điểm thi)
# ==============================================================
from app.database import lay_nhieu, lay_mot, thuc_thi


def lay_theo_sinh_vien(student_id):
    """Lấy tất cả điểm của 1 sinh viên, kèm tên môn và số tín chỉ."""
    return lay_nhieu(
        "SELECT sc.id, sc.semester, sc.midterm_score, sc.final_score, "
        "       sub.name AS ten_mon, sub.credits "
        "FROM scores sc "
        "JOIN subjects sub ON sc.subject_id = sub.id "
        "WHERE sc.student_id = %s "
        "ORDER BY sub.subject_code",
        (student_id,)
    )


def lay_theo_mon(subject_id):
    """Lấy tất cả điểm của 1 môn học, kèm thông tin sinh viên."""
    return lay_nhieu(
        "SELECT sc.id, sc.semester, sc.midterm_score, sc.final_score, "
        "       s.student_code, s.full_name "
        "FROM scores sc "
        "JOIN students s ON sc.student_id = s.id "
        "WHERE sc.subject_id = %s "
        "ORDER BY s.student_code",
        (subject_id,)
    )


def them_hoac_cap_nhat(student_id, subject_id, hoc_ky, diem_giua, diem_cuoi):
    """INSERT nếu chưa có, UPDATE nếu đã tồn tại (cùng sv + môn + học kỳ)."""
    thuc_thi(
        "INSERT INTO scores (student_id, subject_id, semester, midterm_score, final_score) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE midterm_score = %s, final_score = %s",
        (student_id, subject_id, hoc_ky, diem_giua, diem_cuoi,
         diem_giua, diem_cuoi)
    )


def xoa(score_id):
    thuc_thi("DELETE FROM scores WHERE id = %s", (score_id,))
