# -*- coding: utf-8 -*-
"""
Bai 1 - Subscriber
- Ket noi toi cung MQTT broker voi publisher
- Dang ky lang nghe topic: iot/lab/message
- Khi nhan duoc thong diep: in ra Topic, Noi dung, Thoi diem nhan
- Mo rong: chay lien tuc cho toi khi nguoi dung nhan Ctrl+C

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
from datetime import datetime
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"   # Phai trung voi broker cua publisher
PORT = 1883
TOPIC = "iot/lab/message"

CLIENT_ID = f"subscriber-bai1-{int(time.time())}"


def on_connect(client, userdata, flags, reason_code, properties):
    """Callback khi ket noi toi broker xong -> dang ky topic."""
    if reason_code.is_failure:
        print(f"Ket noi that bai: {reason_code}")
        return
    print(f"Da ket noi toi broker {BROKER}:{PORT}")
    print(f"Dang lang nghe topic: {TOPIC} (nhan Ctrl+C de dung)\n")
    client.subscribe(TOPIC, qos=1)


def on_message(client, userdata, msg):
    """Callback khi nhan duoc thong diep."""
    thoi_diem = datetime.now().strftime("%H:%M:%S")
    print("Nhan duoc message:")
    print(f"  Topic: {msg.topic}")
    print(f"  Payload: {msg.payload.decode('utf-8')}")
    print(f"  Time: {thoi_diem}")
    print("-" * 40)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)

    try:
        client.loop_forever()   # chay lien tuc
    except KeyboardInterrupt:
        print("\nDung subscriber (Ctrl+C).")
        client.disconnect()


if __name__ == "__main__":
    main()
