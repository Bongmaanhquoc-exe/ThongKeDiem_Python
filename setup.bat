@echo off
chcp 65001 >nul
echo ============================================
echo   CÀI ĐẶT HỆ THỐNG QUẢN LÝ ĐIỂM SINH VIÊN
echo ============================================
echo.

echo [1] Cài thư viện Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo LỖI: Không cài được thư viện. Kiểm tra pip đã cài chưa.
    pause & exit
)

echo.
echo [2] Tạo database MySQL...
echo Nhập mật khẩu MySQL (root):
set /p MYSQL_PASS=

mysql -u root -p%MYSQL_PASS% < database\schema.sql
if errorlevel 1 (
    echo LỖI: Không tạo được database. Kiểm tra MySQL đang chạy chưa.
    pause & exit
)

mysql -u root -p%MYSQL_PASS% < database\seed.sql
echo.
echo [3] Cập nhật mật khẩu trong config.ini...
echo     Mở file config.ini, sửa dòng password = %MYSQL_PASS%
echo.
echo ============================================
echo   CÀI ĐẶT XONG!
echo   Tài khoản mặc định: admin / 123456
echo   Chạy ứng dụng: python main.py
echo ============================================
pause
