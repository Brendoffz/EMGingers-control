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
global imu_array

save_path = r'C:\Users\m\Desktop\DM2008\Mid-Term\EMG'
sdk_path = r'D:\Projects\EMGingers-control\Robotic-Hand-Machine-Learning'

frequencyofArmband=200 #Fixed Value
number_of_channels =8 #Fixed Value
recordingInterval=30 #In Seconds
number_of_samples = frequencyofArmband*recordingInterval
frequencyofInertial= 50
number_of_inertial = 4
number_of_samples_inertial = frequencyofInertial*recordingInterval
data_array=[]
imu_array=[]
size=100 #Response of hand movement depends on the sampling size, Current size is 100.
gestures=13 #Rest and 12 other gestures
hub_data = 200000000
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
    
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n1)
        self.imu_data_queue = deque(maxlen=n2)

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
            
            if len(list(self.emg_data_queue))>=self.n1:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False
            
    def on_orientation(self, event):
        arr1=[event.orientation[0],event.orientation[1],event.orientation[2],event.orientation[3]]
        self.imu_data_queue.append(arr1)
        if len(list(self.imu_data_queue))>=self.n2:
            imu_array.append(list(self.imu_data_queue))
            self.imu_data_queue.clear()
            

def main():
    while(restart_process()!=True):
        pass
# Wait for 3 seconds until Myo Connect.exe starts
    time.sleep(3)
    
    # Initialize the SDK of Myo Armband
    
    myo.init(sdk_path+r'\myo-sdk-win-0.9.0\bin\myo64.dll')
    # Change as needed
    hub = myo.Hub()
    listener = Listener(number_of_samples,number_of_samples_inertial)
    
    legend = ['Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6','Sensor 7','Sensor 8']
    
    ################## HERE WE GET TRAINING DATA FOR THUMB FINGER OPEN ########
    while True:
        try:
            hub = myo.Hub()
            input("Open THUMB ")    
            hub.run(listener.on_event,hub_data)
            thumb_open_training_set = np.array((data_array[0]))
            print(thumb_open_training_set.shape)
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            thumb_open_training_set_ori = np.array(ori_cache)
            print(thumb_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            # Here we send the received number of samples making them a list of 1000 rows 8 columns 
            index_open_training_set = np.array((data_array[0]))          
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            index_open_training_set_ori = np.array(ori_cache)
            print(index_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            middle_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            middle_open_training_set_ori = np.array(ori_cache)
            print(middle_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            ring_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            ring_open_training_set_ori = np.array(ori_cache)
            print(ring_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            pinky_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            pinky_open_training_set_ori = np.array(ori_cache)
            print(pinky_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            two_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            two_open_training_set_ori = np.array(ori_cache)
            print(two_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            three_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            three_open_training_set_ori = np.array(ori_cache)
            print(three_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            four_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            four_open_training_set_ori = np.array(ori_cache)
            print(four_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            five_open_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            five_open_training_set_ori = np.array(ori_cache)
            print(five_open_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            all_fingers_closed_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            all_fingers_closed_training_set_ori = np.array(ori_cache)
            print(all_fingers_closed_training_set_ori.shape)
            imu_array.clear()
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
            hub.run(listener.on_event,hub_data)
            grasp_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            grasp_training_set_ori = np.array(ori_cache)
            print(grasp_training_set_ori.shape)
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
            hub.run(listener.on_event,hub_data)
            pick_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            pick_training_set_ori = np.array(ori_cache)
            print(pick_training_set_ori.shape)
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)        
    
    ################### HERE WE GET TRAINING DATA FOR RELAX MOVEMENT ####################
    while True:
        try:
            input("Make Relax movement")
            hub.run(listener.on_event,hub_data)
            relax_training_set = np.array((data_array[0]))
            data_array.clear()
            
            ori_cache=[]
            num=np.array(imu_array[0]).shape[0]
            for i in range(num):
                add=[imu_array[0][i],imu_array[0][i],imu_array[0][i],imu_array[0][i]]
                ori_cache.extend(add)
                i+4
            relax_training_set_ori = np.array(ori_cache)
            print(relax_training_set_ori.shape)
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)           
    # Here we stack all the data row wise
    conc_array = np.concatenate([
            thumb_open_training_set,
            index_open_training_set,
            middle_open_training_set,
            ring_open_training_set,
            pinky_open_training_set,
            two_open_training_set,
            three_open_training_set,
            four_open_training_set,
            five_open_training_set,
            all_fingers_closed_training_set,
            grasp_training_set,
            pick_training_set,
            relax_training_set,
        ],axis=0)
    print(conc_array.shape)
    conc_array1 = np.concatenate([
            thumb_open_training_set_ori,
            index_open_training_set_ori,
            middle_open_training_set_ori,
            ring_open_training_set_ori,
            pinky_open_training_set_ori,
            two_open_training_set_ori,
            three_open_training_set_ori,
            four_open_training_set_ori,
            five_open_training_set_ori,
            all_fingers_closed_training_set_ori,
            grasp_training_set_ori,
            pick_training_set_ori,
            relax_training_set_ori,
        ],axis=0)
    #change as needed 
    # In this method the EMG data gets trained and verified
    Train(conc_array,conc_array1)

# This method is responsible for training EMG data
def Train(conc_array,conc_array1):
    train_size =.8
    global training_set,gestures
    global index_open_training_set, middle_open_training_set, thumb_open_training_set, ring_open_training_set, pinky_open_training_set, verification_set
    global two_open_training_set, three_open_training_set, four_open_training_set,five_open_training_set,all_fingers_closed_training_set,grasp_training_set,pick_training_set
    global number_of_samples,size,number_of_channels
    labels=[]
    print(conc_array.size)
    TrainingSamples=int(conc_array.size/(size*number_of_channels)) #TrainingSample is the number of train data, size is the length of each data, 8 is channel of data
    print(conc_array1.size)
    TrainingSamples1=int(conc_array1.size/(size*number_of_inertial)) #TrainingSample is the number of train data, size is the length of each data, 8 is channel of data
    
    conc_array=np.reshape(conc_array, (TrainingSamples,size,number_of_channels))
    print(conc_array,conc_array.shape)
    
    conc_array1=np.reshape(conc_array1, (TrainingSamples1,size,number_of_inertial))
    print(conc_array1,conc_array1.shape)
    
    for i in range(0,gestures):
        for j in range(0,(int(TrainingSamples/gestures))):
            labels.append(i)
    conc_array= np.concatenate((conc_array,conc_array1),axis=2)
    print(conc_array,conc_array.shape)
    labels = np.asarray(labels)
    train_data, validation_data,train_labels,validation_labels = train_test_split(conc_array, labels, train_size=.8, random_state = 3,stratify=labels)
    np.savetxt(save_path+'train_data.csv',train_data.reshape(len(train_data),size*(number_of_channels+number_of_inertial)), delimiter=',')
    np.savetxt(save_path+'validation_data.csv', validation_data.reshape(len(validation_data),size*(number_of_channels+number_of_inertial)), delimiter=',')
    np.savetxt(save_path+'train_labels.csv', train_labels, delimiter=',')
    np.savetxt(save_path+'validation_labels.csv', validation_labels, delimiter=',')
    
    train_labels = np.reshape(train_labels,(train_labels.size,1))
    validation_labels = np.reshape(validation_labels,(validation_labels.size,1))
    
    
    
    print("TS ", TrainingSamples, " S " , number_of_samples)
    print("Length of train data is ", train_data.shape, " train labels is " , train_labels.shape)
    print("Length of validation data is ", validation_data.shape , " validation labels is " , validation_labels.shape)
    print(train_labels)
    
    model = Sequential()
    model.add(LSTM(50,input_shape=(size,number_of_channels+number_of_inertial),return_sequences=True))
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
    model.save(save_path+name+'_realistic_model.h5')
    #change as needed 

    
    

if __name__ == '__main__':
    main()

    
