from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import requests 
import requests as reqs 
url1="http://192.168.10.104/get?input1="
url2="http://192.168.10.104/get?input2="
url3="http://192.168.10.104/get?input3="
url4="http://192.168.10.104/get?input4="
url5="http://192.168.10.104/get?input5="
frame = None
key = None

fingerDetector = HandDetector(detectionCon=0.7, maxHands=1)
cap=cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 2560)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 960)


while 1:
    success, frame = cap.read()
    #frame = cv.flip(frame, 1)
    hands, frame = fingerDetector.findHands(frame)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        boundingBox1 = hand1["bbox"] 
        centerPoint1 = hand1["center"] 
        centerPoint1 = hand1["type"] 
        fingers = fingerDetector.fingersUp(hand1)
        print(fingers)
        reqs.get(url1+str(180*fingers[0]))
        reqs.get(url2+str(180*fingers[1])) 
        reqs.get(url3+str(180*fingers[2])) 
        reqs.get(url4+str(180*fingers[3])) 
        reqs.get(url5+str(180*fingers[4])) 
    
    cv.imshow("Hand Video",frame)
    key = cv.waitKey(500)
    
    if key == (ord('q')):
        break
    
    
cv.destroyAllWindows()
