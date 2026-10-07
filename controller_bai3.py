# -*- coding: utf-8 -*-
"""
Bai 3 - Controller App (ung dung dieu khien)
- Cho nguoi dung nhap lenh tu ban phim: ON / OFF (EXIT de thoat)
- Publish lenh len topic: iot/lab/light01/cmd
- Dong thoi subscribe topic trang thai: iot/lab/light01/status
  va hien thi trang thai den sau khi nhan phan hoi
- Mo rong: xu ly lenh sai (khac ON/OFF thi bao loi), lenh EXIT de ket thuc

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"
PORT = 1883

DEVICE_ID = "light01"
TOPIC_CMD = f"iot/lab/{DEVICE_ID}/cmd"        # topic gui lenh dieu khien
TOPIC_STATUS = f"iot/lab/{DEVICE_ID}/status"  # topic nhan trang thai phan hoi

CLIENT_ID = f"controller-bai3-{int(time.time())}"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Ket noi that bai: {reason_code}")
        return
    print(f"Da ket noi toi broker {BROKER}:{PORT}")
    client.subscribe(TOPIC_STATUS, qos=1)


def on_message(client, userdata, msg):
    """Hien thi trang thai den nhan duoc tu thiet bi."""
    print("\nTrang thai nhan duoc:")
    print(msg.payload.decode("utf-8"))


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()   # luong nen de nhan trang thai trong khi nhap lenh

    try:
        while True:
            lenh = input("\nNhap lenh: ").strip().upper()

            if lenh == "EXIT":
                print("Ket thuc chuong trinh.")
                break

            # Xu ly lenh sai
            if lenh not in ("ON", "OFF"):
                print("Lenh khong hop le! Chi chap nhan ON, OFF hoac EXIT.")
                continue

            client.publish(TOPIC_CMD, lenh, qos=1)
            print(f"Da gui lenh {lenh} toi {DEVICE_ID}")
    except KeyboardInterrupt:
        print("\nKet thuc chuong trinh (Ctrl+C).")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
