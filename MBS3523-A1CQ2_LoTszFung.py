import serial
import cv2
import time
import numpy as np

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
frame = np.zeros((480, 640, 3), np.uint8)

ser = serial.Serial('COM16', baudrate = 9600, timeout = 1)
time.sleep(2)

pan_angle = 90
tilt_angle = 90

def nothing(x):
    pass

def send_angles(pan, tilt):
    ser.write(f"{pan},{tilt}\n".encode())

cv2.namedWindow("Trackbar")
cv2.createTrackbar('HUELOW', 'Trackbar', 0, 179, nothing)
cv2.createTrackbar('HUEHIGH', 'Trackbar', 150, 255, nothing)
cv2.createTrackbar('SATLOW', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('SATHIGH', 'Trackbar', 255, 255, nothing)
cv2.createTrackbar('VALLOW', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('VALHIGH', 'Trackbar', 255, 255, nothing)

smoothing_factor = 0.1

smoothed_pan_angle = pan_angle
smoothed_tilt_angle = tilt_angle

while True:
    ret, img = cam.read()
    if not ret:
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    HUELOW = cv2.getTrackbarPos('HUELOW', 'Trackbar')
    HUEHIGH = cv2.getTrackbarPos('HUEHIGH', 'Trackbar')
    SATLOW = cv2.getTrackbarPos('SATLOW', 'Trackbar')
    SATHIGH = cv2.getTrackbarPos('SATHIGH', 'Trackbar')
    VALLOW = cv2.getTrackbarPos('VALLOW', 'Trackbar')
    VALHIGH = cv2.getTrackbarPos('VALHIGH', 'Trackbar')

    FGmask = cv2.inRange(hsv, (HUELOW, SATLOW, VALLOW), (HUEHIGH, SATHIGH, VALHIGH))

    contours, hierarchy = cv2.findContours(FGmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    if contours:
        largest_contour = contours[0]
        area = cv2.contourArea(largest_contour)

        if area > 100:

            (x, y, w, h) = cv2.boundingRect(largest_contour)

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

            center_x = x + w // 2
            center_y = y + h // 2

            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), 3)

            frame_center_x = img.shape[1] // 2
            frame_center_y = img.shape[0] // 2

            delta_x = center_x - frame_center_x
            delta_y = center_y - frame_center_y

            pan_angle -= delta_x * 0.01
            tilt_angle -= delta_y * 0.01

            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            smoothed_pan_angle = smoothed_pan_angle * (1 - smoothing_factor) + pan_angle * smoothing_factor
            smoothed_tilt_angle = smoothed_tilt_angle * (1 - smoothing_factor) + tilt_angle * smoothing_factor

            send_angles(int(smoothed_pan_angle), int(smoothed_tilt_angle))

    final = cv2.bitwise_and(img, img, mask=FGmask)
    cv2.imshow('final', final)
    cv2.imshow('Original', img)

    if cv2.waitKey(1) & 0xff == 27:
        break

cam.release()
cv2.destroyAllWindows()
ser.close()