# -*- coding: utf-8 -*-
"""
Bai 3 - Smart Light Device (thiet bi den thong minh)
- Subscribe topic dieu khien: iot/lab/light01/cmd
- Nhan lenh "ON"  -> chuyen trang thai den thanh bat
         lenh "OFF" -> chuyen trang thai den thanh tat
- Sau moi lenh hop le, publish trang thai moi len topic: iot/lab/light01/status
  Payload trang thai: {"device_id": "light01", "status": "ON"}

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
import json
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"
PORT = 1883

DEVICE_ID = "light01"
TOPIC_CMD = f"iot/lab/{DEVICE_ID}/cmd"        # topic nhan lenh dieu khien
TOPIC_STATUS = f"iot/lab/{DEVICE_ID}/status"  # topic gui trang thai

CLIENT_ID = f"device-bai3-{DEVICE_ID}-{int(time.time())}"

trang_thai_den = "OFF"   # trang thai ban dau cua den


def publish_trang_thai(client):
    """Gui trang thai hien tai cua den len topic status."""
    payload = json.dumps({"device_id": DEVICE_ID, "status": trang_thai_den})
    client.publish(TOPIC_STATUS, payload, qos=1)
    print(f"Da gui trang thai -> {TOPIC_STATUS}: {payload}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Ket noi that bai: {reason_code}")
        return
    print(f"[{DEVICE_ID}] Da ket noi toi broker {BROKER}:{PORT}")
    print(f"[{DEVICE_ID}] Dang lang nghe lenh tren topic: {TOPIC_CMD} (nhan Ctrl+C de dung)")
    client.subscribe(TOPIC_CMD, qos=1)
    publish_trang_thai(client)   # gui trang thai ban dau khi vua ket noi


def on_message(client, userdata, msg):
    global trang_thai_den
    lenh = msg.payload.decode("utf-8").strip().upper()
    print(f"\n[{DEVICE_ID}] Nhan lenh: {lenh}")

    if lenh == "ON":
        trang_thai_den = "ON"
        print(f"[{DEVICE_ID}] Den da BAT")
        publish_trang_thai(client)
    elif lenh == "OFF":
        trang_thai_den = "OFF"
        print(f"[{DEVICE_ID}] Den da TAT")
        publish_trang_thai(client)
    else:
        print(f"[{DEVICE_ID}] Lenh khong hop le: {lenh} (chi chap nhan ON/OFF)")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n[{DEVICE_ID}] Dung thiet bi (Ctrl+C).")
        client.disconnect()


if __name__ == "__main__":
    main()
