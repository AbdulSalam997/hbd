
from cvzone.HandTrackingModule import HandDetector
import cv2
import math
import time
import numpy as np
from ffpyplayer.player import MediaPlayer


current_milli_time = lambda: int(round(time.time() * 1000))

filename = 'hbdS.mp4'
cap_vid = cv2.VideoCapture(filename)
max_time = 1000 * cap_vid.get(cv2.CAP_PROP_FRAME_COUNT) / cap_vid.get(cv2.CAP_PROP_FPS)


height = int(cap_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap_vid.get(cv2.CAP_PROP_FRAME_WIDTH))

start = current_milli_time()

showSkeleton = False
while True:
    if input("Enter our code:").lower() == "rnask":
        print("Welcome My Queen")
        break
    else:
        print("Wrong code")
        
if int(input("1. Wanna see the magic? \n2. Interested in behind the scenes? \n")) == 2:
    showSkeleton = True


print("Hold Tight!!...")
cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8, maxHands=2)

showPlay = True
showRePlay = False
showBoxes = False
showTease = False
replayed = False
showGift = False
giftGrabbed = False
showVideo = False
audioplayed = False

logo = cv2.imread('box.jpg')
size = 200
logo = cv2.resize(logo, (size, size))

logo2 = cv2.imread('box.jpg')
# size = 200
logo2 = cv2.resize(logo2, (size, size))

logo3 = cv2.imread('box.jpg')
# size = 200
logo3 = cv2.resize(logo3, (size, size))

tease = cv2.imread('tease.jpg')
# size = 200
tease = cv2.resize(tease, (size, size))

gift = cv2.imread('owlGift.jpg')
# size = 200
gift = cv2.resize(gift, (size, size))

img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

counter = 0

while True:
    if not audioplayed:
        if counter >= 200:
            player = MediaPlayer('hbdS.mp4')
            audioplayed = True
    color = (255, 0, 0)
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX      
    try:
        success, img = cap.read()
        if showSkeleton:
            hands, img = detector.findHands(cv2.flip(img, 1), flipType=False) 
        else:
            img = cv2.flip(img,1)
            hands = detector.findHands(img, flipType=False,draw = False)
        # print(hands)
        # print(img)
        if showPlay:
            cv2.rectangle(img,(1000,250),(1150,290),(0,0,255),cv2.FILLED)
            cv2.putText(img, 'Play', (1035, 280), font, 1, (255, 255, 255), thickness=2)
        
        
        if showRePlay:
            cv2.rectangle(img,(1000,250),(1150,290),(0,0,255),cv2.FILLED)
            cv2.putText(img, 'Re-Play', (1000, 280), font, 1, (255, 255, 255), thickness=2)
            
        cv2.putText(img,'Welcome My Love!',(450,50), font, 1, (255,51,51),thickness=2)
        if hands:
            # Hand 1
            hand1 = hands[0]
            # print(hand1)
            hand1["type"] = ""
            lmList1 = hand1["lmList"] 
            cv2.putText(img, ".", (5, 10), font, 1, (0, 255, 0), thickness=2)
            dist = math.sqrt((hand1['center'][0] - lmList1[8][0])** 2 + (hand1['center'][1] - lmList1[8][1])** 2)
            if dist < 100 and showPlay == False and showRePlay == False  and showBoxes == False:
                showGift = False
                giftGrabbed = True
                print("gift grabbed")
            
            if giftGrabbed and dist > 120 and showPlay == False and showRePlay == False and showGift == False and showBoxes == False:
                print("happy birthday")
                showVideo = True
                giftGrabbed = True
                showGift = False
            # cv2.putText(img,str(dist),(5,100), font, 1, (0,255,0),thickness=2)
            # cv2.putText(img,str(trial),(150,450), font, 1, (255,51,51),thickness=2)
            # cv2.putText(img, str(), (150, 250), font, 1, (255, 51, 51), thickness=2)
            
            if 1000 < lmList1[8][0] < 1150 and 250 < lmList1[8][1] < 290: #for play action
                showPlay = False
                showBoxes = True

            if 1000 < lmList1[8][0] < 1150 and 250 < lmList1[8][1] < 290 and showPlay == False and showTease: #for replay action
                showRePlay = False
                showBoxes = True
                showTease = False
                replayed = True

            if 700 < hand1['center'][0]  < 1000 and 100 < hand1['center'][1]  < 300:
                color = (0, 255, 0)
            
            if showBoxes or replayed:
                if 200 < lmList1[8][0] < 400 and 100 < lmList1[8][1] < 300:  # for box one
                    if not showTease:
                        if not replayed:
                            showTease = True
                            showRePlay = True
                        else:
                            color = (0,255,0)
                        showBoxes = False
                        if replayed and  not giftGrabbed:
                            showGift = True
                if 500 < lmList1[8][0] < 700 and 100 < lmList1[8][1] < 300:  # for box two
                    if not showTease:
                        if not replayed:
                            showTease = True
                            showRePlay = True
                        else:
                            color = (0,255,0)
                        showBoxes = False
                        if replayed and not giftGrabbed:
                            showGift = True

                if 800 < lmList1[8][0] < 1000 and 100 < lmList1[8][1] < 300:  # for box three
                    if not showTease:
                        if not replayed:
                            showTease = True
                            showRePlay = True
                        else:
                            color = (0,255,0)
                        showBoxes = False
                        if replayed and not giftGrabbed:
                            showGift = True

            if showSkeleton:
                cv2.circle(img,center=(lmList1[8][0],lmList1[8][1]),radius=5,color=color)
                cv2.circle(img, center=hand1['center'], radius=5, color=color)
            
            
            
            bbox1 = hand1["bbox"]  
            centerPoint1 = hand1['center'] 
            handType1 = hand1["type"] 

            fingers1 = detector.fingersUp(hand1)
            
        if showBoxes:
            roi = img[-size-400:-400, -size-900:-900]
            roi2 = img[-size-400:-400, -size-600:-600]
            roi3 = img[-size-400:-400, -size-300:-300]
        
            roi[np.where(mask)] = 0
            roi += logo
            roi2[np.where(mask)] = 0
            roi2 += logo2
            roi3[np.where(mask)] = 0
            roi3 += logo3
        
        if showTease:
            roi2 = img[-size - 400:-400, -size - 600:-600]
            roi2[np.where(mask)] = 0
            roi2 += tease

        if showGift:
            roi2 = img[-size - 400:-400, -size - 600:-600]
            roi2[np.where(mask)] = 0
            roi2 += gift

        # cv2.rectangle(img,(700,100),(1000,300),color)
        
        if showVideo:
            counter += 5
            if counter >= 30:
                ret, frame_vid = cap_vid.read()
                if audioplayed:
                    audio_frame, val = player.get_frame()
                frame_vid = cv2.resize(frame_vid,(1280,720))
                tr = 1 
                img = ((1 - tr) * img.astype(np.float) + tr * frame_vid.astype(np.float)).astype(np.uint8)
                cv2.imshow('Happy Birthday sunshine', img)
                if audioplayed:
                    if val != 'eof' and audio_frame is not None:
                        img, t = audio_frame
                    else:
                        if val == 'eof':
                            break
            else:
                cv2.imshow("Happy Birthday sunshine",img)
        else:
            cv2.imshow("Happy Birthday sunshine",img)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    except Exception as e:
        print(e)

cap.release()
cv2.destroyAllWindows()
exit()