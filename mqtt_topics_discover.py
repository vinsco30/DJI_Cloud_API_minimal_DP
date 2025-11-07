#!/usr/bin/env python3

import os
import json
import pprint

from importlib.metadata import version

import paho
import paho.mqtt.client as mqtt

host_addr = os.environ["HOST_ADDR"]

# This set will store all unique topics
discovered_topics = set()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    # Subscribe to the general "thing" topic, which covers all drone data
    client.subscribe("thing/#")
    client.subscribe("sys/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):

    # Check if we've seen this topic before
    if msg.topic not in discovered_topics:
        # If it's new, add it to our set
        discovered_topics.add(msg.topic)
        
        # Print the complete list of unique topics found so far
        print("\n--- Discovered Topics List (Updated) ---")
        # Using pprint for a clean, sorted list
        pprint.pprint(sorted(list(discovered_topics)))
        print("------------------------------------------\n")

# --- All the old logic for OSD and status is removed ---

PAHO_MAIN_VER = int(version("paho-mqtt").split(".")[0])
if PAHO_MAIN_VER == 1:
    client = mqtt.Client(transport="tcp")
if PAHO_MAIN_VER == 2:
    client = mqtt.Client(paho.mqtt.enums.CallbackAPIVersion.VERSION2, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to MQTT server at {host_addr}...")
client.connect(host_addr, 1883, 60)

# Blocking call that processes network traffic
client.loop_forever()