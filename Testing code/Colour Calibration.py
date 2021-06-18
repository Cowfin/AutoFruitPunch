import cv2
import numpy as np

def nothing(x):
    pass

#Gets camera feed
cap = cv2.VideoCapture(0)

#Creates window of sliders that are the HSV values for easy colour masking
cv2.namedWindow("Colour picker")
cv2.createTrackbar("Low Hue", "Colour picker", 0, 255, nothing)
cv2.createTrackbar("Low Sat", "Colour picker", 0, 255, nothing)
cv2.createTrackbar("Low Value", "Colour picker", 0, 255, nothing)
cv2.createTrackbar("Up Hue", "Colour picker", 255, 255, nothing)
cv2.createTrackbar("Up Sat", "Colour picker", 255, 255, nothing)
cv2.createTrackbar("Up Value", "Colour picker", 255, 255, nothing)

while True:
    #Converts camera feed to colour image
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Pulls values from the sliders
    lh = cv2.getTrackbarPos("Low Hue","Colour picker")
    ls = cv2.getTrackbarPos("Low Sat","Colour picker")
    lv = cv2.getTrackbarPos("Low Value","Colour picker")
    
    uh = cv2.getTrackbarPos("Up Hue","Colour picker")
    us = cv2.getTrackbarPos("Up Sat","Colour picker")
    uv = cv2.getTrackbarPos("Up Value","Colour picker")

    #Assigns values to the colour range
    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    #Creates a mask of just the specified colour
    mask = cv2.inRange(hsv, lower, upper)
    #Removes everything from the picture that does not align with the mask
    res = cv2.bitwise_and(img, img, mask = mask)

    blur = cv2.medianBlur(mask, 15)

    cv2.imshow('blur', blur)

    #Displays original image, mask, result
    cv2.imshow('image', img)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()