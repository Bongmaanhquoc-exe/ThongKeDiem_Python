# ==============================================================
# database.py — Kết nối MySQL và 3 hàm truy vấn dùng chung
# ==============================================================
import configparser
import os
import mysql.connector

# Đọc file config.ini một lần khi chương trình khởi động
_cfg = configparser.ConfigParser()
_cfg.read(
    os.path.join(os.path.dirname(__file__), '..', 'config.ini'),
    encoding='utf-8'
)


def ket_noi():
    """Tạo và trả về kết nối MySQL mới."""
    return mysql.connector.connect(
        host=_cfg.get('database', 'host',     fallback='localhost'),
        port=_cfg.getint('database', 'port',  fallback=3306),
        user=_cfg.get('database', 'user',     fallback='root'),
        password=_cfg.get('database', 'password', fallback=''),
        database=_cfg.get('database', 'name', fallback='thongkediem'),
        charset='utf8mb4'
    )


def lay_nhieu(sql, tham_so=()):
    """Chạy SELECT nhiều dòng — trả về list các dict."""
    conn = ket_noi()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, tham_so)
    ket_qua = cur.fetchall()
    cur.close()
    conn.close()
    return ket_qua


def lay_mot(sql, tham_so=()):
    """Chạy SELECT 1 dòng — trả về dict hoặc None."""
    conn = ket_noi()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, tham_so)
    ket_qua = cur.fetchone()
    cur.close()
    conn.close()
    return ket_qua


def thuc_thi(sql, tham_so=()):
    """Chạy INSERT / UPDATE / DELETE — trả về id của dòng vừa INSERT."""
    conn = ket_noi()
    cur = conn.cursor()
    cur.execute(sql, tham_so)
    conn.commit()
    id_moi = cur.lastrowid
    cur.close()
    conn.close()
    return id_moi
