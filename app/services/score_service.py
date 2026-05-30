# ==============================================================
# score_service.py — Tính điểm trung bình và xếp loại
# ==============================================================

# Ngưỡng điểm để xếp loại (từ cao xuống thấp)
BANG_XEP_LOAI = [
    (9.0, 'A+'), (8.5, 'A'),
    (8.0, 'B+'), (7.0, 'B'),
    (6.5, 'C+'), (5.5, 'C'),
    (5.0, 'D+'), (4.0, 'D'),
    (0.0, 'F'),
]


def tinh_diem_tb(diem_giua_ky, diem_cuoi_ky):
    """Điểm TB = Giữa kỳ * 40% + Cuối kỳ * 60%"""
    return round(float(diem_giua_ky) * 0.4 + float(diem_cuoi_ky) * 0.6, 2)


def xep_loai(diem_tb):
    """Trả về ký hiệu xếp loại: A+, A, B+, B, C+, C, D+, D, F"""
    for nguong, loai in BANG_XEP_LOAI:
        if diem_tb >= nguong:
            return loai
    return 'F'


def tinh_gpa(student_id):
    """Tính GPA theo tín chỉ cho 1 sinh viên."""
    from app.models import score_model
    diem_list = score_model.lay_theo_sinh_vien(student_id)

    tong_tin_chi = sum(d['credits'] for d in diem_list)
    if tong_tin_chi == 0:
        return 0.0

    tong_diem = sum(
        tinh_diem_tb(d['midterm_score'], d['final_score']) * d['credits']
        for d in diem_list
    )
    return round(tong_diem / tong_tin_chi, 2)


def lay_diem_sinh_vien(student_id):
    """Lấy điểm sinh viên, tính thêm cột diem_tb và xep_loai."""
    from app.models import score_model
    rows = score_model.lay_theo_sinh_vien(student_id)
    for r in rows:
        r['diem_tb'] = tinh_diem_tb(r['midterm_score'], r['final_score'])
        r['xep_loai'] = xep_loai(r['diem_tb'])
    return rows
