import pybullet as p
import time
import serial
coordinate=[.150,.120,0.000]
rawdata=[]
file_name = "RoboticArmFinalURDF.urdf"
p.connect(p.GUI)
arm = p.loadURDF(file_name, useFixedBase=1)

esp=serial.Serial('COM5',115200,timeout=.1)

numJoints = p.getNumJoints(arm)
for i in range(numJoints):
    print(p.getJointInfo(arm,i))
    
    
angle1, angle2, angle3, angle4, angle5=p.calculateInverseKinematics(arm,4,coordinate)
p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=0,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle1,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=1,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle2,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=2,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle3,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=3,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle4,
                        force=20)


p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=4,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle5,
                        force=20)

print(angle1, angle2, angle3, angle4, angle5)
previoustime=0
interval=0.1
previoustime2=0
interval2=0.5
while True:
    
    if (time.time()>previoustime+interval):
        p.stepSimulation()
        previoustime=time.time()
        #print("FK")
        #print(p.getLinkState(arm,4,computeForwardKinematics=1))
        

    if(time.time()>previoustime2+interval2): 
         previoustime2=time.time()       
         coordinate=str(esp.readline().strip().decode("utf-8")).split(',')
         try:
             coordinate[0]=float(coordinate[0])/100
             coordinate[1]=float(coordinate[1])/100
             coordinate[2]=float(coordinate[2])/100
         except:
             print("An exception occurred") 
             coordinate=[.150,.120,0.000]
         print("coordinate")
         print(coordinate)
         
         angleA, angleB, angleC, angleD, angleE=p.calculateInverseKinematics(arm,4,coordinate)
         p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=0,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angleA,
                        force=20)

         p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=1,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angleB,
                        force=20)

         p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=2,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angleC,
                        force=20)

         p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=3,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angleD,
                        force=20)


         p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=4,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angleE,
                        force=20)
         print(angleA, angleB, angleC, angleD, angleE)
         values = bytearray([angleA, angleB, angleC, angleD, angleE])
         esp.write(values)
    