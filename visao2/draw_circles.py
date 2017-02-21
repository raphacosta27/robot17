import cv2
import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
import time

#cap = cv2.VideoCapture('hall_box_battery.mp4')
cap = cv2.VideoCapture(0)
cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)


lower = 0
upper = 1
pos = 0
global posicoesx
global posicoesy
global dist
dist = 0

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    global lower
    lower = int(max(0, (1.0 - sigma) * v))
    global upper
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged



while(True):

    # Capture frame-by-frame
    #print("New frame")
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = frame

    posicoesx = []
    posicoesy = []



    #print("Will apply HoughCircles")
    circles = []

    bordas = auto_canny(gray)

    # Obtains a colored image back
    bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(bordas,cv.CV_HOUGH_GRADIENT,1.3,40,param1=50,param2=100,minRadius=20,maxRadius=60)

    if circles != None:
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:

            # draw the outer circle
            # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            cv2.circle(bordas_color,(i[0],i[1]),i[2],(255,0,0),2)
            posicoesx.append(i[0])
            posicoesy.append(i[1])
            dist = (685*6.5)/(i[2]*2)
            global pos

            # draw the center of the circle
            cv2.circle(bordas_color,(i[0],i[1]),2,(0,0,255),3)

    # Draw a diagonal blue line with thickness of 5 px
    # cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    # cv2.line(bordas_color,(0,0),(640,640),(0,255,0),5)

    # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])

    # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    if len(posicoesx) > 0 and len(posicoesy) > 0:
        deltax = max(posicoesx) - min(posicoesx)
        deltay = max(posicoesy) - min(posicoesy)
        if deltax > deltay:
            pos = "Horizontal"
        else:
            pos = "Vertical"
    text = "Distancia: {0}".format(dist)
    text2 = "Posicao: {0}".format(pos)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #hpix=131px; d=34cm; h=6,5; f=685
    cv2.putText(bordas_color, text,(0,100), font, 1,(0,0,255),2,cv2.CV_AA)
    cv2.putText(bordas_color, text2,(0,50), font, 1,(0,0,255),2,cv2.CV_AA)

    #More drawing functions @ http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html

    # Display the resulting frame
    cv2.imshow('frame', bordas_color)
    #print("No circles were found")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()