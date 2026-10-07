# -*- coding: utf-8 -*-
"""
Bai 2 - Sensor Publisher
- Mo phong cam bien nhiet do / do am gui du lieu dinh ky moi 3 giay
- Topic: iot/lab/sensor01/data
- Payload dang JSON: {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
- Gia tri nhiet do / do am sinh ngau nhien trong khoang hop ly
- Mo rong: gui du lieu cua nhieu thiet bi (sensor01, sensor02)

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
import json
import random
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"
PORT = 1883

# Mo rong: nhieu thiet bi, moi thiet bi gui len topic rieng iot/lab/<device_id>/data
DEVICES = ["sensor01", "sensor02"]
TOPIC_TEMPLATE = "iot/lab/{device_id}/data"

CHU_KY_GUI = 3  # giay

CLIENT_ID = f"sensor-publisher-bai2-{int(time.time())}"


def sinh_du_lieu(device_id):
    """Sinh du lieu cam bien ngau nhien trong khoang hop ly."""
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(25.0, 40.0), 1),  # 25 - 40 do C
        "humidity": round(random.uniform(30.0, 80.0), 1),     # 30 - 80 %
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    print(f"Da ket noi toi broker {BROKER}:{PORT}")
    print(f"Mo phong {len(DEVICES)} cam bien, gui du lieu moi {CHU_KY_GUI} giay (nhan Ctrl+C de dung)\n")

    try:
        while True:
            for device_id in DEVICES:
                du_lieu = sinh_du_lieu(device_id)
                topic = TOPIC_TEMPLATE.format(device_id=device_id)
                payload = json.dumps(du_lieu)   # dong goi JSON
                client.publish(topic, payload, qos=1)
                print(f"[{time.strftime('%H:%M:%S')}] {topic} -> {payload}")
            print()
            time.sleep(CHU_KY_GUI)
    except KeyboardInterrupt:
        print("\nDung sensor publisher (Ctrl+C).")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
