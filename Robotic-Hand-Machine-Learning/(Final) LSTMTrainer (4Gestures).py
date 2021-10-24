#Setting up
from __future__ import print_function
from collections import deque
from threading import Lock, Thread
import seaborn as sb

import numpy as np
#np.random.seed(1)
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

from sklearn.model_selection import train_test_split

import myo
import time

import psutil
import os

global training_set
global number_of_samples
global index_training_set, middle_training_set,thumb_training_set,verification_set
global data_array

FrequencyofArmband=200 #Fixed Value
number_of_channels =8 #Fixed Value
RecordingInterval=10 #In Seconds
number_of_samples = FrequencyofArmband*RecordingInterval
data_array=[]
size=200 #Response of hand movement depends on the sampling size, Current size is 100.
gestures=4 #Rest and 3 other gestures

#Setting up Testing Variables
# 8 Sensors in armband
Sensor1 = np.zeros((1,number_of_samples))
Sensor2 = np.zeros((1,number_of_samples))
Sensor3 = np.zeros((1,number_of_samples))
Sensor4 = np.zeros((1,number_of_samples))
Sensor5 = np.zeros((1,number_of_samples))
Sensor6 = np.zeros((1,number_of_samples))
Sensor7 = np.zeros((1,number_of_samples))
Sensor8 = np.zeros((1,number_of_samples))

# 12 finger movements
gesture1_training_set = np.zeros((number_of_channels,number_of_samples))
gesture2_training_set = np.zeros((number_of_channels,number_of_samples))
gesture3_training_set = np.zeros((number_of_channels,number_of_samples))
gesture4_training_set = np.zeros((number_of_channels,number_of_samples))

verification_set = np.zeros((number_of_channels,number_of_samples))
training_set = np.zeros((number_of_channels,number_of_samples))


gesture1_label = 0
gesture2_label = 1
gesture3_label = 2
gesture4_label = 3

 
#Connecting to Armband

name = input("Enter name of Subject")

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
            

def main():
    unrecognized_training_set = np.zeros((number_of_channels,number_of_samples))
    gesture1_training_set = np.zeros((number_of_channels,number_of_samples))
    gesture2_training_set = np.zeros((number_of_channels,number_of_samples))
    gesture3_training_set = np.zeros((number_of_channels,number_of_samples))
    gesture4_training_set = np.zeros((number_of_channels,number_of_samples))
    verification_set = np.zeros((number_of_channels,number_of_samples))
    training_set = np.zeros((number_of_channels,number_of_samples))
    # This function kills Myo Connect.exe and restarts it to make sure it is running
    # Because sometimes the application does not run even when Myo Connect process is running
    # So i think its a good idea to just kill if its not running and restart it

    while(restart_process()!=True):
        pass
    # Wait for 3 seconds until Myo Connect.exe starts
    time.sleep(3)
    
    # Initialize the SDK of Myo Armband
    myo.init(r'C:\Users\himol\OneDrive\Documents\GitHub\EMGingers-control\Robotic-Hand-Machine-Learning\myo-sdk-win-0.9.0\bin\myo64.dll')
    # Change as needed
    hub = myo.Hub()
    listener = Listener(number_of_samples)

    legend = ['Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6','Sensor 7','Sensor 8']

    ################## HERE WE GET TRAINING DATA FOR THUMB FINGER OPEN ########
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Do Gesture 1")    
            hub.run(listener.on_event,20000)
            gesture1_training_set = np.array((data_array[0]))
            print(gesture1_training_set.shape)
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)
        
    # Here we send the received number of samples making them a list of 1000 rows 8 columns just how we need to feed to tensorflow
    
    ################## HERE WE GET TRAINING DATA FOR INDEX FINGER OPEN ########
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Do Gesture 2")    
            hub.run(listener.on_event,20000)
            gesture2_training_set = np.array((data_array[0]))
            print(gesture2_training_set.shape)
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################## HERE WE GET TRAINING DATA FOR MIDDLE FINGER OPEN #################
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Do Gesture 3")    
            hub.run(listener.on_event,20000)
            gesture3_training_set = np.array((data_array[0]))
            print(gesture3_training_set.shape)
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    # Here we send the received number of samples making them a list of 1000 rows 8 columns
        
    ################## HERE WE GET TRAINING DATA FOR RING FINGER OPEN ##########
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Do Gesture 4")    
            hub.run(listener.on_event,20000)
            gesture4_training_set = np.array((data_array[0]))
            print(gesture4_training_set.shape)
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)



    # Here we stack all the data row wise
    conc_array = np.concatenate([
            gesture1_training_set,
            gesture2_training_set,
            gesture3_training_set,
            gesture4_training_set
        ],axis=0)
    print(conc_array.shape)
    np.savetxt('C:/Users/himol/OneDrive/Documents/GitHub/EMGingers-control/Robotic-Hand-Machine-Learning/'+name+'.txt', conc_array, fmt='%i')
    #change as needed 
    # In this method the EMG data gets trained and verified

    Train(conc_array)
    

# This method is responsible for training EMG data
def Train(conc_array):
    global training_set,gestures
    global gesture1_training_set, gesture2_training_set, gesture3_training_set, gesture4_training_set
    global number_of_samples,size,number_of_channels
    labels=[]
    print(conc_array.size)
    TrainingSamples=int(conc_array.size/(size*number_of_channels)) #TrainingSample is the number of train data, size is the length of each data, 8 is channel of data
    conc_array=np.reshape(conc_array, (TrainingSamples,size,number_of_channels))
    print(conc_array,conc_array.shape)
    
    
    for i in range(0,gestures):
        for j in range(0,(int(TrainingSamples/gestures))):
            labels.append(i)
    
    labels = np.asarray(labels)
    labels = np.reshape(labels,(labels.size,1))
    print(labels, len(labels),type(labels))
    train_data, validation_data,train_labels,validation_labels = train_test_split(conc_array, labels, random_state = 3)
    
    print("TS ", TrainingSamples, " S " , number_of_samples)
    print("Length of train data is ", train_data.shape, " train labels is " , train_labels.shape)
    print("Length of validation data is ", validation_data.shape , " validation labels is " , validation_labels.shape)
    print(train_labels)
    
    model = Sequential()
    model.add(LSTM(50,input_shape=(size,number_of_channels),return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(32,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(gestures,activation='softmax'))
    adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=1e-7, amsgrad=False)
    model.compile(optimizer=adam_optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
         
    history = model.fit(train_data, train_labels, epochs=200,validation_data=(validation_data,validation_labels),batch_size=16)
    model.save('C:/Users/himol/OneDrive/Documents/GitHub/EMGingers-control/Robotic-Hand-Machine-Learning/'+name+'_realistic_model.h5')
    #change as needed 


    
    

if __name__ == '__main__':
    main()

    
