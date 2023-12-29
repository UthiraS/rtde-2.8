from pynput import keyboard
import time
import os

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.f2:
        sys.exit()
        

listener = keyboard.Listener(on_release=on_release)

listener.start()

os.system('python3 record.py --host=127.0.0.1 --port=30004 --output robot_data_record.csv') 
input('Press ENTER to exit')



