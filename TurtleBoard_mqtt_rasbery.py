
import serial
import keyboard
import paho.mqtt.client as mqtt
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)


def on_connect(client,usedata,flags, rc):
    if rc == 0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("Error")


connected = False
broker_address = "dev.rightech.io"
port = 1883
user = "111"
password = "111"

client = mqtt.Client(client_id="mqtt-anulanov_1-5npumo")
client.username_pw_set(user, password = password)
#client.on_message = on_message
client.on_connect = on_connect
#client.on_publish = on_publish
#client.on_subscribe = on_subscribe

client.connect(broker_address, port=port)
client.loop_start()
while connected != True:
    time.sleep(0.2)
seq = []
while True:
    for c in ser.read():
        seq.append(chr(c)) #convert from ASCII
        joined_seq = ''.join(str(v) for v in seq) #Make a string from array
        if chr(c) == '\n':
            k = joined_seq.find('#')
            if k != -1:
                data_str = joined_seq[k+1:]
                data_str = data_str.strip()
                i = data_str.find(' ')
                temp = float(data_str[:i])
                humd = data_str[i:]
                humd = humd.replace(' ','')
                humd = float(humd)
                client.publish("base/state/humd", humd)
                client.publish("base/state/temp", temp)
                seq = []
                break
            seq = []
            break
    if keyboard.is_pressed('Esc'):  # if key 'Esc' is pressed 
            client.loop_stop()
            client.disconnect()
            print('END!')
            break  # finishing the loop