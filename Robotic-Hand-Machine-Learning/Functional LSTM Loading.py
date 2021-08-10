#Setting up
from __future__ import print_function
from collections import deque
from threading import Lock, Thread
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import numpy as np
#np.random.seed(1)
import tensorflow as tf
from tensorflow import keras
from keras import regularizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import myo
import time
import sys
import psutil
import os

global training_set
global number_of_samples
global index_training_set, middle_training_set,thumb_training_set,verification_set
global data_array

FrequencyofArmband=200 #Fixed Value
number_of_channels =8 #Fixed Value
RecordingInterval=8 #In Seconds
number_of_samples = FrequencyofArmband*RecordingInterval
data_array=[]
size=50 #Response of hand movement depends on the sampling size, Current size is 50.
gestures=14

model = keras.models.load_model('C:/Users/m/Desktop/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand-master/Test1_realistic_model.h5')

# Check if Myo Connect.exe process is running
def check_if_process_running():

    try:
        for proc in psutil.process_iter():
            if proc.name()=='Myo Connect.exe':
                return True
            
        return False
            
    except (psutil.NoSuchProcess,psutil.AccessDenied, psutil.ZombieProcess):
        print (PROCNAME, " not running")

# Restart myo connect.exe process if its not running
def restart_process():
    PROCNAME = "Myo Connect.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
            # Wait a second
            time.sleep(1)

    while(check_if_process_running()==False):
        path = 'C:\Program Files (x86)\Thalmic Labs\Myo Connect\Myo Connect.exe'
        os.startfile(path)
        time.sleep(1)
        #while(check_if_process_running()==False):
        #    pass

    print("Process started")
    return True

# This class from Myo-python SDK listens to EMG signals from armband
class Listener(myo.DeviceListener):
    
    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def on_connected(self, event):
        print("Myo Connected")
        self.started = time.time()
        event.device.stream_emg(True)
        
    def get_emg_data(self):
        with self.lock:
            print("H")   # Ignore this

    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append((event.emg))
            
            if len(list(self.emg_data_queue))>=number_of_samples:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False

while True:
    while True:
        try:
            input("Hold a finger movement and press enter to get its classification")
            hub = myo.Hub()        
            listener = Listener(size)
            hub.run(listener.on_event,20000)
            
            # Here we send the received number of samples making them a list of 1000 rows 8 columns
            verification_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)
            
    predictions = model.predict(verification_set,batch_size=16)
    predicted_value = np.argmax(predictions[0])
    print(predictions[0])
    print(predicted_value)
    if predicted_value == 0:
        print("Thumb open")
    elif predicted_value == 1:
        print("Index finger open")
    elif predicted_value == 2:
        print("Middle finger open")
    elif predicted_value == 3:
        print("Ring finger open")
    elif predicted_value == 4:
        print("Pinky finger open")
    elif predicted_value == 5:
        print("Two fingers open")
    elif predicted_value == 6:
        print("Three fingers open")
    elif predicted_value == 7:
        print("Four fingers open")
    elif predicted_value == 8:
        print("Five fingers open")
    elif predicted_value == 9:
        print("All fingers closed")
    elif predicted_value == 10:
        print("Grasp movement")
    elif predicted_value == 11:
        print("Pick movement")
    elif predicted_value == 12:
        print("Resting")        
    else:
        pass