-- ============================================================
-- Tạo database và các bảng cho hệ thống Quản lý Điểm
-- Chạy: mysql -u root -p < database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS thongkediem
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE thongkediem;

-- Bảng lớp học
CREATE TABLE IF NOT EXISTS classes (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE COMMENT 'Tên lớp, ví dụ: CNTT01',
    faculty    VARCHAR(150)               COMMENT 'Khoa / ngành',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng sinh viên
CREATE TABLE IF NOT EXISTS students (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20)  NOT NULL UNIQUE COMMENT 'Mã sinh viên',
    full_name    VARCHAR(150) NOT NULL,
    dob          DATE                   COMMENT 'Ngày sinh',
    gender       ENUM('Nam','Nữ','Khác'),
    email        VARCHAR(150),
    phone        VARCHAR(15),
    class_id     INT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL
);

-- Bảng môn học
CREATE TABLE IF NOT EXISTS subjects (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20)  NOT NULL UNIQUE COMMENT 'Mã môn, ví dụ: IT101',
    name         VARCHAR(150) NOT NULL,
    credits      TINYINT UNSIGNED NOT NULL DEFAULT 3 COMMENT 'Số tín chỉ',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng điểm thi
CREATE TABLE IF NOT EXISTS scores (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    student_id     INT NOT NULL,
    subject_id     INT NOT NULL,
    semester       VARCHAR(20) NOT NULL COMMENT 'Học kỳ, ví dụ: HK1-2024',
    midterm_score  DECIMAL(4,2) COMMENT 'Điểm giữa kỳ (0-10)',
    final_score    DECIMAL(4,2) COMMENT 'Điểm cuối kỳ (0-10)',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Mỗi SV chỉ có 1 bộ điểm cho mỗi môn + học kỳ
    UNIQUE KEY uk_sv_mon_hk (student_id, subject_id, semester),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- Bảng tài khoản người dùng
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    password_hash VARCHAR(64)  NOT NULL COMMENT 'SHA-256 hash',
    full_name     VARCHAR(150),
    role          ENUM('admin','teacher','viewer') NOT NULL DEFAULT 'teacher',
    is_active     TINYINT(1) NOT NULL DEFAULT 1,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
