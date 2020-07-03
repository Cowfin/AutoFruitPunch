import cv2
import numpy as np
import serial

#Initializes serial communication
ser = serial.Serial('COM4', 9600)

#Gets camera feed
cap = cv2.VideoCapture(0)

#Creates detector with parameters
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000 #will depend on camera distance
params.filterByColor = True
params.blobColor = 255 #light colours
params.filterByConvexity = True
params.minConvexity = 0.8 #higher = more uniform round   lower = more bumpy   max: 1
params.filterByInertia = True
params.minInertiaRatio = 0.5 #higher = more uniform round   lower = more oval like  max:1

detector = cv2.SimpleBlobDetector_create(params)

#Bananas are annoying cause they're a different shape so we need to make different parameters for it
params_banana = cv2.SimpleBlobDetector_Params()
params_banana.filterByArea = True
params_banana.minArea = 600
params_banana.filterByColor = True
params_banana.blobColor = 255
params_banana.filterByConvexity = True
params_banana.minConvexity = 0
params_banana.filterByInertia = True
params_banana.minInertiaRatio = 0.07

detector_banana = cv2.SimpleBlobDetector_create(params_banana)

while True:
    #Converts camera feed to colour image
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Different Hue Saturation Values for each fruit and creates a mask only allowing those colours through
    lower_lemon = np.array([23, 60, 0])
    upper_lemon = np.array([120, 255, 170])
    mask_lemon = cv2.inRange(hsv, lower_lemon, upper_lemon)

    lower_plum = np.array([130, 15, 0])
    upper_plum = np.array([200, 180, 190])
    mask_plum = cv2.inRange(hsv, lower_plum, upper_plum)

    lower_banana = np.array([10, 45, 45])
    upper_banana = np.array([25, 255, 255])
    mask_banana = cv2.inRange(hsv, lower_banana, upper_banana)

    lower_strawberry = np.array([0, 30, 30])
    upper_strawberry = np.array([9, 255, 255])
    mask_strawberry = cv2.inRange(hsv, lower_strawberry, upper_strawberry)

    #Blurs the mask to remove any noise and fills any holes in the mask
    blur_strawberry = cv2.medianBlur(mask_strawberry, 15)
    blur_lemon = cv2.medianBlur(mask_lemon, 15)
    blur_banana = cv2.medianBlur(mask_banana, 15)
    blur_plum = cv2.medianBlur(mask_plum, 15)
    
    #Detects the blurred blobs and counts them
    keypoints_strawberry = detector.detect(blur_strawberry)
    keypoints_lemon = detector.detect(blur_lemon)
    keypoints_plum = detector.detect(blur_plum)
    keypoints_banana = detector_banana.detect(blur_banana)

    print("Strawberry: " + str(len(keypoints_strawberry)))
    print("Lemon: " + str(len(keypoints_lemon)))
    print("Banana: " + str(len(keypoints_banana)))
    print("Plum: " + str(len(keypoints_plum)))

    #Determines whether 5 of a fruit is on the field if so then communicate with the Arduino
    if ((len(keypoints_strawberry) == 5) or (len(keypoints_lemon) == 5) or (len(keypoints_banana) == 5) or (len(keypoints_plum) == 5) ):
        ser.write(b'o')

    #Draws on the original image where fruits are detected
    imgKeyPoints = cv2.drawKeypoints(img, keypoints_strawberry, np.array([]), (255, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    imgKeyPoints = cv2.drawKeypoints(imgKeyPoints, keypoints_lemon, np.array([]), (255, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    imgKeyPoints = cv2.drawKeypoints(imgKeyPoints, keypoints_banana, np.array([]), (255, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    imgKeyPoints = cv2.drawKeypoints(imgKeyPoints, keypoints_plum, np.array([]), (255, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #Displays the different camera feeds.
    cv2.imshow("keypoints", imgKeyPoints)
    cv2.imshow('lemon', blur_lemon)
    cv2.imshow('strawberry', blur_strawberry)
    cv2.imshow('banana', blur_banana)
    cv2.imshow('plum', blur_plum)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()