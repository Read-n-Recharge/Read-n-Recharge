import paho.mqtt.client as mqtt
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

def on_message(client, userdata, message):
    print(f"Received message '{str(message.payload.decode())}' on topic '{message.topic}' with QoS {message.qos}")

def connect_mqtt():
    client = mqtt.Client()

    client.username_pw_set("PutipongSailen", "Putipong.48852")

    ca_cert_path = os.path.join(os.path.dirname(__file__), 'cert/emqxsl-ca.crt')
    client.tls_set(ca_certs= ca_cert_path)

    try:   
        client.connect("wb35b1b7.ala.asia-southeast1.emqxsl.com", 8883, 60)
        print("Connected to MQTT Broker")
    except Exception as e: 
        print(f"Failed to connect MQTT Broker: {e}")
        return None
    
    client.on_message = on_message
    client.loop_start()

    return client

def check_emqx_connection():
    client = connect_mqtt()
    if client:  
        topic = "emqx/esp32"
        message = "Django server started successfully"
        client.publish(topic, message)
        print(f"Message sent to {topic}: {message}")
    else:
        print("Failed to send message due to connection issue")


@csrf_exempt
def start_mqtt_listener(request):
    if request.method == 'POST':
        client = connect_mqtt()
        if client:
            return JsonResponse({'status': 'listening'})
        else:
            return JsonResponse({'status': 'failed', 'reason': 'Connection issue'}, status=500)
        
    return JsonResponse({'status': 'failed', 'reason': 'invalid request method'}, status=400)

def control_relay_module(module_number, command):
    client = connect_mqtt()
    if client:
        topic = f"relay/{module_number}/control"
        client.publish(topic, command)
        print(f"Sent command '{command}' to '{topic}'")

        return JsonResponse({'status': 'success', 'module': module_number, 'command': command})
    else:
        return JsonResponse({'status': 'failed', 'reason': 'Failed to Connect to MQTT Broker'}, status=500)
    
def start_relay(request, module_number):
    return control_relay_module(module_number, 'START')

def stop_relay(request, module_number):
    return control_relay_module(module_number, 'STOP')

