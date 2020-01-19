import cv2  # as cv
import time
import numpy as np

cap = cv2.VideoCapture(0)

time.sleep(1)

# define which color you want to mask out using the given plot of HSV. It's green here.
lower_range = np.array([100, 40, 40])  # ([40, 30, 80])
upper_range = np.array([100, 255, 255])  # ([45, 255, 255])


# upper_red = np.array([100, 255, 255])

time.sleep(1)
count = 0
background = 0



for x in range(60):
    ret, background = cap.read()
    if not ret:
        continue

while(cap.isOpened()):
    return_val, img = cap.read()
    if not return_val:
        break
    count = count + 1
    # img = np.flip(img, axis=1)

    # convert the image - BGR to HSV
    # as we focused on detection of red color

    # converting BGR to HSV for better
    # detection or you can convert it to gray
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #-------------------------------------BLOCK----------------------------#
    # ranges should be carefully chosen
    # setting the lower and upper range for mask1
    lower_red = np.array([100, 40, 40])
    upper_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # setting the lower and upper range for mask2
    lower_red = np.array([155, 40, 40])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    #----------------------------------------------------------------------#

    # the above block of code could be replaced with
    # some other code depending upon the color of your cloth
    mask1 = mask1 + mask2

    # Refining the mask corresponding to the detected red color
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                                            np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
    if k == 27:
        break
