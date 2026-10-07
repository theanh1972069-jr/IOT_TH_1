# -*- coding: utf-8 -*-
"""
Bai 1 - Publisher
- Ket noi toi MQTT broker
- Gui thong diep (Ho ten, MSSV, loi chao) len topic: iot/lab/message
- Mo rong: gui nhieu thong diep lien tiep cho toi khi nhan Ctrl+C

Yeu cau: pip install paho-mqtt (phien ban 2.x)
"""
import time
import paho.mqtt.client as mqtt

# ==================== CAU HINH ====================
BROKER = "broker.emqx.io"   # Broker MQTT cong cong (co the doi: test.mosquitto.org, broker.hivemq.com, hoac IP broker local)
PORT = 1883                 # Cong MQTT khong ma hoa mac dinh
TOPIC = "iot/lab/message"

# TODO: Sua thong tin ca nhan tai day truoc khi nop bai
HO_TEN = "Nguyen Van A"
MSSV = "B23DCCN001"
LOI_CHAO = "Xin chao tu client Python MQTT"

# client_id duy nhat de tranh xung dot tren broker cong cong
CLIENT_ID = f"publisher-bai1-{int(time.time())}"


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    print(f"Da ket noi toi broker {BROKER}:{PORT}")
    print(f"Gui thong diep len topic: {TOPIC} (nhan Ctrl+C de dung)")

    dem = 0
    try:
        while True:
            dem += 1
            # Noi dung thong diep: loi chao - MSSV - Ho ten
            payload = f"{LOI_CHAO} - {MSSV} - {HO_TEN} (lan {dem})"
            client.publish(TOPIC, payload, qos=1)
            print(f"[{time.strftime('%H:%M:%S')}] Da gui: {payload}")
            time.sleep(2)  # gui moi 2 giay
    except KeyboardInterrupt:
        print("\nDung publisher (Ctrl+C).")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
