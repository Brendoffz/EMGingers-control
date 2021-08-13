import pybullet as p
import time
import pybullet_data
import os
p.connect(p.GUI)
coordinate=[2,1,3]

p.loadURDF(os.path.join(pybullet_data.getDataPath(), "plane.urdf"), 0, 0, 0)
orn = p.getQuaternionFromEuler([0, 0, 0])
arm=p.loadURDF("Arm2.urdf", useFixedBase=1)
numJoints = p.getNumJoints(arm)
for i in range(numJoints):
    print(p.getJointInfo(arm,i))
    
p.setGravity(0, 0, 0)


angle1, angle2, angle3, angle4=p.calculateInverseKinematics(arm,7,coordinate)
p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=0,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle1,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=2,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle2,
                        force=20)
p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=5,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle3,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=7,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle4,
                        force=20)
while True:

    p.stepSimulation()
    print(p.getLinkState(arm,7,computeForwardKinematics=1))
    #time.sleep(1. / 240000.)