# ==============================================================
# report_service.py — Thống kê báo cáo
# ==============================================================
from app.models import score_model, student_model
from app.services.score_service import tinh_diem_tb, xep_loai, tinh_gpa


def thong_ke_theo_mon(subject_id):
    """
    Thống kê kết quả thi của 1 môn học.
    Trả về dict chứa: tổng SV, điểm TB, cao nhất, thấp nhất,
                      tỉ lệ qua, phân bố xếp loại, danh sách chi tiết.
    """
    rows = score_model.lay_theo_mon(subject_id)
    if not rows:
        return None

    # Tính điểm TB cho từng sinh viên
    diem_tbs = [tinh_diem_tb(r['midterm_score'], r['final_score']) for r in rows]

    # Đếm phân bố xếp loại (A+, A, B+, ...)
    phan_bo = {}
    for dtb in diem_tbs:
        loai = xep_loai(dtb)
        phan_bo[loai] = phan_bo.get(loai, 0) + 1

    return {
        'tong_sv':    len(rows),
        'diem_tb':    round(sum(diem_tbs) / len(diem_tbs), 2),
        'cao_nhat':   max(diem_tbs),
        'thap_nhat':  min(diem_tbs),
        'ti_le_qua':  round(sum(1 for d in diem_tbs if d >= 5.0) / len(diem_tbs) * 100, 1),
        'phan_bo':    phan_bo,
        'chi_tiet':   rows,   # để hiển thị bảng chi tiết
    }


def bang_xep_hang(class_id=None):
    """
    Xếp hạng sinh viên theo GPA.
    class_id = None → xếp hạng toàn trường.
    """
    danh_sach = student_model.lay_tat_ca()

    # Lọc theo lớp nếu có
    if class_id:
        danh_sach = [s for s in danh_sach if s['class_id'] == class_id]

    # Tính GPA từng người
    ket_qua = []
    for sv in danh_sach:
        gpa = tinh_gpa(sv['id'])
        ket_qua.append({
            'ma_sv':    sv['student_code'],
            'ho_ten':   sv['full_name'],
            'ten_lop':  sv.get('ten_lop', ''),
            'gpa':      gpa,
            'xep_loai': xep_loai(gpa),
        })

    # Sắp xếp từ cao xuống thấp
    ket_qua.sort(key=lambda x: x['gpa'], reverse=True)

    # Gán thứ hạng
    for i, r in enumerate(ket_qua, 1):
        r['thu_hang'] = i

    return ket_qua
