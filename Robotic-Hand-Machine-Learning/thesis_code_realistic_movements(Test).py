
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
from sklearn.model_selection import train_test_split

import myo
import time
import sys
import psutil
import os


# This training set will contain 1000 samples of 8 sensor values
global training_set
global number_of_samples
global index_training_set, middle_training_set,thumb_training_set,verification_set
global data_array
number_of_samples = 1000
number_of_channels =8
data_array=[]
size=20
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
index_open_training_set = np.zeros((8,number_of_samples))
middle_open_training_set = np.zeros((8,number_of_samples))
thumb_open_training_set = np.zeros((8,number_of_samples))
ring_open_training_set = np.zeros((8,number_of_samples))
pinky_open_training_set = np.zeros((8,number_of_samples))
two_open_training_set = np.zeros((8,number_of_samples))
three_open_training_set = np.zeros((8,number_of_samples))
four_open_training_set = np.zeros((8,number_of_samples))
five_open_training_set = np.zeros((8,number_of_samples))
all_fingers_closed_training_set = np.zeros((8,number_of_samples))
grasp_training_set = np.zeros((8,number_of_samples))
pick_training_set = np.zeros((8,number_of_samples))

verification_set = np.zeros((8,number_of_samples))
training_set = np.zeros((8,number_of_samples))


thumb_open_label = 0
index_open_label = 1
middle_open_label = 2
ring_open_label = 3
pinky_open_label = 4
two_open_label = 5
three_open_label = 6
four_open_label = 7
five_open_label = 8
all_fingers_closed_label = 9
grasp_label = 10
pick_label = 11

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



# This method is responsible for training EMG data
def Train(conc_array):
    global training_set
    global index_open_training_set, middle_open_training_set, thumb_open_training_set, ring_open_training_set, pinky_open_training_set, verification_set
    global two_open_training_set, three_open_training_set, four_open_training_set,five_open_training_set,all_fingers_closed_training_set,grasp_training_set,pick_training_set
    global number_of_samples,size,number_of_channels
    labels=[]
    shape1=int(conc_array.size/(size*8))
    conc_array=np.reshape(conc_array, (shape1,size,8))    
    print(conc_array,conc_array.shape)
    for i in range(0,12):
        for j in range(0,(int(number_of_samples/20))):
            labels.append(i)
    labels = np.asarray(labels)
    labels = np.reshape(labels,(labels.size,1))
    print(labels, len(labels),type(labels))
    permutation_function = np.random.permutation(conc_array.shape[0])
    total_samples = conc_array.shape[0]
    all_shuffled_data,all_shuffled_labels = np.zeros((total_samples,8)),np.zeros((total_samples,8))
    all_shuffled_data,all_shuffled_labels = conc_array[permutation_function],labels[permutation_function]
    print(all_shuffled_data.shape)
    print(all_shuffled_labels.shape)
    number_of_training_samples = np.int(np.floor(0.8*total_samples))   
    train_data = np.zeros((number_of_training_samples,size,8))
    train_labels = np.zeros((number_of_training_samples,size,8))
    print("TS ", number_of_training_samples, " S " , number_of_samples)
    number_of_validation_samples = np.int(total_samples-number_of_training_samples)
    train_data = all_shuffled_data[0:number_of_training_samples,:]
    train_labels = all_shuffled_labels[0:number_of_training_samples,]
    print("Length of train data is ", train_data.shape, " train labels is " , train_labels.shape)
    validation_data = all_shuffled_data[number_of_training_samples:total_samples,:]
    validation_labels = all_shuffled_labels[number_of_training_samples:total_samples,]
    print("Length of validation data is ", validation_data.shape , " validation labels is " , validation_labels.shape)
    print(train_labels)
    
    model = Sequential()
    model.add(LSTM(50,input_shape=(size,8),return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(32,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(12,activation='softmax'))
    adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=1e-7, amsgrad=False)
    model.compile(optimizer=adam_optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
        
    history = model.fit(train_data, train_labels, epochs=20,validation_data=(validation_data,validation_labels),batch_size=16)
    model.save('C:/Users/m/Desktop/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand-master/'+name+'_realistic_model.h5')

    averages = number_of_samples/50
    # Initializing array for verification_averages
    verification_averages = np.zeros((int(averages),8))
    
    
    while True:
        while True:
            try:
                input("Hold a finger movement and press enter to get its classification")
                hub = myo.Hub()        
                listener = Listener(number_of_samples)
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
        div = int(50*number_of_samples/1000)
        # We add one because iterator below starts from 1
        batches = int(number_of_samples/div) + 1
        for i in range(1,batches):
            verification_averages[i-1,:] = np.mean(verification_set[(i-1)*div:i*div,:],axis=0)
        verification_data = np.reshape(np.asarray(verification_averages),(1,size,number_of_channels))
        print("Verification matrix shape is " , verification_data.shape)
        
        predictions = model.predict(verification_data,batch_size=16)
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
        else:
            pass


def main():
    unrecognized_training_set = np.zeros((8,number_of_samples))
    index_open_training_set = np.zeros((8,number_of_samples))
    middle_open_training_set = np.zeros((8,number_of_samples))
    thumb_open_training_set = np.zeros((8,number_of_samples))
    ring_open_training_set = np.zeros((8,number_of_samples))
    pinky_open_training_set = np.zeros((8,number_of_samples))
    two_open_training_set = np.zeros((8,number_of_samples))
    three_open_training_set = np.zeros((8,number_of_samples))
    four_open_training_set = np.zeros((8,number_of_samples))
    five_open_training_set = np.zeros((8,number_of_samples))
    all_fingers_closed_training_set = np.zeros((8,number_of_samples))
    grasp_training_set = np.zeros((8,number_of_samples))
    pick_training_set = np.zeros((8,number_of_samples))
    verification_set = np.zeros((8,number_of_samples))
    training_set = np.zeros((8,number_of_samples))
    # This function kills Myo Connect.exe and restarts it to make sure it is running
    # Because sometimes the application does not run even when Myo Connect process is running
    # So i think its a good idea to just kill if its not running and restart it

    while(restart_process()!=True):
        pass
    # Wait for 3 seconds until Myo Connect.exe starts
    time.sleep(3)
    
    # Initialize the SDK of Myo Armband
    myo.init(r'C:\Users\m\Desktop\myo-sdk-win-0.9.0\bin\myo64.dll')
    hub = myo.Hub()
    listener = Listener(number_of_samples)

    legend = ['Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6','Sensor 7','Sensor 8']

    ################## HERE WE GET TRAINING DATA FOR THUMB FINGER OPEN ########
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Open THUMB ")    
            hub.run(listener.on_event,20000)
            thumb_open_training_set = np.array((data_array[0]))
            print(thumb_open_training_set.shape)
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
            input("Open index finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            # Here we send the received number of samples making them a list of 1000 rows 8 columns 
            index_open_training_set = np.array((data_array[0]))            
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
            input("Open MIDDLE finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            middle_open_training_set = np.array((data_array[0]))
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
            input("Open Ring finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            ring_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR PINKY FINGER OPEN ####################
    while True:
        try:
            input("Open Pinky finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            pinky_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR TWO FINGER OPEN ####################
    while True:
        try:
            
            input("Open Two fingers")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            two_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR THREE FINGER OPEN ####################
    while True:
        try:
            input("Open Three fingers")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            three_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR THREE FINGER OPEN ####################
    while True:
        try:            
            input("Open Four fingers")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            four_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR FIVE FINGER OPEN ####################
    while True:
        try:
            input("Open Five fingers")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            five_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR ALL FINGERS CLOSED ####################
    while True:
        try:
            input("Make all fingers closed")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            all_fingers_closed_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR GRASP MOVEMENT ####################
    while True:
        try:
            input("Make Grasp movement")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            grasp_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR PICK MOVEMENT ####################
    while True:
        try:
            input("Make Pick movement")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            pick_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)         
        
    # Here we stack all the data row wise
    conc_array = np.concatenate([
            index_open_training_set,
            middle_open_training_set,
            thumb_open_training_set,
            ring_open_training_set,
            pinky_open_training_set,
            two_open_training_set,
            three_open_training_set,
            four_open_training_set,
            five_open_training_set,
            all_fingers_closed_training_set,
            grasp_training_set,
            pick_training_set,
        ],axis=0)
    print(conc_array.shape)
    np.savetxt('C:/Users/m/Desktop/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand-master/'+name+'.txt', conc_array, fmt='%i')
    # In this method the EMG data gets trained and verified
    Train(conc_array)

if __name__ == '__main__':
    main()
