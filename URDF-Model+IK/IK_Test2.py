import pybullet as p
import time

coordinate=[.15,.18,.14]

file_name = "5DOFArm.urdf"
p.connect(p.GUI)
arm = p.loadURDF(file_name, useFixedBase=1)


numJoints = p.getNumJoints(arm)
for i in range(numJoints):
    print(p.getJointInfo(arm,i))
    

angle1, angle2, angle3, angle4, angle5=p.calculateInverseKinematics(arm,6,coordinate,residualThreshold=0.001)
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
                        jointIndex=3,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle3,
                        force=20)


p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=4,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle4,
                        force=20)

p.setJointMotorControl2(bodyIndex=arm,
                        jointIndex=6,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle5,
                        force=20)

print(angle1, angle2, angle3, angle4, angle5)
while True:

    p.stepSimulation()
    print(p.getLinkState(arm,6,computeForwardKinematics=1))
    time.sleep(0.1)