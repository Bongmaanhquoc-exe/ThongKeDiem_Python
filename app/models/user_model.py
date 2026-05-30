# ==============================================================
# user_model.py — Truy vấn bảng users
# ==============================================================
from app.database import lay_nhieu, lay_mot, thuc_thi


def tim_theo_username(username):
    """Tìm user theo tên đăng nhập (chỉ lấy tài khoản đang kích hoạt)."""
    return lay_mot(
        "SELECT * FROM users WHERE username = %s AND is_active = 1",
        (username,)
    )


def lay_tat_ca():
    """Lấy toàn bộ danh sách tài khoản."""
    return lay_nhieu(
        "SELECT id, username, full_name, role, is_active, created_at "
        "FROM users ORDER BY id"
    )


def them(username, password_hash, full_name, role):
    """Thêm tài khoản mới, trả về id vừa tạo."""
    return thuc_thi(
        "INSERT INTO users (username, password_hash, full_name, role) "
        "VALUES (%s, %s, %s, %s)",
        (username, password_hash, full_name, role)
    )


def doi_mat_khau(user_id, password_hash_moi):
    thuc_thi(
        "UPDATE users SET password_hash = %s WHERE id = %s",
        (password_hash_moi, user_id)
    )


def doi_trang_thai(user_id, kich_hoat):
    """kich_hoat = True → mở khoá, False → khoá."""
    thuc_thi(
        "UPDATE users SET is_active = %s WHERE id = %s",
        (1 if kich_hoat else 0, user_id)
    )


def xoa(user_id):
    thuc_thi("DELETE FROM users WHERE id = %s", (user_id,))
