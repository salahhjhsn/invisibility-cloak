import cv2  # as cv
import time
import numpy as np

cap = cv2.VideoCapture(0)

time.sleep(1)
background = 0
background_timeout = 100

input("Pleas get out of the camera FoV and press enter")

# Acquire the background image in the beginning, timeout to let the camera start up properly
for x in range(background_timeout):
    ret, background = cap.read()
    if not ret:
        continue

# First red mask ranges
lower_red_one = np.array([0, 170, 70])  # 117, 234])
upper_red_one = np.array([2, 226, 255])

# Second red mask ranges, to avoid filtering augmented red colors
lower_red_two = np.array([177, 170, 70])  # 117, 234])
upper_red_two = np.array([180, 226, 255])

while(cap.isOpened()):
    err, img = cap.read()
    if not err:
        break
    cv2.imshow("Original Image", img)

    # BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generate masks based on the defined thresholds
    red_one = cv2.inRange(hsv, lower_red_one, upper_red_one)
    red_two = cv2.inRange(hsv, lower_red_two, upper_red_two)

    red_one = red_one + red_two

    # Creating the mask corresponding to the detected red color
    red_one = cv2.morphologyEx(red_one, cv2.MORPH_OPEN, np.ones((3, 3),
                                                                np.uint8))
    red_two = cv2.morphologyEx(
        red_one, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    red_two = cv2.bitwise_not(red_one)

    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask=red_one)
    # For testing the generated mask uncomment the next two lines
    # res1 = cv2.bitwise_and(img, img, mask=red_one)
    # cv2.imshow("Red Color Cloak!!!!", res1)
    res2 = cv2.bitwise_and(img, img, mask=red_two)

    output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Red Color Cloak", output)
    k = cv2.waitKey(10)
    if k == 27:
        break
