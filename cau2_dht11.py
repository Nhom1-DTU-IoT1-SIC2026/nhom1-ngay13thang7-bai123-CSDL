import time
import board
import adafruit_dht
import pymysql
from datetime import datetime
import digitalio

# 1. Cấu hình cảm biến DHT11 ở chân GPIO 4
dhtDevice = adafruit_dht.DHT11(board.D4)

# 2. Cấu hình Đèn LED Đỏ ở chân GPIO 17
led_do = digitalio.DigitalInOut(board.D17)
led_do.direction = digitalio.Direction.OUTPUT
led_do.value = False  # Đảm bảo LED tắt lúc mới chạy

# 3. Cấu hình kết nối Cơ sở dữ liệu
db_config = {
    'host': 'localhost',
    'user': 'nhom1',
    'password': '123456',  
    'database': 'HeThongIoT'
}

print("Dang ket noi voi co so du lieu...")

try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    print("Ket noi CSDL thanh cong! Dang doc cam bien...")

    while True:
        try:
            # Đọc nhiệt độ và độ ẩm
            nhiet_do = dhtDevice.temperature
            do_am = dhtDevice.humidity

            if nhiet_do is not None and do_am is not None:
                trang_thai_led = 1  # Bật LED nên trạng thái ghi vào DB là 1
                
                # Lưu vào DB
                sql = "INSERT INTO DuLieuCamBien (nhiet_do, do_am, trang_thai_led) VALUES (%s, %s, %s)"
                val = (nhiet_do, do_am, trang_thai_led)
                cursor.execute(sql, val)
                conn.commit()
                
                # In ra màn hình
                thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{thoi_gian}] Da luu -> Nhiet do: {nhiet_do:.1f}*C | Do am: {do_am:.1f}% | LED: Bật (1)")
                
                # -- XỬ LÝ NHỊP ĐỘ SÁNG ĐÈN VÀ NGHỈ --
                led_do.value = True   # Bật đèn sáng
                time.sleep(1)         # Sáng trong 1 giây
                
                led_do.value = False  # Tắt đèn
                time.sleep(9)         # Nghỉ 9 giây nữa (1 + 9 = 10 giây/lần đọc)
            
        except RuntimeError as error:
            print(f"Dang doc lai... loi nhe: ({error.args[0]})")
            time.sleep(2)
            continue

except KeyboardInterrupt:
    print("\nDa dung chuong trinh.")
except Exception as e:
    print(f"Loi he thong: {e}")
finally:
    if 'conn' in locals() and conn.open:
        cursor.close()
        conn.close()
        print("Da ngat ket noi CSDL.")
    dhtDevice.exit()
    led_do.value = False  # Đảm bảo tắt hẳn LED khi bấm Ctrl+C thoát chương trình
