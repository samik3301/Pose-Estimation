import cv2
import numpy as np
import time
import pose_module as pm

path = '/Users/samik/Desktop/Programming/Pose Estimation/test_footage.mp4'
cap= cv2.VideoCapture(path)


detector = pm.poseDetector()
count = 0 
dir = 0 # keeping 0 and 1 . 0 is when its going up and 1 is when its going down
#considering a full curl iff both directions are done ie 0 and 1
pTime = 0 #previous time - using to calculate the manual fps every frame

while True:
    
    sucess, img = cap.read()
    # if needed then can resize
    img = cv2.resize(img, (1280,720))

    
    #img = cv2.imread('/Users/samik/Desktop/Programming/Pose Estimation/bicep_curl_testing.jpg')
    img = detector.findPose(img,draw=False) #to just focus on points of interest we can set draw to False
    lmList = detector.findPosition(img,draw =False) #no need to draw

    
    #now have the list of landmarks in a list in a format [landmark_id, landmark_coordinate_x, landmark_coordinate_y]
    #print(lmList) #just to check if it's storing all the landmark points properly in the list

    if len(lmList)!=0:
        #Done for arms, adding more functionality and doing for legs -> check mediapipe documentation for the exact landmark positions
        #Odd landmark coordinates for the Left arm
        #angle= detector.findAngle(img, 11, 13, 15, draw=True)
        #Even landmark coordinates for the Right arm
        angle= detector.findAngle(img, 12, 14, 16, draw= True)

        #Converting the angle range from angle to some percentage
        per = np.interp(angle,(95,150),(0,100))
        #here 210 is the least angle thats going while doing a curl and similarly 315 is the max angle while doing a bicep curl
        #so converting that range into a percentage value from 0 to 100 using interp function (maps the change in 1 value to another wrt to first value)
        #print(angle,per)

        #making a visual bar to display the percentage change while doing a curl
        bar  = np.interp(angle, (95,150), (650,100)) #650 is the minimum value of the bar and 100 is the maximum value of the bar -> vertically obviously


        #Check for the curls here
        color  = (255,0,255)
        if per == 100:
            color = (0,255,0) #making it green when the percentage hits 100%
            if dir ==0:
                count +=0.5 #adding half to the count since full curl is not down
                dir =1 #change direction
        if per ==0:
            color = (255,0,0) #making it red when the percentage hits 0%
            if dir==1:
                count+= 0.5 #adding another half to the count since the curl is not up
                dir =0 #change direction
        #print(count)

        #making the percentage change with curl BAR on img
        cv2.rectangle(img, (1100,100), (1175,650), (0,255,0), 3)
        cv2.rectangle(img, (1100,int(bar)), (1175,650), color, cv2.FILLED)
        cv2.putText(img, str(int(per)),(1100,75),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
        #Can make separate bars for separate hands 


        #Displaying the curl count on the img
        cv2.putText(img, str(int(count)),(100,100),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)   #using int to round off the half curls
        #can put the fps inside a rectangular box forf presentation if needed - not necessary at all-> just presentation


    cTime = time.time() #The current time
    fps = 1/(cTime-pTime)
    ptiime = cTime
    cv2.putText(img, str(int(fps)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
    #resizing the stream affects the FPS, if original dimensions are used for the stream then high fps otherwise if the dimensions are reduced then will get a lower yet smooth fps


    cv2.imshow("Image",img)
    cv2.waitKey(1)