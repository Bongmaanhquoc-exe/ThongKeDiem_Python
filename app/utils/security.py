# ==============================================================
# security.py — Mã hoá mật khẩu bằng SHA-256
# ==============================================================
import hashlib


def ma_hoa(mat_khau):
    """Chuyển mật khẩu thô thành chuỗi hash SHA-256."""
    return hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()


def kiem_tra(mat_khau_nhap, hash_trong_db):
    """So sánh mật khẩu người dùng nhập với hash đã lưu."""
    return ma_hoa(mat_khau_nhap) == hash_trong_db
