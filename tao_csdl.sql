-- Tao co so du lieu
CREATE DATABASE IF NOT EXISTS HeThongIoT;
USE HeThongIoT;

-- Tao bang luu tru
CREATE TABLE IF NOT EXISTS DuLieuCamBien (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ngay_gio DATETIME DEFAULT CURRENT_TIMESTAMP,
    nhiet_do FLOAT,
    do_am FLOAT,
    trang_thai_led INT
)
