from flask import Flask, render_template, jsonify, request
import pymysql
import board
import digitalio

app = Flask(__name__)

# Cấu hình chân LED GPIO 17
led_do = digitalio.DigitalInOut(board.D17)
led_do.direction = digitalio.Direction.OUTPUT

# Cấu hình CSDL MariaDB
db_config = {
    'host': 'localhost',
    'user': 'nhom1',
    'password': '123456',
    'database': 'HeThongIoT'
}

# Đường dẫn trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Đường dẫn API cung cấp dữ liệu cho biểu đồ (lấy 10 dòng mới nhất)
@app.route('/api/data')
def get_data():
    try:
        conn = pymysql.connect(**db_config)
        # Sử dụng DictCursor để trả về dạng dictionary dễ đưa lên web
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # Lấy giờ:phút:giây để hiển thị cho gọn
        sql = """
            SELECT DATE_FORMAT(ngay_gio, '%H:%i:%s') as thoi_gian, nhiet_do, do_am 
            FROM DuLieuCamBien 
            ORDER BY id DESC LIMIT 10
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        # Đảo ngược lại mảng để vẽ từ trái sang phải
        rows.reverse()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)})

# Đường dẫn API điều khiển LED
@app.route('/api/led', methods=['GET', 'POST'])
def led_control():
    if request.method == 'POST':
        data = request.json
        # Thay đổi trạng thái vật lý của chân LED
        led_do.value = data['status']
    
    return jsonify({'status': led_do.value})

if __name__ == '__main__':
    # Chạy server ở cổng 5000, mọi máy trong cùng mạng Wifi đều truy cập được
    app.run(host='0.0.0.0', port=5000)
