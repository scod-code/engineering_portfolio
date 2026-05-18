import json, os, time

try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

BROKER = os.environ.get("MQTT_BROKER", "mqtt-broker")
PORT   = int(os.environ.get("MQTT_PORT",  "1883"))
TOPIC  = os.environ.get("MQTT_TOPIC",  "cwk/risk_result")


def publish_mqtt(payload: dict, topic: str = TOPIC,
                 broker: str = BROKER, port: int = PORT) -> bool:
    if not MQTT_AVAILABLE:
        print("[MQTT] paho-mqtt not installed — skipping")
        return False
    try:
        connected = []

        def on_connect(client, userdata, flags, reason_code, properties):
            connected.append(True)

        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        client.on_connect = on_connect
        client.connect(broker, port, 60)
        client.loop_start()

        deadline = time.time() + 10
        while not connected and time.time() < deadline:
            time.sleep(0.1)

        client.publish(topic, json.dumps(payload), qos=1, retain=False)
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        print(f"[MQTT] Published to {topic}:")
        print(json.dumps(payload, indent=2))
        return True
    except Exception as e:
        print(f"[MQTT] Could not publish: {e}")
        return False


if __name__ == "__main__":
    # Standalone orchestrator mode — used by Docker Compose orchestrator service
    while True:
        publish_mqtt({"status": "orchestrator_alive", "ts": time.time()})
        time.sleep(15)
