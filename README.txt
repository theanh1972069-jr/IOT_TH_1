THUC HANH BUOI 1 - LAP TRINH PYTHON VOI MQTT
==============================================

1. BROKER SU DUNG
- broker.emqx.io, cong 1883 (broker MQTT cong cong, khong can tai khoan).
- Muon doi broker: sua hang so BROKER va PORT o dau moi file .py
  (vi du broker local: BROKER = "localhost").
- Cai thu vien: pip install paho-mqtt (phien ban 2.x)

2. CACH CHAY TUNG CHUONG TRINH
(mo 2 terminal cho moi bai, chay subscriber/device TRUOC)

Bai 1:
  python subscriber_bai1.py     (terminal 1)
  python publisher_bai1.py      (terminal 2 - nho sua HO_TEN, MSSV trong file)

Bai 2:
  python monitor_subscriber_bai2.py   (terminal 1)
  python sensor_publisher_bai2.py     (terminal 2)

Bai 3:
  python device_bai3.py         (terminal 1)
  python controller_bai3.py     (terminal 2: nhap ON / OFF / EXIT)

3. KET QUA DAT DUOC
- Bai 1: publish/subscribe thanh cong topic iot/lab/message, hien thi
  day du Topic - Payload - Time.
- Bai 2: gui JSON dinh ky 3 giay, subscriber phan tich du lieu va canh
  bao dung dieu kien (nhiet do > 35C, do am < 40%).
- Bai 3: dieu khien den ON/OFF qua MQTT, thiet bi phan hoi dung trang
  thai, giao tiep 2 chieu, xu ly lenh sai va lenh EXIT.

(Chi tiet xem file README.md)
