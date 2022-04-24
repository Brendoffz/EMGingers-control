from __future__ import print_function
from collections import deque
from threading import Lock, Thread
import numpy as np
import tensorflow as tf
import myo
import time
import psutil
import os


# This training set will contain 1000 samples of 8 sensor values
global number_of_samples
global verification_set1
global verification_set2
global data_array
global imu_array
global training_set
global number_of_samples
global index_training_set, middle_training_set,thumb_training_set,verification_set
global data_array
global imu_array
global training_set,gestures
global index_open_training_set, middle_open_training_set, thumb_open_training_set, ring_open_training_set, pinky_open_training_set, verification_set
global two_open_training_set, three_open_training_set, four_open_training_set,five_open_training_set,all_fingers_closed_training_set,grasp_training_set,pick_training_set
global number_of_samples,size,number_of_channels

frequencyofArmband=200 #Fixed Value
number_of_channels =8 #Fixed Value
recordingInterval=0.5 #In Seconds
number_of_samples = int(frequencyofArmband*recordingInterval)
frequencyofInertial= 50
number_of_inertial = 4
number_of_samples_inertial = int(frequencyofInertial*recordingInterval)
data_array=[]
imu_array=[]
size=100 #Response of hand movement depends on the sampling size, Current size is 100.
gestures=13 #Rest and 12 other gestures
hub_data = number_of_samples*number_of_channels

save_path = r'C:\Users\m\Desktop\DM2008\Mid-Term\EMG'
sdk_path = r'D:\Projects\EMGingers-control\Robotic-Hand-Machine-Learning'
model=tf.keras.models.load_model(r'C:\Users\m\Desktop\DM2008\Mid-Term\EMGTest1_realistic_model.h5')


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
                print(len(data_array))
                self.emg_data_queue.clear()
                return False
            
    def on_orientation(self, event):
        arr1=[event.orientation[0],event.orientation[1],event.orientation[2],event.orientation[3]]
        self.imu_data_queue.append(arr1)
        if len(list(self.imu_data_queue))>=self.n2:
            imu_array.append(list(self.imu_data_queue))
            print(len(imu_array))
            self.imu_data_queue.clear()



# This method is responsible for training EMG data
def Train():
    global number_of_samples
    while True:
        while True:
            try:
                hub = myo.Hub()
                listener = Listener(number_of_samples,number_of_samples_inertial) 
                hub.run(listener.on_event,hub_data)
                # Here we send the received number of samples making them a list of 1000 rows 8 columns
                verification_set1 = np.reshape(np.array((data_array[0])),(1,number_of_samples,number_of_channels)) 
                print(verification_set1.shape)
                verification_set2 = np.array((imu_array[0]))
                verification_set2 = np.repeat(verification_set2,4,axis=1)
                verification_set2 = np.reshape(verification_set2,(1,number_of_samples,number_of_inertial))
                print(verification_set2.shape)
                verification_data= np.concatenate((verification_set1,verification_set2),axis=2)
                print(verification_data.shape)
                data_array.clear()
                imu_array.clear()
                break
            except Exception as e:
                print(e)
                while(restart_process()!=True):
                    pass
                # Wait for 3 seconds until Myo Connect.exe starts
                time.sleep(3)
                
        verification_data
        
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
        elif predicted_value == 12:
            print("Resting")    
        else:
            pass


def main():
    # This function kills Myo Connect.exe and restarts it to make sure it is running
    # Because sometimes the application does not run even when Myo Connect process is running
    # So i think its a good idea to just kill if its not running and restart it

    while(restart_process()!=True):
        pass
    # Wait for 3 seconds until Myo Connect.exe starts
    time.sleep(3)
    
    # Initialize the SDK of Myo Armband
    myo.init(sdk_path+r'\myo-sdk-win-0.9.0\bin\myo64.dll')
    hub = myo.Hub()
    listener = Listener(number_of_samples,number_of_samples_inertial)        
    Train()

if __name__ == '__main__':
    main()
