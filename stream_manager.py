#!/usr/bin/env python3
import os
import json
import time
import uuid
import threading
from importlib.metadata import version
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
HOST_ADDR = os.environ.get("HOST_ADDR", "localhost")
MQTT_PORT = 1883
RTMP_PORT = 1935
KEEP_ALIVE = 60

# VIDEO QUALITY SETTINGS
# 1 = Smooth (Lowest bandwidth, ~500Kbps) - BEST FOR WEAK WI-FI
# 2 = Standard Definition (~2Mbps) - RECOMMENDED STARTING POINT
# 3 = High Definition (~5Mbps+) - CAUSES CRASHES ON WEAK NETWORKS
VIDEO_QUALITY = 1 

active_drones = set()

def start_live_stream(client, drone_sn):
    time.sleep(3)
    topic = f"thing/product/{drone_sn}/services"
    rtmp_url = f"rtmp://{HOST_ADDR}:{RTMP_PORT}/live/{drone_sn}"
    
    print(f"\n🎥 Starting video for {drone_sn} (Quality: {VIDEO_QUALITY}) -> {rtmp_url}")

    payload = {
        "tid": str(uuid.uuid4()),
        "bid": str(uuid.uuid4()),
        "timestamp": int(time.time() * 1000),
        "method": "live_start_push",
        "data": {
            "live_type": 1, # RTMP
            "url": rtmp_url,
            "video_id": "gimbal",
            "video_quality": VIDEO_QUALITY
        }
    }
    client.publish(topic, json.dumps(payload))

# --- USER'S TELEMETRY HANDLER ---
def handle_osd_message(message: dict, device_sn: str):
    data = message.get("data", {})
    if 'attitude_pitch' not in data: return

    # Use .get() to read data without removing it
    lat = data.get("latitude", 0)
    lon = data.get("longitude", 0)
    height = data.get("height", 0)
    attitude_head = data.get("attitude_head", 0)
    attitude_pitch = data.get("attitude_pitch", 0)
    attitude_roll = data.get("attitude_roll", 0)

    print(f"🌍 [{device_sn}] Status: Lat: {lat} Lon: {lon} height: {height} att_head {attitude_head} att_pitch {attitude_pitch} att_roll {attitude_roll}", end='\r')

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected to MQTT at {HOST_ADDR}. Waiting for drone...")
        client.subscribe("thing/#")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg: mqtt.MQTTMessage):
    try:
        if msg.topic.startswith("$SYS") or msg.topic.endswith("_reply"): return
        payload_str = msg.payload.decode("utf-8")
        message = json.loads(payload_str)
        topic_parts = msg.topic.split('/')
        device_sn = topic_parts[2] if len(topic_parts) > 2 else "Unknown"

        if msg.topic.endswith("status") or msg.topic.endswith("requests"):
            response = {
                "tid": message.get("tid"),
                "bid": message.get("bid"),
                "timestamp": int(time.time() * 1000),
                "method": message.get("method"),
                "data": {"result": 0}
            }
            client.publish(msg.topic + "_reply", payload=json.dumps(response))

        elif msg.topic.endswith("osd"):
             # 1. Check for new drone and trigger video
             if 'attitude_pitch' in message.get('data', {}) and device_sn not in active_drones:
                 active_drones.add(device_sn)
                 threading.Thread(target=start_live_stream, args=(client, device_sn)).start()
             # 2. Print telemetry
             handle_osd_message(message, device_sn)

        elif msg.topic.endswith("services_reply"):
            if message.get('method') == 'live_start_push':
                res = message.get('data', {}).get('result')
                if res == 0:
                    print(f"\n✅ STREAMING ACTIVE! Open VLC: rtmp://{HOST_ADDR}:{RTMP_PORT}/live/{device_sn}\n")
                else:
                     print(f"\n❌ STREAM FAILED (Error {res})\n")

    except Exception as e:
        pass

# --- MAIN ---
PAHO_MAIN_VER = int(version("paho-mqtt").split(".")[0])
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) if PAHO_MAIN_VER >= 2 else mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Starting Auto-Streamer on {HOST_ADDR}...")
client.connect(HOST_ADDR, MQTT_PORT, KEEP_ALIVE)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")