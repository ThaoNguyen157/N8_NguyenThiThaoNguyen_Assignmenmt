KTPM_Assignment-2

Tổng Quan
OpenCart là một nền tảng thương mại điện tử mã nguồn mở, giúp bạn dễ dàng xây dựng và quản lý các cửa hàng trực tuyến.
Dự án này sử dụng Selenium WebDriver để tự động hóa kiểm thử cho OpenCart và Pytest để quản lý các kịch bản kiểm thử, Selenium giúp tương tác với giao diện trình duyệt, hỗ trợ việc kiểm thử các tính năng trên giao diện người dùng.

Cài Đặt Môi Trường
1. Cài Đặt OpenCart
Tải mã nguồn OpenCart từ Trang chủ OpenCart.
Làm theo các hướng dẫn trên trang để thiết lập OpenCart trên máy chủ cục bộ hoặc dịch vụ lưu trữ web, đảm bảo truy cập được vào trang quản trị và cửa hàng trực tuyến.
2. Cài Đặt Python
Tải xuống Python từ Python.org và cài đặt.
Đảm bảo chọn “Add Python to PATH” trong quá trình cài đặt để dễ dàng truy cập từ dòng lệnh.
3. Cài đặt thư viện Selenium:

Mở terminal và chạy lệnh sau để cài đặt thư viện Selenium:
pip install selenium

4. Cài Đặt WebDriver Cho Trình Duyệt Mong Muốn

Microsoft Edge: Tải Edge WebDriver từ Microsoft Edge WebDriver.
Google Chrome: Tải ChromeDriver từ ChromeDriver Download.
Firefox: Tải GeckoDriver từ GeckoDriver Releases.
Thêm đường dẫn WebDriver vào PATH hệ thống hoặc đặt trong thư mục env/Scripts.

5. Cách Chạy Kiểm Thử

Điều hướng đến thư mục chứa các tệp kiểm thử.
Để chạy toàn bộ các kiểm thử, dùng lệnh:

pytest <ten_tap_kiem_thu>.py

 Ví dụ: pytest search.py
