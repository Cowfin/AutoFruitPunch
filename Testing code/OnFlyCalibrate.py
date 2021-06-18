import cv2
import numpy as np

count = 0

#Gets camera feed
cap = cv2.VideoCapture(0)

def window_maker(fruitName, lh,ls,lv,uh,us,uv):
    cv2.namedWindow(fruitName)
    cv2.createTrackbar("Low Hue", fruitName, lh, 255, nothing)
    cv2.createTrackbar("Low Sat", fruitName, ls, 255, nothing)
    cv2.createTrackbar("Low Value", fruitName, lv, 255, nothing)
    cv2.createTrackbar("Up Hue", fruitName, uh, 255, nothing)
    cv2.createTrackbar("Up Sat", fruitName, us, 255, nothing)
    cv2.createTrackbar("Up Value", fruitName, uv, 255, nothing)


def nothing(x):
    pass

window_maker("Lemon",25,30,0,65,255,255)
window_maker("Strawberry",0,30,30,9,255,255)
window_maker("Banana",10,45,45,25,255,255)
window_maker("Plum",130,15,0,200,180,190)


#Creates windows of sliders that are the HSV values for easy colour masking

#cv2.namedWindow("Lemon")
#cv2.createTrackbar("Low Hue", "Lemon", 25, 255, nothing)
#cv2.createTrackbar("Low Sat", "Lemon", 30, 255, nothing)
#cv2.createTrackbar("Low Value", "Lemon", 0, 255, nothing)
#cv2.createTrackbar("Up Hue", "Lemon", 65, 255, nothing)
#cv2.createTrackbar("Up Sat", "Lemon", 255, 255, nothing)
#cv2.createTrackbar("Up Value", "Lemon", 255, 255, nothing)

#cv2.namedWindow("Strawberry")
#cv2.createTrackbar("Low Hue", "Strawberry", 0, 255, nothing)
#cv2.createTrackbar("Low Sat", "Strawberry", 30, 255, nothing)
#cv2.createTrackbar("Low Value", "Strawberry", 30, 255, nothing)
#cv2.createTrackbar("Up Hue", "Strawberry", 9, 255, nothing)
#cv2.createTrackbar("Up Sat", "Strawberry", 255, 255, nothing)
#cv2.createTrackbar("Up Value", "Strawberry", 255, 255, nothing)

#cv2.namedWindow("Banana")
#cv2.createTrackbar("Low Hue", "Banana", 10, 255, nothing)
#cv2.createTrackbar("Low Sat", "Banana", 45, 255, nothing)
#cv2.createTrackbar("Low Value", "Banana", 45, 255, nothing)
#cv2.createTrackbar("Up Hue", "Banana", 25, 255, nothing)
#cv2.createTrackbar("Up Sat", "Banana", 255, 255, nothing)
#cv2.createTrackbar("Up Value", "Banana", 255, 255, nothing)

#cv2.namedWindow("Plum")
#cv2.createTrackbar("Low Hue", "Plum", 130, 255, nothing)
#cv2.createTrackbar("Low Sat", "Plum", 15, 255, nothing)
#cv2.createTrackbar("Low Value", "Plum", 0, 255, nothing)
#cv2.createTrackbar("Up Hue", "Plum", 200, 255, nothing)
#cv2.createTrackbar("Up Sat", "Plum", 180, 255, nothing)
#cv2.createTrackbar("Up Value", "Plum", 190, 255, nothing)



#Creates detector with parameters
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000 #will depend on camera distance
params.filterByColor = True
params.blobColor = 255 #light colours
params.filterByConvexity = True
params.minConvexity = 0.4 #higher = more uniform round   lower = more bumpy   max: 1
params.filterByInertia = True
params.minInertiaRatio = 0.4 #higher = more uniform round   lower = more oval like  max:1

detector = cv2.SimpleBlobDetector_create(params)

#Bananas are annoying cause they're a different shape so we need to make different parameters for it
params_banana = cv2.SimpleBlobDetector_Params()
params_banana.filterByArea = True
params_banana.minArea = 650
params_banana.filterByColor = True
params_banana.blobColor = 255
params_banana.filterByConvexity = True
params_banana.minConvexity = 0.05
params_banana.filterByInertia = True
params_banana.minInertiaRatio = 0.05

detector_banana = cv2.SimpleBlobDetector_create(params_banana)

while True:
    #Converts camera feed to colour image
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Different Hue Saturation Values for each fruit and creates a mask only allowing those colours through
    lower_lemon = np.array([cv2.getTrackbarPos("Low Hue","Lemon"), cv2.getTrackbarPos("Low Sat","Lemon"), cv2.getTrackbarPos("Low Value","Lemon")])
    upper_lemon = np.array([cv2.getTrackbarPos("Up Hue","Lemon"), cv2.getTrackbarPos("Up Sat","Lemon"), cv2.getTrackbarPos("Up Value","Lemon")])
    mask_lemon = cv2.inRange(hsv, lower_lemon, upper_lemon)

    lower_strawberry = np.array([cv2.getTrackbarPos("Low Hue","Strawberry"), cv2.getTrackbarPos("Low Sat","Strawberry"), cv2.getTrackbarPos("Low Value","Strawberry")])
    upper_strawberry = np.array([cv2.getTrackbarPos("Up Hue","Strawberry"), cv2.getTrackbarPos("Up Sat","Strawberry"), cv2.getTrackbarPos("Up Value","Strawberry")])
    mask_strawberry = cv2.inRange(hsv, lower_strawberry, upper_strawberry)

    lower_banana = np.array([cv2.getTrackbarPos("Low Hue","Banana"), cv2.getTrackbarPos("Low Sat","Banana"), cv2.getTrackbarPos("Low Value","Banana")])
    upper_banana = np.array([cv2.getTrackbarPos("Up Hue","Banana"), cv2.getTrackbarPos("Up Sat","Banana"), cv2.getTrackbarPos("Up Value","Banana")])
    mask_banana = cv2.inRange(hsv, lower_banana, upper_banana)

    lower_plum = np.array([cv2.getTrackbarPos("Low Hue","Plum"), cv2.getTrackbarPos("Low Sat","Plum"), cv2.getTrackbarPos("Low Value","Plum")])
    upper_plum = np.array([cv2.getTrackbarPos("Up Hue","Plum"), cv2.getTrackbarPos("Up Sat","Plum"), cv2.getTrackbarPos("Up Value","Plum")])
    mask_plum = cv2.inRange(hsv, lower_plum, upper_plum)

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
        count += 1
        if (count >= 2):
            count -= 1
        if (count < 0):
            count = 0
    else:
        count -= 1

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