from cvzone.HandTrackingModule import HandDetector
import cv2 as cv


frame = None
key = None

fingerDetector = HandDetector(detectionCon=0.7, maxHands=1)
cap=cv.VideoCapture(1)
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
        #fingers = fingerDetector.fingersUp(hand1)
        #print(fingers)
    
    cv.imshow("Hand Video",frame)
    key = cv.waitKey(500)
    if key == (ord('q')):
        break
    
    
cv.destroyAllWindows()
