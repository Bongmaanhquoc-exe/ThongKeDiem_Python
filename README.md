# Hệ thống Quản lý Điểm Sinh viên

Ứng dụng desktop viết bằng **Python + Tkinter**, kết nối **MySQL**, dành cho việc quản lý và thống kê điểm sinh viên.

---

## Chức năng

- Đăng nhập / phân quyền (admin, teacher, viewer)
- Quản lý sinh viên — thêm, sửa, xoá, tìm kiếm
- Quản lý lớp học và môn học
- Nhập điểm thi (giữa kỳ + cuối kỳ), tính điểm TB và xếp loại tự động
- Thống kê theo môn học, bảng xếp hạng GPA
- Xuất báo cáo ra file Excel
- Quản lý tài khoản người dùng (chỉ admin)

---

## Yêu cầu

| Phần mềm | Phiên bản |
|---|---|
| Python | 3.8 trở lên |
| MySQL Server | 8.0 trở lên |

---

## Cài đặt

### Bước 1 — Tải source code

```bash
git clone https://github.com/Bongmaanhquoc-exe/ThongKeDiem_Python.git
cd ThongKeDiem_Python
```

### Bước 2 — Cài thư viện Python

```bash
pip install -r requirements.txt
```

### Bước 3 — Tạo database MySQL

Mở MySQL và chạy lần lượt 2 file:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql
```

Hoặc mở bằng **MySQL Workbench**:
- File → Open SQL Script → chọn `database/schema.sql` → Execute
- Làm lại với `database/seed.sql`

### Bước 4 — Cấu hình kết nối database

Sao chép file mẫu và điền thông tin:

```bash
copy config.ini.example config.ini
```

Mở `config.ini` và sửa lại:

```ini
[database]
host     = localhost
port     = 3306
user     = root
password = mật_khẩu_mysql_của_bạn
name     = thongkediem
```

### Bước 5 — Chạy ứng dụng

```bash
python main.py
```

---

## Tài khoản mặc định

| Tên đăng nhập | Mật khẩu | Quyền |
|---|---|---|
| admin | 123456 | Toàn quyền |

---

## Cấu trúc thư mục

```
ThongKeDiem_Python/
├── main.py                  # Điểm khởi chạy
├── config.ini               # Cấu hình DB (không đưa lên Git)
├── config.ini.example       # File mẫu cấu hình
├── requirements.txt         # Danh sách thư viện
├── setup.bat                # Script cài đặt tự động (Windows)
│
├── app/
│   ├── database.py          # Kết nối MySQL
│   ├── models/              # Truy vấn dữ liệu (CRUD)
│   ├── services/            # Xử lý logic nghiệp vụ
│   ├── views/               # Giao diện Tkinter
│   └── utils/               # Tiện ích (bảo mật, xuất Excel)
│
├── database/
│   ├── schema.sql           # Script tạo bảng
│   └── seed.sql             # Dữ liệu mẫu
│
└── logs/                    # File log ứng dụng
```

---

## Công nghệ sử dụng

- **Python** — ngôn ngữ lập trình chính
- **Tkinter / ttk** — giao diện đồ họa
- **MySQL** — cơ sở dữ liệu
- **mysql-connector-python** — kết nối MySQL
- **openpyxl** — xuất file Excel
- **hashlib (SHA-256)** — mã hoá mật khẩu
