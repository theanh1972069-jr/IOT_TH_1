# Thực hành Buổi 1 — Lập trình Python với giao thức MQTT

## 1. Broker sử dụng

- **Broker:** `broker.emqx.io` — cổng `1883` (broker MQTT công cộng, miễn phí, không cần tài khoản).
- Có thể đổi sang broker khác (`test.mosquitto.org`, `broker.hivemq.com`, hoặc broker cài local bằng Mosquitto) bằng cách sửa 2 hằng số `BROKER` và `PORT` ở đầu mỗi file `.py`.
- Nếu dùng **Mosquitto local**: cài Mosquitto, chạy service, sau đó đặt `BROKER = "localhost"`, `PORT = 1883`.

> ⚠️ Lưu ý: broker công cộng là dùng chung cho tất cả mọi người. Nếu thấy message lạ lẫn vào topic (do bạn khác cùng dùng topic `iot/lab/...`), hãy đổi prefix topic thành riêng mình, ví dụ `iot/lab/B23DCCN001/message`, trong **cả 2 file** publisher và subscriber tương ứng.

## 2. Yêu cầu môi trường

```bash
pip install paho-mqtt
```

- Python 3.x (code viết cho **paho-mqtt phiên bản 2.x** — nếu máy đã có bản 1.x cũ thì chạy `pip install -U paho-mqtt`).

## 3. Danh sách file

| File | Mô tả |
|---|---|
| `publisher_bai1.py` | Bài 1 — gửi thông điệp (họ tên, MSSV, lời chào) lên topic `iot/lab/message` |
| `subscriber_bai1.py` | Bài 1 — lắng nghe `iot/lab/message`, in Topic / Payload / Time |
| `sensor_publisher_bai2.py` | Bài 2 — mô phỏng cảm biến gửi JSON mỗi 3 giây lên `iot/lab/sensor01/data` (kèm `sensor02`) |
| `monitor_subscriber_bai2.py` | Bài 2 — nhận dữ liệu cảm biến, in ra và cảnh báo vượt ngưỡng |
| `device_bai3.py` | Bài 3 — thiết bị đèn thông minh: nhận lệnh ON/OFF, gửi lại trạng thái |
| `controller_bai3.py` | Bài 3 — app điều khiển: nhập lệnh ON/OFF/EXIT từ bàn phím |

## 4. Cách chạy từng chương trình

Mở **2 cửa sổ terminal** cho mỗi bài (chạy subscriber/device **trước**, publisher/controller **sau**).

### Bài 1 — Gửi/nhận thông điệp cơ bản

```bash
# Terminal 1
python subscriber_bai1.py

# Terminal 2
python publisher_bai1.py
```

- Trước khi chạy: sửa `HO_TEN` và `MSSV` ở đầu file `publisher_bai1.py`.
- Publisher gửi liên tiếp mỗi 2 giây, nhấn `Ctrl+C` để dừng cả 2 chương trình.

### Bài 2 — Mô phỏng cảm biến nhiệt độ / độ ẩm

```bash
# Terminal 1
python monitor_subscriber_bai2.py

# Terminal 2
python sensor_publisher_bai2.py
```

- Dữ liệu JSON gửi mỗi 3 giây. Nhấn `Ctrl+C` để dừng.

### Bài 3 — Điều khiển đèn thông minh (2 chiều)

```bash
# Terminal 1
python device_bai3.py

# Terminal 2
python controller_bai3.py
```

- Ở terminal controller, nhập `ON`, `OFF` để điều khiển đèn, `EXIT` để thoát.
- Nhập lệnh khác ON/OFF sẽ báo lỗi "Lenh khong hop le".

## 5. Kết quả đạt được

- ✅ Bài 1: kết nối broker thành công, publish đúng topic, subscriber nhận đúng dữ liệu và hiển thị rõ Topic / Payload / Time:

```
Nhan duoc message:
  Topic: iot/lab/message
  Payload: Xin chao tu client Python MQTT - B23DCCN001 - Nguyen Van A (lan 1)
  Time: 10:30:36
```

- ✅ Bài 2: payload đúng định dạng JSON, gửi tuần hoàn 3 giây, subscriber phân tích dữ liệu và cảnh báo đúng điều kiện:

```
Device: sensor01
Temperature: 39.4 C
Humidity: 51.3 %
CANH BAO: Nhiet do cao
```

- ✅ Bài 3: điều khiển được thiết bị qua MQTT, thiết bị phản hồi đúng trạng thái, giao tiếp 2 chiều:

```
Nhap lenh: ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id": "light01", "status": "ON"}
```

## 6. Mô hình topic sử dụng

```
iot/lab/message            # Bài 1: thông điệp chào
iot/lab/sensor01/data      # Bài 2: dữ liệu cảm biến 01 (JSON)
iot/lab/sensor02/data      # Bài 2 (mở rộng): dữ liệu cảm biến 02
iot/lab/light01/cmd        # Bài 3: lệnh điều khiển đèn (ON/OFF)
iot/lab/light01/status     # Bài 3: trạng thái phản hồi của đèn (JSON)
```
