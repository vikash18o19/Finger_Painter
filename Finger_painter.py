import cv2
import numpy as np

import os
import HandTrackingModule as htm


folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[2]

drawColor = (255,0,255)

###########
brushThickness = 15
flag = 0

##########
cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65,maxHands=1)

xp, yp = 0,0

imgCanvas = np.zeros((720,1280,3),np.uint8)
while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)


    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList)

        #tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]


        fingers = detector.fingersUp()
        #print(fingers)

        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(drawColor),cv2.FILLED)
            #print("selection mode")
            if y1 < 110:
                if 160<x1<320:
                    header = overlayList[0]
                    drawColor = (1,1,1)
                if 320<x1<640:
                    header = overlayList[3]
                    drawColor = (0, 0, 255)
                if 640<x1<800:
                    header = overlayList[4]
                    drawColor = (255, 255, 255)
                if 800<x1<1280:
                    header = overlayList[1]
                    drawColor = (0,0,0)


        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)
            #print("drawing mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            #if abs(x1-xp) > 1 or abs(x1-xp) >1:
            #    xp, yp = x1, y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, 100)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 100)
            else:
                cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

        if fingers[0] == True and fingers[1] == True and fingers[2] == True and fingers[3] == True and fingers[4] == True and flag ==0:
            flag=1
        if fingers[0] == False and fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == False and flag ==1:
            flag=2
        if fingers[0] == True and fingers[1] == True and fingers[2] == True and fingers[3] == True and fingers[4] == True and flag ==2:
            flag=3
        if fingers[0] == False and fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == False and flag ==3:
            flag=4
        #if fingers[0] == True and fingers[1] == True and fingers[2] == True and fingers[3] == True and fingers[4] == True and flag ==4:
            #break




    #imgGray = cv2.cvtColor()
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:110,0:1280] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("image",img)
    #cv2.imshow("Canvas", imgCanvas)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
