import os
import sys
import time
from pynput import keyboard
import sys
sys.path.append('..')


class Error(Exception):
    """Base class for other exceptions"""
    pass


class KeybaordExist(Error):
    """Raised when the input value is too small"""
    pass

break_program = False
def on_press(key):
    global break_program
    print (key)
    if key == keyboard.Key.caps_lock:
     print ('end pressed')
     break_program = True        
     raise KeybaordExist
     return False

with keyboard.Listener(on_press=on_press) as listener:
    try:
     os.system('python3 record.py --host=127.0.0.1 --port=30004 --output robot_data_record.csv')  
     listener.join()   
    except KeyboardExist:
     sys.exit()
        
        
     
    

 
