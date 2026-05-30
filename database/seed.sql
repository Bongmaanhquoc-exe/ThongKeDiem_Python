-- ============================================================
-- Dữ liệu mẫu để test ứng dụng
-- Chạy: mysql -u root -p < database/seed.sql
-- ============================================================

USE thongkediem;

-- Lớp học
INSERT IGNORE INTO classes (name, faculty) VALUES
    ('CNTT01', 'Công nghệ Thông tin'),
    ('CNTT02', 'Công nghệ Thông tin'),
    ('KT01',   'Kế toán - Tài chính'),
    ('QT01',   'Quản trị Kinh doanh');

-- Môn học
INSERT IGNORE INTO subjects (subject_code, name, credits) VALUES
    ('IT101', 'Nhập môn Lập trình',       3),
    ('IT102', 'Cấu trúc Dữ liệu',         3),
    ('IT103', 'Cơ sở Dữ liệu',            3),
    ('IT201', 'Lập trình Python',          3),
    ('MA101', 'Toán Cao cấp A1',          4),
    ('EN101', 'Tiếng Anh Tổng hợp 1',     3);

-- Sinh viên mẫu
INSERT IGNORE INTO students (student_code, full_name, dob, gender, email, class_id) VALUES
    ('SV001', 'Nguyễn Văn An',   '2003-05-10', 'Nam', 'an.nv@email.com', 1),
    ('SV002', 'Trần Thị Bình',   '2003-08-22', 'Nữ',  'binh.tt@email.com', 1),
    ('SV003', 'Lê Hoàng Cường',  '2002-12-01', 'Nam', 'cuong.lh@email.com', 2),
    ('SV004', 'Phạm Thị Dung',   '2003-03-15', 'Nữ',  'dung.pt@email.com', 2);

-- Tài khoản mặc định
-- Mật khẩu: 123456  (SHA-256 = 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92)
INSERT IGNORE INTO users (username, password_hash, full_name, role) VALUES
    ('admin',    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
     'Quản trị viên',  'admin'),
    ('teacher1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
     'Giáo viên Demo', 'teacher');

-- Điểm mẫu
INSERT IGNORE INTO scores (student_id, subject_id, semester, midterm_score, final_score)
SELECT s.id, sub.id, 'HK1-2024', 7.5, 8.0
FROM students s, subjects sub
WHERE s.student_code = 'SV001' AND sub.subject_code = 'IT101';

INSERT IGNORE INTO scores (student_id, subject_id, semester, midterm_score, final_score)
SELECT s.id, sub.id, 'HK1-2024', 6.0, 7.0
FROM students s, subjects sub
WHERE s.student_code = 'SV001' AND sub.subject_code = 'MA101';

INSERT IGNORE INTO scores (student_id, subject_id, semester, midterm_score, final_score)
SELECT s.id, sub.id, 'HK1-2024', 8.0, 9.0
FROM students s, subjects sub
WHERE s.student_code = 'SV002' AND sub.subject_code = 'IT101';
