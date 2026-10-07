# -*- coding: utf-8 -*-
"""
Bai 2 - Monitoring Subscriber
- Subscribe topic du lieu cam bien: iot/lab/sensor01/data
  (dung wildcard iot/lab/+/data de nhan ca sensor01, sensor02 - phan mo rong;
   wildcard nay van bao gom topic iot/lab/sensor01/data theo yeu cau)
- Nhan du lieu JSON, in ra man hinh
- Kiem tra nguong:
    + Nhiet do > 35 do C  -> "CANH BAO: Nhiet do cao"
    + Do am < 40 %        -> "CANH BAO: Do am thap"

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
import json
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/+/data"   # wildcard '+' nhan du lieu moi sensor, gom ca sensor01

NGUONG_NHIET_DO = 35.0     # do C
NGUONG_DO_AM = 40.0        # %

CLIENT_ID = f"monitor-subscriber-bai2-{int(time.time())}"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Ket noi that bai: {reason_code}")
        return
    print(f"Da ket noi toi broker {BROKER}:{PORT}")
    print(f"Dang lang nghe topic: {TOPIC} (nhan Ctrl+C de dung)\n")
    client.subscribe(TOPIC, qos=1)


def on_message(client, userdata, msg):
    # Giai ma payload JSON
    try:
        du_lieu = json.loads(msg.payload.decode("utf-8"))
    except json.JSONDecodeError:
        print(f"Payload khong phai JSON hop le: {msg.payload}")
        return

    device_id = du_lieu.get("device_id", "unknown")
    temperature = du_lieu.get("temperature")
    humidity = du_lieu.get("humidity")

    # In du lieu ra man hinh
    print(f"Device: {device_id}")
    print(f"Temperature: {temperature} C")
    print(f"Humidity: {humidity} %")

    # Kiem tra nguong va canh bao
    if temperature is not None and temperature > NGUONG_NHIET_DO:
        print("CANH BAO: Nhiet do cao")
    if humidity is not None and humidity < NGUONG_DO_AM:
        print("CANH BAO: Do am thap")
    print("-" * 40)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDung monitoring subscriber (Ctrl+C).")
        client.disconnect()


if __name__ == "__main__":
    main()
