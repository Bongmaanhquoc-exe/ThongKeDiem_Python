# TÀI LIỆU MÔ TẢ XÂY DỰNG ỨNG DỤNG
# Hệ thống Quản lý Điểm Sinh viên

---

## MỤC LỤC

1. [Giới thiệu đề tài](#1-giới-thiệu-đề-tài)
2. [Phân tích yêu cầu](#2-phân-tích-yêu-cầu)
3. [Thiết kế cơ sở dữ liệu](#3-thiết-kế-cơ-sở-dữ-liệu)
4. [Thiết kế kiến trúc ứng dụng](#4-thiết-kế-kiến-trúc-ứng-dụng)
5. [Xây dựng tầng Database](#5-xây-dựng-tầng-database)
6. [Xây dựng tầng Models](#6-xây-dựng-tầng-models)
7. [Xây dựng tầng Services](#7-xây-dựng-tầng-services)
8. [Xây dựng tầng Views](#8-xây-dựng-tầng-views)
9. [Chức năng phân quyền](#9-chức-năng-phân-quyền)
10. [Chức năng xuất Excel](#10-chức-năng-xuất-excel)
11. [Bảo mật mật khẩu](#11-bảo-mật-mật-khẩu)
12. [Cấu hình ứng dụng](#12-cấu-hình-ứng-dụng)
13. [Luồng chạy chương trình](#13-luồng-chạy-chương-trình)
14. [Kết quả và hướng phát triển](#14-kết-quả-và-hướng-phát-triển)

---

## 1. GIỚI THIỆU ĐỀ TÀI

### 1.1 Đặt vấn đề

Việc quản lý điểm sinh viên tại các trường đại học thường được thực hiện thủ công qua bảng tính Excel, dẫn đến nhiều bất cập:
- Khó tra cứu, tìm kiếm khi dữ liệu lớn
- Dễ xảy ra sai sót khi tính toán
- Không có phân quyền người dùng
- Khó tổng hợp báo cáo thống kê

### 1.2 Mục tiêu

Xây dựng ứng dụng desktop quản lý điểm sinh viên với các mục tiêu:
- Lưu trữ dữ liệu tập trung trên MySQL
- Giao diện đồ họa trực quan bằng Tkinter
- Phân quyền người dùng (admin / teacher / viewer)
- Tính toán điểm tự động, thống kê báo cáo
- Xuất báo cáo ra file Excel

### 1.3 Công nghệ sử dụng

| Thành phần | Công nghệ | Lý do chọn |
|---|---|---|
| Ngôn ngữ | Python 3 | Phổ biến, dễ học, nhiều thư viện |
| Giao diện | Tkinter / ttk | Có sẵn trong Python, không cần cài thêm |
| Cơ sở dữ liệu | MySQL 8.0 | Phổ biến, miễn phí, mạnh mẽ |
| Kết nối DB | mysql-connector-python | Thư viện chính thức của MySQL |
| Xuất Excel | openpyxl | Nhẹ, dễ dùng |
| Mã hoá | hashlib (SHA-256) | Có sẵn trong Python |

---

## 2. PHÂN TÍCH YÊU CẦU

### 2.1 Yêu cầu chức năng

| STT | Chức năng | Mô tả |
|---|---|---|
| 1 | Đăng nhập | Xác thực tài khoản bằng username + password |
| 2 | Quản lý sinh viên | Thêm, sửa, xoá, tìm kiếm sinh viên |
| 3 | Quản lý lớp học | CRUD lớp học / khoa |
| 4 | Quản lý môn học | CRUD môn học, số tín chỉ |
| 5 | Nhập điểm thi | Nhập điểm giữa kỳ và cuối kỳ |
| 6 | Tính điểm tự động | Tính điểm TB, xếp loại A+→F |
| 7 | Thống kê theo môn | Số SV, điểm TB, tỉ lệ qua môn |
| 8 | Bảng xếp hạng GPA | Xếp hạng SV theo GPA toàn khoá |
| 9 | Xuất Excel | Xuất bảng xếp hạng ra file .xlsx |
| 10 | Quản lý tài khoản | Tạo, khoá, đặt lại mật khẩu (admin) |

### 2.2 Yêu cầu phi chức năng

- **Bảo mật:** Mật khẩu được mã hoá SHA-256, không lưu plaintext
- **Phân quyền:** 3 cấp độ — admin, teacher, viewer
- **Cấu hình:** Thông tin kết nối DB tách riêng trong `config.ini`
- **Giao diện:** Trực quan, dễ sử dụng, có thông báo lỗi rõ ràng

### 2.3 Phân quyền người dùng

| Chức năng | Admin | Teacher | Viewer |
|---|---|---|---|
| Xem sinh viên / lớp / môn | ✅ | ✅ | ✅ |
| Thêm / Sửa / Xoá sinh viên | ✅ | ✅ | ❌ ẩn nút |
| Thêm / Sửa / Xoá lớp học | ✅ | ✅ | ❌ ẩn nút |
| Thêm / Sửa / Xoá môn học | ✅ | ✅ | ❌ ẩn nút |
| Nhập / Sửa / Xoá điểm | ✅ | ✅ | ❌ ẩn nút |
| Xem thống kê + xuất Excel | ✅ | ✅ | ✅ |
| Quản lý tài khoản | ✅ | ❌ ẩn menu | ❌ ẩn menu |

---

## 3. THIẾT KẾ CƠ SỞ DỮ LIỆU

### 3.1 Sơ đồ quan hệ (ERD)

```
classes          students              scores
--------         --------              --------
id (PK)    ←─── class_id (FK)         id (PK)
name             id (PK)         ┌──── student_id (FK)
faculty          student_code    │     subject_id (FK) ───┐
                 full_name       │     semester            │
                 dob             │     midterm_score       │
                 gender          │     final_score         │
                 email           │                         │
                 phone           │    subjects             │
                                 │    --------             │
users                            └──► id (PK) ◄────────────┘
--------                              subject_code
id (PK)                               name
username                              credits
password_hash
full_name
role
is_active
```

### 3.2 Mô tả các bảng

**Lý do thiết kế database theo dạng chuẩn hoá (normalized):**
- Tách `classes`, `students`, `subjects`, `scores` thành bảng riêng tránh lặp dữ liệu: tên lớp chỉ lưu 1 lần trong `classes`, không lặp ở từng dòng sinh viên.
- Khi đổi tên lớp chỉ cần cập nhật 1 dòng trong `classes` — tất cả sinh viên thuộc lớp đó tự động phản ánh đúng.
- Foreign Key + `ON DELETE CASCADE` / `SET NULL` giúp database tự giữ toàn vẹn dữ liệu khi xoá.

#### Bảng `classes` — Lớp học
```sql
CREATE TABLE classes (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE,  -- Tên lớp: CNTT01
    faculty    VARCHAR(150),                  -- Khoa / ngành
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Bảng `students` — Sinh viên
```sql
CREATE TABLE students (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20)  NOT NULL UNIQUE,  -- Mã SV: SV001
    full_name    VARCHAR(150) NOT NULL,
    dob          DATE,                          -- Ngày sinh
    gender       ENUM('Nam','Nữ','Khác'),
    email        VARCHAR(150),
    phone        VARCHAR(15),
    class_id     INT,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL
);
```

#### Bảng `subjects` — Môn học
```sql
CREATE TABLE subjects (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20)  NOT NULL UNIQUE,  -- Mã môn: IT101
    name         VARCHAR(150) NOT NULL,
    credits      TINYINT UNSIGNED NOT NULL DEFAULT 3
);
```

#### Bảng `scores` — Điểm thi
```sql
CREATE TABLE scores (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    student_id     INT NOT NULL,
    subject_id     INT NOT NULL,
    semester       VARCHAR(20) NOT NULL,        -- HK1-2024
    midterm_score  DECIMAL(4,2),               -- Điểm giữa kỳ
    final_score    DECIMAL(4,2),               -- Điểm cuối kỳ
    -- Mỗi SV chỉ có 1 bộ điểm / môn / học kỳ
    UNIQUE KEY (student_id, subject_id, semester),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);
```

**Lý do dùng `ON DELETE CASCADE` cho bảng `scores`:**
- Xoá một sinh viên thì tất cả điểm của sinh viên đó cũng xoá theo — tránh dữ liệu mồ côi (orphan records) trong bảng `scores` không còn liên kết đến sinh viên nào.

**Lý do dùng `UNIQUE KEY (student_id, subject_id, semester)` trong `scores`:**
- Một sinh viên chỉ có 1 bộ điểm / môn / học kỳ — ràng buộc này đảm bảo điều đó ở tầng database, không chỉ trong code ứng dụng.
- Là điều kiện tiên quyết để kỹ thuật `ON DUPLICATE KEY UPDATE` hoạt động đúng.

#### Bảng `users` — Tài khoản
```sql
CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    password_hash VARCHAR(64)  NOT NULL,  -- SHA-256 hash
    full_name     VARCHAR(150),
    role          ENUM('admin','teacher','viewer') DEFAULT 'teacher',
    is_active     TINYINT(1) NOT NULL DEFAULT 1
);
```

**Lý do dùng `is_active` thay vì xoá tài khoản:**
- Xoá tài khoản thật sự sẽ mất lịch sử — ai đã nhập dữ liệu gì? Dùng cờ `is_active = 0` để khoá tài khoản mà vẫn giữ audit trail.
- Dễ phục hồi nếu khoá nhầm: chỉ cần đặt lại `is_active = 1`.

---

## 4. THIẾT KẾ KIẾN TRÚC ỨNG DỤNG

### 4.1 Mô hình 3 tầng (3-Tier Architecture)

**Lý do chọn kiến trúc 3 tầng:**
- **Tách biệt trách nhiệm:** Mỗi tầng chỉ làm đúng việc của nó — View không biết SQL, Model không biết giao diện. Khi cần sửa giao diện không ảnh hưởng logic, khi đổi database không ảnh hưởng UI.
- **Dễ bảo trì:** Nếu công thức tính điểm thay đổi, chỉ sửa `score_service.py` — không phải tìm kiếm khắp các file View.
- **Tái sử dụng:** `score_service.tinh_diem_tb()` được gọi từ cả `score_view` (hiện realtime) lẫn `report_service` (thống kê), không cần viết lại.
- **Dễ kiểm thử:** Service và Model có thể test độc lập mà không cần mở cửa sổ Tkinter.

```
┌─────────────────────────────────────────┐
│           TẦNG GIAO DIỆN (Views)        │
│  login_view  │  student_view  │  ...    │
│  Hiển thị UI, nhận input từ người dùng  │
└─────────────────────┬───────────────────┘
                      │ gọi hàm
┌─────────────────────▼───────────────────┐
│          TẦNG NGHIỆP VỤ (Services)      │
│  auth_service  │  score_service  │ ...  │
│  Xử lý logic: tính điểm, kiểm tra...   │
└─────────────────────┬───────────────────┘
                      │ gọi hàm
┌─────────────────────▼───────────────────┐
│           TẦNG DỮ LIỆU (Models)         │
│  student_model  │  score_model  │  ...  │
│  Truy vấn SQL trực tiếp vào MySQL       │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│              MySQL Database              │
└─────────────────────────────────────────┘
```

### 4.2 Cấu trúc thư mục

**Lý do tổ chức thư mục theo tầng (`models/`, `services/`, `views/`):**
- Dễ tìm file: biết cần sửa logic tính điểm → vào `services/`, biết cần sửa giao diện → vào `views/`.
- Tránh file quá dài: mỗi màn hình một file riêng thay vì nhét tất cả vào `main.py`.
- `utils/` chứa các hàm không thuộc nghiệp vụ cụ thể (mã hoá, xuất Excel) — tái sử dụng nhiều nơi mà không tạo vòng phụ thuộc.

```
thongkediem/
├── main.py              ← Điểm khởi động ứng dụng
├── config.ini           ← Cấu hình DB (không đưa lên Git)
├── requirements.txt     ← Danh sách thư viện
│
├── app/
│   ├── database.py      ← Hàm kết nối + truy vấn dùng chung
│   │
│   ├── models/          ← Tầng dữ liệu
│   │   ├── user_model.py
│   │   ├── class_model.py
│   │   ├── student_model.py
│   │   ├── subject_model.py
│   │   └── score_model.py
│   │
│   ├── services/        ← Tầng nghiệp vụ
│   │   ├── auth_service.py
│   │   ├── score_service.py
│   │   └── report_service.py
│   │
│   ├── views/           ← Tầng giao diện
│   │   ├── bang_du_lieu.py   ← Widget bảng dùng chung
│   │   ├── login_view.py
│   │   ├── main_window.py
│   │   ├── student_view.py
│   │   ├── class_view.py
│   │   ├── subject_view.py
│   │   ├── score_view.py
│   │   ├── report_view.py
│   │   └── user_view.py
│   │
│   └── utils/           ← Tiện ích
│       ├── security.py  ← Mã hoá mật khẩu
│       └── exporter.py  ← Xuất Excel
│
└── database/
    ├── schema.sql       ← Script tạo bảng
    └── seed.sql         ← Dữ liệu mẫu
```

---

## 5. XÂY DỰNG TẦNG DATABASE

### 5.1 File `app/database.py`

> **Vị trí:** `thongkediem/app/database.py`

Đây là file trung tâm, cung cấp **4 hàm dùng chung** cho toàn bộ ứng dụng:

```python
import configparser, os, mysql.connector

# Đọc config.ini một lần khi khởi động
_cfg = configparser.ConfigParser()
_cfg.read('config.ini', encoding='utf-8')

def ket_noi():
    """Tạo kết nối MySQL mới từ config.ini"""
    return mysql.connector.connect(
        host=_cfg.get('database', 'host'),
        user=_cfg.get('database', 'user'),
        password=_cfg.get('database', 'password'),
        database=_cfg.get('database', 'name'),
        charset='utf8mb4'
    )

def lay_nhieu(sql, tham_so=()):
    """SELECT nhiều dòng → trả về list[dict]"""
    conn = ket_noi()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, tham_so)
    ket_qua = cur.fetchall()
    cur.close(); conn.close()
    return ket_qua

def lay_mot(sql, tham_so=()):
    """SELECT 1 dòng → trả về dict hoặc None"""
    conn = ket_noi()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, tham_so)
    ket_qua = cur.fetchone()
    cur.close(); conn.close()
    return ket_qua

def thuc_thi(sql, tham_so=()):
    """INSERT / UPDATE / DELETE → trả về lastrowid"""
    conn = ket_noi()
    cur = conn.cursor()
    cur.execute(sql, tham_so)
    conn.commit()
    id_moi = cur.lastrowid
    cur.close(); conn.close()
    return id_moi
```

**Lý do thiết kế như vậy:**
- Mỗi hàm tự mở và đóng kết nối → không bị rò rỉ kết nối
- Dùng `dictionary=True` → kết quả trả về dạng `{'column': value}` thay vì tuple
- Dùng `%s` placeholder thay vì nối chuỗi → chống SQL Injection
- Gọi `conn.commit()` sau mỗi lệnh ghi → đảm bảo dữ liệu được lưu

---

## 6. XÂY DỰNG TẦNG MODELS

### 6.1 Nguyên tắc

Mỗi file model tương ứng với **1 bảng** trong database. Mỗi model chứa các **hàm CRUD**:
- `lay_tat_ca()` — lấy toàn bộ dữ liệu
- `lay_theo_id(id)` — lấy 1 bản ghi theo ID
- `them(...)` — thêm mới
- `cap_nhat(id, ...)` — cập nhật
- `xoa(id)` — xoá

**Lý do tách mỗi bảng thành một file model riêng:**
- Mỗi file ngắn, dễ đọc — không phải cuộn qua hàng trăm dòng SQL không liên quan.
- Tìm đúng chỗ ngay lập tức: muốn sửa cách lấy dữ liệu sinh viên → mở `student_model.py`, không cần tìm trong file lớn.
- Nếu thêm bảng mới (vd: `departments`) chỉ cần thêm file `department_model.py` — không đụng chạm code cũ.

### 6.2 Ví dụ — `student_model.py`

> **Vị trí:** `thongkediem/app/models/student_model.py`

```python
from app.database import lay_nhieu, lay_mot, thuc_thi

def lay_tat_ca():
    # JOIN với bảng classes để lấy tên lớp
    return lay_nhieu(
        "SELECT s.*, c.name AS ten_lop "
        "FROM students s "
        "LEFT JOIN classes c ON s.class_id = c.id "
        "ORDER BY s.student_code"
    )

def tim_kiem(tu_khoa):
    kw = f"%{tu_khoa}%"
    return lay_nhieu(
        "SELECT s.*, c.name AS ten_lop FROM students s "
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
```

**Lý do dùng `LEFT JOIN` thay vì `JOIN` (INNER JOIN):**
- Sinh viên có thể chưa được xếp vào lớp nào (`class_id = NULL`). Nếu dùng INNER JOIN, những sinh viên đó sẽ bị ẩn hoàn toàn khỏi danh sách — đây là lỗi dữ liệu âm thầm khó phát hiện.
- LEFT JOIN giữ lại sinh viên chưa có lớp, chỉ để `ten_lop = NULL` — hiển thị trống trên giao diện, người dùng biết cần bổ sung.

**Lý do `tim_kiem` dùng `LIKE %tu_khoa%` (substring) thay vì `= tu_khoa` (exact match):**
- Người dùng thường chỉ nhớ một phần tên hoặc mã số — tìm "Nguy" phải ra "Nguyễn Văn A".
- Truyền tham số `%s` dạng placeholder thay vì nối chuỗi trực tiếp vào SQL để chống SQL Injection.

### 6.3 Kỹ thuật `ON DUPLICATE KEY UPDATE` trong `score_model`

> **Vị trí:** `thongkediem/app/models/score_model.py`

Khi nhập điểm, nếu sinh viên đã có điểm môn đó trong học kỳ đó thì **cập nhật**, ngược lại **thêm mới**:

**Lý do dùng `ON DUPLICATE KEY UPDATE` thay vì kiểm tra rồi INSERT/UPDATE riêng:**
- Tránh race condition: nếu dùng `SELECT` → `INSERT/UPDATE` riêng, có thể xảy ra 2 request cùng lúc đều thấy "chưa có" và cùng INSERT → lỗi duplicate.
- Gọn hơn: chỉ 1 lệnh SQL thay vì 2 lần round-trip đến database.
- Bảng `scores` đã có `UNIQUE KEY (student_id, subject_id, semester)` — MySQL tự phát hiện trùng và chuyển sang UPDATE.

```python
def them_hoac_cap_nhat(student_id, subject_id, hoc_ky, diem_giua, diem_cuoi):
    thuc_thi(
        "INSERT INTO scores (student_id, subject_id, semester, midterm_score, final_score) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE midterm_score = %s, final_score = %s",
        (student_id, subject_id, hoc_ky, diem_giua, diem_cuoi, diem_giua, diem_cuoi)
    )
```

---

## 7. XÂY DỰNG TẦNG SERVICES

### 7.1 `auth_service.py` — Xác thực người dùng

> **Vị trí:** `thongkediem/app/services/auth_service.py`

```python
def dang_nhap(username, password):
    user = user_model.tim_theo_username(username)
    if user is None:
        raise ValueError("Tài khoản không tồn tại")
    if not kiem_tra(password, user['password_hash']):
        raise ValueError("Mật khẩu không đúng")
    return user

def tao_tai_khoan(username, password, ho_ten, role):
    if user_model.tim_theo_username(username):
        raise ValueError(f"Tên đăng nhập '{username}' đã tồn tại")
    if len(password) < 6:
        raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
    return user_model.them(username, ma_hoa(password), ho_ten, role)

def dat_lai_mat_khau(user_id, mk_moi):
    # Admin đặt lại MK cho người khác — KHÔNG cần biết MK cũ
    if len(mk_moi) < 6:
        raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
    user_model.doi_mat_khau(user_id, ma_hoa(mk_moi))
```

**Nguyên tắc:** Ném `ValueError` thay vì trả về `None/False` → tầng View chỉ cần `try/except` là bắt được lỗi kèm thông báo cụ thể.

**Tách biệt 2 luồng đổi mật khẩu:**
- `doi_mat_khau(user_id, mk_cu, mk_moi)` — người dùng tự đổi, phải nhập đúng mật khẩu cũ
- `dat_lai_mat_khau(user_id, mk_moi)` — admin đặt lại, không cần mật khẩu cũ

### 7.2 `score_service.py` — Tính điểm

> **Vị trí:** `thongkediem/app/services/score_service.py`

```python
BANG_XEP_LOAI = [
    (9.0, 'A+'), (8.5, 'A'), (8.0, 'B+'), (7.0, 'B'),
    (6.5, 'C+'), (5.5, 'C'), (5.0, 'D+'), (4.0, 'D'), (0.0, 'F'),
]

def tinh_diem_tb(diem_giua_ky, diem_cuoi_ky):
    # Giữa kỳ 40% + Cuối kỳ 60%
    return round(diem_giua_ky * 0.4 + diem_cuoi_ky * 0.6, 2)

def xep_loai(diem_tb):
    for nguong, loai in BANG_XEP_LOAI:
        if diem_tb >= nguong:
            return loai
    return 'F'

def tinh_gpa(student_id):
    diem_list = score_model.lay_theo_sinh_vien(student_id)
    tong_tin_chi = sum(d['credits'] for d in diem_list)
    if tong_tin_chi == 0:
        return 0.0
    tong_diem = sum(
        tinh_diem_tb(d['midterm_score'], d['final_score']) * d['credits']
        for d in diem_list
    )
    return round(tong_diem / tong_tin_chi, 2)
```

**Lý do dùng công thức 40% giữa kỳ + 60% cuối kỳ:**
- Đây là tỉ lệ phổ biến tại nhiều trường đại học Việt Nam. Cuối kỳ quan trọng hơn vì kiểm tra toàn bộ kiến thức môn học.
- Hàm `tinh_diem_tb` được tách riêng để nếu trường thay đổi tỉ lệ (vd: 30/70) chỉ cần sửa 1 chỗ — tất cả nơi gọi hàm tự cập nhật.

**Lý do dùng bảng `BANG_XEP_LOAI` (list of tuples) thay vì chuỗi `if/elif`:**
- Dễ thêm/bớt/đổi ngưỡng xếp loại mà không cần sửa logic — chỉ chỉnh giá trị trong list.
- Vòng lặp dừng ở ngưỡng đầu tiên thoả điều kiện `diem_tb >= nguong` → không cần kiểm tra khoảng chồng lấp.

**Công thức GPA theo tín chỉ:**

```
GPA = Σ (Điểm TB môn × Số tín chỉ môn) / Σ Số tín chỉ
```

**Lý do dùng GPA theo tín chỉ thay vì trung bình cộng đơn giản:**
- Môn nhiều tín chỉ (4 TC) quan trọng hơn môn ít tín chỉ (2 TC) — cần có trọng số.
- Đây là chuẩn tính GPA quốc tế (weighted GPA), phản ánh đúng năng lực học tập của sinh viên hơn.

### 7.3 `report_service.py` — Thống kê

> **Vị trí:** `thongkediem/app/services/report_service.py`

```python
def thong_ke_theo_mon(subject_id):
    rows = score_model.lay_theo_mon(subject_id)
    diem_tbs = [tinh_diem_tb(r['midterm_score'], r['final_score']) for r in rows]
    return {
        'tong_sv':   len(rows),
        'diem_tb':   round(sum(diem_tbs) / len(diem_tbs), 2),
        'cao_nhat':  max(diem_tbs),
        'thap_nhat': min(diem_tbs),
        'ti_le_qua': round(sum(1 for d in diem_tbs if d >= 5.0) / len(diem_tbs) * 100, 1),
    }
```

**Lý do đặt logic thống kê trong Service thay vì truy vấn SQL thuần:**
- Công thức `tinh_diem_tb` đã được định nghĩa sẵn trong `score_service` — gọi lại để đảm bảo nhất quán, không viết lại công thức 40/60 trong SQL.
- Python dễ viết và đọc hơn SQL aggregate phức tạp (vd: tính tỉ lệ qua môn trong SQL cần `CASE WHEN` lồng nhau).
- Nếu sau này đổi ngưỡng "qua môn" từ 5.0 thành 4.0, chỉ sửa 1 chỗ trong service.

---

## 8. XÂY DỰNG TẦNG VIEWS

### 8.1 Widget dùng chung — `BangDuLieu`

> **Vị trí:** `thongkediem/app/views/bang_du_lieu.py`

Thay vì viết lại Treeview ở mỗi màn hình, tạo 1 class dùng chung:

```python
class BangDuLieu(ttk.Frame):
    def __init__(self, master, cac_cot):
        # cac_cot: [('key', 'Tiêu đề', độ_rộng), ...]
        self._tree = ttk.Treeview(self, columns=[c[0] for c in cac_cot], show='headings')
        for key, tieu_de, do_rong in cac_cot:
            self._tree.heading(key, text=tieu_de)
            self._tree.column(key, width=do_rong)

    def hien_du_lieu(self, du_lieu):
        self._tree.delete(*self._tree.get_children())
        for i, dong in enumerate(du_lieu):
            gia_tri = [dong.get(k, '') for k in self._cac_key]
            self._tree.insert('', 'end', iid=str(i), values=gia_tri)

    def lay_dong_chon(self):
        chon = self._tree.selection()
        if not chon:
            return None
        return self._du_lieu[int(chon[0])]
```

**Lý do tạo class `BangDuLieu` dùng chung thay vì viết Treeview trực tiếp ở mỗi màn hình:**
- Có 6 màn hình đều cần bảng dữ liệu — nếu viết lại mỗi lần thì 6 chỗ cần sửa khi có thay đổi (vd: thêm scrollbar, đổi font).
- Đóng gói `hien_du_lieu()` và `lay_dong_chon()` vào class giúp tất cả màn hình dùng chung giao tiếp nhất quán.
- Giảm lỗi: logic "xoá hết rồi điền lại" (`delete` → `insert`) chỉ viết 1 lần, không bị viết sai ở nơi nào đó.

### 8.2 Cấu trúc mỗi màn hình CRUD

Mỗi màn hình đều theo cùng 1 cấu trúc:

```
┌─────────────────────────────────────────────┐
│            TIÊU ĐỀ MÀN HÌNH                 │
├─────────────────────────────────────────────┤
│  [+ Thêm]  [✎ Sửa]  [✕ Xoá]   [Tìm] [🔍]  │  ← Toolbar
│  (ẩn 3 nút này nếu role = viewer)           │
├─────────────────────────────────────────────┤
│                                             │
│           BẢNG DỮ LIỆU                     │  ← BangDuLieu widget
│           (Treeview + Scrollbar)            │
│                                             │
└─────────────────────────────────────────────┘
```

**Lý do tất cả màn hình CRUD đều có cùng bố cục:**
- Người dùng học cách dùng một màn hình là biết dùng tất cả — giảm thời gian làm quen.
- Khi thêm màn hình mới (vd: quản lý khoa), chỉ cần copy cấu trúc và đổi dữ liệu, không phải thiết kế lại từ đầu.

**Cách ẩn nút theo role:**

> **Áp dụng trong:** `thongkediem/app/views/student_view.py`, `class_view.py`, `subject_view.py`, `score_view.py`

```python
# Áp dụng ở tất cả các view: student, class, subject, score
if self.user.get('role') != 'viewer':
    ttk.Button(toolbar, text="+ Thêm", command=self._them).pack(side='left')
    ttk.Button(toolbar, text="✎ Sửa",  command=self._sua).pack(side='left')
    ttk.Button(toolbar, text="✕ Xoá",  command=self._xoa).pack(side='left')
# Viewer chỉ thấy thanh toolbar trống hoặc ô tìm kiếm
```

### 8.3 Pattern Form Thêm / Sửa

> **Ví dụ trong:** `thongkediem/app/views/student_view.py` (class `FormSinhVien`)
> Tương tự áp dụng trong: `class_view.py`, `subject_view.py`, `score_view.py`, `user_view.py`

Tất cả form đều dùng chung pattern:

```python
class FormSinhVien(tk.Toplevel):
    def __init__(self, master, sinh_vien=None, on_luu=None):
        # sinh_vien = None  → chế độ Thêm mới
        # sinh_vien = {...} → chế độ Sửa, điền sẵn dữ liệu
        self.sinh_vien = sinh_vien
        self.on_luu = on_luu   # callback để reload bảng sau khi lưu
        ...

    def _kiem_tra(self, d):
        import re
        if not d['ma_sv']:
            raise ValueError("Mã sinh viên không được để trống")
        if not d['ho_ten']:
            raise ValueError("Họ tên không được để trống")
        # Validate định dạng ngày sinh YYYY-MM-DD trước khi gửi MySQL
        if d['ngay_sinh']:
            from datetime import datetime
            try:
                datetime.strptime(d['ngay_sinh'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Ngày sinh sai định dạng! Dùng: YYYY-MM-DD (vd: 2003-05-21)")
        # Validate email
        if d['email']:
            if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', d['email']):
                raise ValueError("Email không hợp lệ\nVí dụ: sinhvien@example.com")
        # Validate số điện thoại
        if d['sdt']:
            sdt_chuan = re.sub(r'\s+', '', d['sdt'])
            if not re.match(r'^(0|\+84)[0-9]{8,10}$', sdt_chuan):
                raise ValueError("Số điện thoại không hợp lệ\nVui lòng nhập 9–11 chữ số, bắt đầu bằng 0 hoặc +84")

    def _luu(self):
        try:
            d = self._lay_du_lieu_form()
            self._kiem_tra(d)           # validate trước khi gửi DB
            if self.sinh_vien is None:
                student_model.them(...)  # Thêm mới
            else:
                student_model.cap_nhat(...)  # Cập nhật
            self.on_luu()   # reload bảng
            self.destroy()
        except ValueError as loi:
            messagebox.showerror("Lỗi", str(loi))  # hiện thông báo rõ ràng
```

**Lý do validate tại View trước khi gửi DB:**
MySQL sẽ trả về lỗi `DataError: Incorrect date value` nếu định dạng sai. Validate sớm tại View giúp hiện thông báo thân thiện thay vì lỗi kỹ thuật.

**Quy tắc validate thông tin liên hệ:**
- **Email:** kiểm tra định dạng `xxx@xxx.xxx` bằng regex; trường tùy chọn — chỉ validate khi có nhập
- **Số điện thoại:** phải bắt đầu bằng `0` hoặc `+84`, tổng 9–11 chữ số; trường tùy chọn — chỉ validate khi có nhập; khoảng trắng được loại bỏ trước khi kiểm tra

### 8.4 Màn hình Nhập điểm — Tính điểm realtime

> **Vị trí:** `thongkediem/app/views/score_view.py`

Khi người dùng đang gõ điểm, ứng dụng tính điểm TB ngay lập tức:

```python
self.o_gk.bind('<KeyRelease>', self._tinh_thu)
self.o_ck.bind('<KeyRelease>', self._tinh_thu)

def _tinh_thu(self, _=None):
    try:
        gk = float(self.o_gk.get())
        ck = float(self.o_ck.get())
        tb = score_service.tinh_diem_tb(gk, ck)
        loai = score_service.xep_loai(tb)
        self.lbl_tb.config(text=f"{tb}  →  {loai}")
    except ValueError:
        self.lbl_tb.config(text="—")
```

**Combobox vừa gõ vừa chọn (autocomplete):**

Các combo `Sinh viên` và `Môn học` trong màn hình Nhập điểm, cùng với combo `Môn học` và `Lớp` trong Thống kê, đều hỗ trợ vừa gõ vừa chọn. Khi người dùng gõ, danh sách tự lọc theo từ khóa và dropdown tự mở ra để gợi ý:

```python
self.combo_sv.bind('<KeyRelease>', self._loc_sv)

def _loc_sv(self, _=None):
    tu_khoa = self.combo_sv.get().lower()
    tat_ca = list(self.sv_map.keys())
    loc = [s for s in tat_ca if tu_khoa in s.lower()] if tu_khoa else tat_ca
    self.combo_sv['values'] = loc
    if loc:
        self.combo_sv.event_generate('<Down>')
    self._hien_diem_sv()  # cập nhật bảng điểm nếu khớp chính xác
```

Tìm kiếm không phân biệt hoa/thường và khớp theo chuỗi con (substring).

**Khoá combo Môn học khi Sửa điểm:**

Khi mở form ở chế độ Sửa, combo Môn học bị disable để tránh người dùng đổi sang môn khác (sẽ tạo record mới thay vì cập nhật):

```python
# Trong FormNhapDiem.__init__
if diem:
    self._dien_du_lieu()
    self.combo_mon.config(state='disabled')  # chỉ sửa được điểm số
```

**Nút làm mới danh sách (🔄):**

Danh sách sinh viên trong màn hình Nhập điểm được load lại khi nhấn nút 🔄, tránh trường hợp thêm sinh viên mới nhưng combo không cập nhật:

```python
def _lam_moi_sv(self):
    svien = student_model.lay_tat_ca()
    self.sv_map = {f"{s['student_code']} — {s['full_name']}": s['id'] for s in svien}
    self.combo_sv['values'] = list(self.sv_map.keys())
```

Tương tự, màn hình Thống kê cũng có nút 🔄 để làm mới combo Môn học và Lớp.

### 8.6 Thanh tìm kiếm trong màn hình CRUD

> **Vị trí:** `thongkediem/app/views/subject_view.py`, `thongkediem/app/views/class_view.py`

Các màn hình Quản lý Môn học và Quản lý Lớp học có thanh tìm kiếm lọc dữ liệu trực tiếp trên client (không truy vấn lại DB):

```
┌─────────────────────────────────────────────┐
│            TIÊU ĐỀ MÀN HÌNH                 │
├─────────────────────────────────────────────┤
│  [+ Thêm]  [✎ Sửa]  [✕ Xoá]               │  ← Toolbar
├─────────────────────────────────────────────┤
│  Tìm kiếm: [________________] [✕]           │  ← Thanh tìm kiếm
├─────────────────────────────────────────────┤
│           BẢNG DỮ LIỆU                     │
└─────────────────────────────────────────────┘
```

```python
def _tai_du_lieu(self):
    self._du_lieu_goc = subject_model.lay_tat_ca()  # lưu toàn bộ để lọc lại
    self._loc_va_hien(self.o_tim.get() if hasattr(self, 'o_tim') else '')

def _loc_va_hien(self, tu_khoa):
    tu_khoa = tu_khoa.strip().lower()
    if tu_khoa:
        ds = [m for m in self._du_lieu_goc
              if tu_khoa in m['subject_code'].lower()
              or tu_khoa in m['name'].lower()]
    else:
        ds = self._du_lieu_goc
    self.bang.hien_du_lieu(ds)
```

- Lọc theo **nhiều trường** (mã môn + tên môn; tên lớp + khoa/ngành)
- Nút **✕** xóa ô tìm kiếm và hiện lại toàn bộ danh sách
- Sau khi Thêm/Sửa/Xoá, dữ liệu làm mới và giữ nguyên từ khóa đang tìm

**Lý do lọc trên client (Python) thay vì gọi lại DB mỗi lần gõ:**
- Dữ liệu môn học và lớp học thường ít (vài chục đến vài trăm dòng) — load một lần vào `_du_lieu_goc` là đủ, không cần truy vấn liên tục.
- Lọc local nhanh hơn và không tạo nhiều kết nối MySQL khi người dùng đang gõ từng ký tự.
- Ngược lại, màn hình Sinh viên dùng `tim_kiem()` gọi DB vì số lượng sinh viên có thể rất lớn, load toàn bộ vào bộ nhớ sẽ tốn tài nguyên.

### 8.5 Luồng điều hướng (Navigation)

> **Liên quan:** `thongkediem/main.py`, `thongkediem/app/views/login_view.py`, `thongkediem/app/views/main_window.py`

```
main.py
  │
  └── LoginView (Toplevel)
        │ đăng nhập thành công
        └── MainWindow (Toplevel)
              │  protocol("WM_DELETE_WINDOW") → _thoat() → root.destroy()
              │
              ├── [Sinh viên]  → SinhVienView (Frame)
              ├── [Lớp học]    → LopHocView (Frame)
              ├── [Môn học]    → MonHocView (Frame)
              ├── [Nhập điểm] → NhapDiemView (Frame)
              ├── [Thống kê]  → ThongKeView (Frame)
              └── [Tài khoản] → TaiKhoanView (Frame)  ← chỉ admin
```

**Xử lý thoát ứng dụng đúng cách:**

> **Vị trí:** `thongkediem/app/views/main_window.py`

`MainWindow` là `Toplevel` — con của `root` ẩn. Nếu không bắt sự kiện đóng cửa sổ, nhấn X chỉ đóng `Toplevel` nhưng `root.mainloop()` vẫn chạy ngầm. Giải pháp:

```python
class MainWindow(tk.Toplevel):
    def __init__(self, root, user):
        self.root = root
        self.protocol("WM_DELETE_WINDOW", self._thoat)

    def _thoat(self):
        self.root.destroy()  # huỷ root → mainloop() kết thúc → thoát hẳn
```

---

## 9. CHỨC NĂNG PHÂN QUYỀN

### 9.1 Cách triển khai

Phân quyền được kiểm tra tại **tầng View** theo 2 cấp:

**Lý do kiểm tra quyền ở tầng View (ẩn nút) thay vì chặn ở Service:**
- Mục tiêu là **UX rõ ràng** — người dùng không thấy nút thì không nhầm lẫn, thay vì nhấn nút rồi nhận thông báo lỗi.
- Ứng dụng desktop chạy local, không có HTTP request từ bên ngoài — không cần bảo vệ nhiều lớp như web API.
- Nếu cần nâng cấp lên web sau này, việc thêm kiểm tra quyền ở Service/Model là bước tiếp theo, không mâu thuẫn với thiết kế hiện tại.

**Cấp 1 — Ẩn menu Tài khoản (chỉ admin thấy):**

> **Vị trí:** `thongkediem/app/views/main_window.py`

```python
# main_window.py
cac_menu = [("Sinh viên", ...), ("Nhập điểm", ...), ...]
if self.user['role'] == 'admin':
    cac_menu.append(("Tài khoản", ...))
```

**Cấp 2 — Ẩn nút Thêm/Sửa/Xoá (viewer không thấy):**

> **Áp dụng trong:** `thongkediem/app/views/student_view.py`, `class_view.py`, `subject_view.py`, `score_view.py`

```python
# Áp dụng trong: student_view, class_view, subject_view, score_view
if self.user.get('role') != 'viewer':
    ttk.Button(toolbar, text="+ Thêm", command=self._them).pack(side='left')
    ttk.Button(toolbar, text="✎ Sửa",  command=self._sua).pack(side='left')
    ttk.Button(toolbar, text="✕ Xoá",  command=self._xoa).pack(side='left')
```

**Bảo vệ tài khoản đang đăng nhập:**

> **Vị trí:** `thongkediem/app/views/user_view.py`

```python
# user_view.py — admin không thể tự xoá tài khoản mình đang dùng
def _xoa(self):
    if dong['id'] == self.user_hien_tai['id']:
        messagebox.showerror("Không thể xoá",
            "Bạn không thể xoá tài khoản đang dùng để đăng nhập.")
        return
```

**Đặt lại mật khẩu (admin):**

> **Vị trí:** `thongkediem/app/views/user_view.py` (class `FormDoiMatKhau`)

Admin có thể đặt lại mật khẩu cho bất kỳ tài khoản nào mà **không cần biết mật khẩu cũ**. Form yêu cầu nhập mật khẩu mới 2 lần để xác nhận:

```python
# FormDoiMatKhau trong user_view.py
def _luu(self):
    if self.o_moi.get() != self.o_xn.get():
        messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp.")
        return
    auth_service.dat_lai_mat_khau(self.user_id, self.o_moi.get())
```

### 9.2 3 cấp độ quyền

| Role | Mô tả | Được làm |
|---|---|---|
| **admin** | Quản trị viên | Toàn quyền + quản lý tài khoản |
| **teacher** | Giáo viên | Xem + nhập/sửa dữ liệu và điểm |
| **viewer** | Người xem | Chỉ xem dữ liệu và thống kê |

---

## 10. CHỨC NĂNG XUẤT EXCEL

Sử dụng thư viện **openpyxl** để tạo file `.xlsx`. Khi xuất, ứng dụng mở hộp thoại **Save As** để người dùng tự chọn thư mục và tên file:

> **Vị trí:** `thongkediem/app/utils/exporter.py`

```python
from tkinter import filedialog

def xuat_excel(du_lieu, ten_file='ket_qua.xlsx', ten_cot=None):
    # Mở hộp thoại Save As
    duong_dan = filedialog.asksaveasfilename(
        defaultextension='.xlsx',
        filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')],
        initialfile=ten_file,
        title='Chọn nơi lưu file Excel',
    )
    if not duong_dan:
        return None   # người dùng nhấn Cancel

    wb = openpyxl.Workbook()
    ws = wb.active

    # Tạo hàng tiêu đề với nền xanh đậm, chữ trắng
    headers = list(du_lieu[0].keys())
    for col, key in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=(ten_cot or {}).get(key, key))
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='2C3E50')
        cell.alignment = Alignment(horizontal='center')

    # Điền dữ liệu từ dòng 2
    for row_idx, dong in enumerate(du_lieu, 2):
        for col_idx, key in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=dong.get(key, ''))

    # Tự chỉnh độ rộng cột
    for col in ws.columns:
        do_rong = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(do_rong + 4, 40)

    wb.save(duong_dan)
    return duong_dan
```

**Hàm trả về `None` nếu người dùng huỷ** — tầng View kiểm tra trước khi hiện thông báo thành công.

**Lý do mở hộp thoại Save As thay vì lưu tự động vào thư mục cố định:**
- Người dùng muốn kiểm soát nơi lưu file — đặt tên theo học kỳ, chọn thư mục Desktop hay USB.
- Tránh ghi đè file cũ không có cảnh báo nếu lưu tự động vào cùng đường dẫn.

**Lý do dùng `openpyxl` thay vì `csv`:**
- CSV không có định dạng (không in đậm tiêu đề, không căn chỉnh cột) — file đẹp hơn khi mở bằng Excel/LibreOffice.
- `openpyxl` cho phép tô màu tiêu đề, tự chỉnh độ rộng cột — tăng tính chuyên nghiệp của báo cáo.

---

## 11. BẢO MẬT MẬT KHẨU

### 11.1 Vấn đề

Không bao giờ lưu mật khẩu dạng plaintext vào database. Nếu database bị lộ, mật khẩu người dùng vẫn an toàn.

**Lý do không lưu plaintext:**
- Nếu file backup database bị lấy cắp hay người quản trị tò mò nhìn vào, họ thấy ngay mật khẩu thật của mọi người.
- Người dùng thường dùng lại mật khẩu cho nhiều dịch vụ (email, ngân hàng...) — lộ mật khẩu ứng dụng nhỏ dẫn đến nguy cơ cho các tài khoản quan trọng hơn.

### 11.2 Giải pháp — SHA-256 Hash

> **Vị trí:** `thongkediem/app/utils/security.py`

**Lý do dùng SHA-256 thay vì MD5 hay bcrypt:**
- MD5 đã bị bẻ khóa bằng rainbow table — không còn an toàn cho mật khẩu.
- bcrypt an toàn hơn SHA-256 (có salt, slow by design) nhưng cần cài thêm thư viện và phức tạp hơn — SHA-256 là lựa chọn hợp lý cho ứng dụng học tập nội bộ.
- SHA-256 có sẵn trong thư viện chuẩn Python (`hashlib`) — không cần cài thêm.

```python
import hashlib

def ma_hoa(mat_khau):
    return hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()

def kiem_tra(mat_khau_nhap, hash_trong_db):
    return ma_hoa(mat_khau_nhap) == hash_trong_db
```

### 11.3 Minh hoạ

```
Người dùng nhập:  "123456"
             ↓  SHA-256
Lưu vào DB:  "8d969eef6ecad3c29a3a629280e686..."  (64 ký tự hex)

Khi đăng nhập:
  SHA-256("123456") == hash_trong_db?  → True → Cho vào
  SHA-256("sai")    == hash_trong_db?  → False → Từ chối
```

---

## 12. CẤU HÌNH ỨNG DỤNG

### 12.1 Vấn đề

Không hardcode thông tin kết nối database trong code → khi triển khai ở máy khác chỉ cần sửa file config, không cần sửa code.

**Lý do dùng `config.ini` thay vì hardcode hay biến môi trường:**
- Hardcode (`host = "localhost"`, `password = "123456"` trong code) khiến mỗi máy khác nhau phải sửa code — dễ commit nhầm mật khẩu lên Git.
- `config.ini` được thêm vào `.gitignore` nên không bao giờ bị đẩy lên repository — thông tin nhạy cảm ở lại local.
- Dễ đọc hơn biến môi trường đối với người mới: mở file ra là thấy ngay cần điền gì, không cần biết cách set `$env:DB_PASSWORD`.

### 12.2 File `config.ini`

> **Vị trí:** `thongkediem/config.ini` (không đưa lên Git — xem `config.ini.example` để tham khảo)

```ini
[database]
host     = localhost
port     = 3306
user     = root
password = 123456
name     = thongkediem
```

### 12.3 Đọc config trong code

> **Vị trí:** `thongkediem/app/database.py` (phần đầu file)

```python
import configparser
cfg = configparser.ConfigParser()
cfg.read('config.ini', encoding='utf-8')

host = cfg.get('database', 'host', fallback='localhost')
port = cfg.getint('database', 'port', fallback=3306)
```

Dùng `fallback` để có giá trị mặc định nếu key không tồn tại.

---

## 13. LUỒNG CHẠY CHƯƠNG TRÌNH

> **Điểm khởi động:** `thongkediem/main.py`

```
python main.py
     │
     ├─ Tạo root = tk.Tk() (ẩn)
     ├─ Hiện LoginView
     │
     │  [Người dùng nhập username + password]
     │       │
     │       ├─ auth_service.dang_nhap()
     │       │       │
     │       │       ├─ user_model.tim_theo_username()  → truy vấn DB
     │       │       ├─ security.kiem_tra(password, hash)
     │       │       └─ Trả về dict user nếu đúng
     │       │
     │  [Đăng nhập thành công]
     │       │
     │       └─ Mở MainWindow
     │               │
     │               ├─ Hiện sidebar menu (ẩn "Tài khoản" nếu không phải admin)
     │               │
     │               └─ [Người dùng click menu]
     │                       │
     │                       ├─ Sinh viên  → student_model.lay_tat_ca() → hiện bảng
     │                       ├─ Nhập điểm → score_service.lay_diem_sinh_vien()
     │                       ├─ Thống kê  → report_service.thong_ke_theo_mon()
     │                       └─ ...
     │
     └─ root.mainloop()  ← chờ sự kiện cho đến khi đóng cửa sổ
```

---

## 14. KẾT QUẢ VÀ HƯỚNG PHÁT TRIỂN

### 14.1 Kết quả đạt được

| Chức năng | Trạng thái | Ghi chú |
|---|---|---|
| Đăng nhập / thoát đúng cách | ✅ Hoàn thành | WM_DELETE_WINDOW → root.destroy() |
| CRUD Sinh viên | ✅ Hoàn thành | Validate ngày sinh, email, SDT |
| CRUD Lớp học | ✅ Hoàn thành | Có thanh tìm kiếm theo tên lớp / khoa |
| CRUD Môn học | ✅ Hoàn thành | Có thanh tìm kiếm theo mã môn / tên môn |
| Validate thông tin liên hệ SV | ✅ Hoàn thành | Email regex, SDT 9–11 số bắt đầu 0/+84 |
| Nhập điểm thi | ✅ Hoàn thành | Tính điểm TB realtime khi gõ |
| Combobox vừa gõ vừa chọn | ✅ Hoàn thành | Sinh viên, Môn học, Lớp — lọc theo từ khóa |
| Khoá môn khi sửa điểm | ✅ Hoàn thành | Tránh tạo record trùng |
| Nút 🔄 làm mới danh sách | ✅ Hoàn thành | score_view, report_view |
| Tính điểm TB + xếp loại | ✅ Hoàn thành | Công thức 40% + 60% |
| Tính GPA theo tín chỉ | ✅ Hoàn thành | |
| Thống kê theo môn | ✅ Hoàn thành | Tổng SV, TB, tỉ lệ qua |
| Bảng xếp hạng GPA | ✅ Hoàn thành | Lọc theo lớp |
| Xuất Excel (Save As) | ✅ Hoàn thành | Hộp thoại chọn nơi lưu, huỷ được |
| Phân quyền 3 cấp (UI) | ✅ Hoàn thành | Ẩn nút theo role tại View |
| Quản lý tài khoản | ✅ Hoàn thành | Chỉ admin, chặn tự xoá |
| Đặt lại mật khẩu (admin) | ✅ Hoàn thành | Không cần MK cũ, xác nhận 2 lần |
| Bảo mật mật khẩu SHA-256 | ✅ Hoàn thành | |

### 14.2 Hướng phát triển

- Thêm biểu đồ thống kê bằng `matplotlib`
- Xuất báo cáo dạng PDF bằng `reportlab`
- Triển khai web bằng Flask / Django
- Thêm tính năng nhập điểm hàng loạt từ file Excel
- Gửi thông báo điểm qua email tự động
