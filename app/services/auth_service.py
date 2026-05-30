# ==============================================================
# auth_service.py — Xử lý đăng nhập và quản lý tài khoản
# ==============================================================
from app.models import user_model
from app.utils.security import ma_hoa, kiem_tra


def dang_nhap(username, password):
    """
    Kiểm tra username + password.
    Trả về dict user nếu hợp lệ.
    Ném ValueError nếu sai.
    """
    if not username.strip() or not password:
        raise ValueError("Vui lòng nhập đầy đủ tài khoản và mật khẩu")

    user = user_model.tim_theo_username(username.strip())
    if user is None:
        raise ValueError("Tài khoản không tồn tại hoặc đã bị khoá")

    if not kiem_tra(password, user['password_hash']):
        raise ValueError("Mật khẩu không đúng")

    return user


def tao_tai_khoan(username, password, ho_ten, role):
    """Tạo tài khoản mới. Ném ValueError nếu dữ liệu không hợp lệ."""
    if not username.strip():
        raise ValueError("Tên đăng nhập không được để trống")
    if not ho_ten.strip():
        raise ValueError("Họ tên không được để trống")
    if user_model.tim_theo_username(username.strip()):
        raise ValueError(f"Tên đăng nhập '{username}' đã tồn tại")
    if len(password) < 6:
        raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
    return user_model.them(username.strip(), ma_hoa(password), ho_ten.strip(), role)


def doi_mat_khau(user_id, mk_cu, mk_moi):
    """Người dùng tự đổi mật khẩu — cần nhập đúng mật khẩu cũ."""
    from app.database import lay_mot
    user = lay_mot("SELECT * FROM users WHERE id = %s", (user_id,))
    if not kiem_tra(mk_cu, user['password_hash']):
        raise ValueError("Mật khẩu cũ không đúng")
    if len(mk_moi) < 6:
        raise ValueError("Mật khẩu mới phải có ít nhất 6 ký tự")
    user_model.doi_mat_khau(user_id, ma_hoa(mk_moi))


def dat_lai_mat_khau(user_id, mk_moi):
    """Admin đặt lại mật khẩu cho người khác — không cần mật khẩu cũ."""
    if len(mk_moi) < 6:
        raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
    user_model.doi_mat_khau(user_id, ma_hoa(mk_moi))
