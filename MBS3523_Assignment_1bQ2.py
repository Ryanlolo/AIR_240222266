import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameCanny = cv2.Canny(frame, 100, 100)
    frameBlurred = cv2.GaussianBlur(frame, (15, 15), 0)

    cv2.imshow('Web_camera', frame)
    cv2.imshow('Webcam_HSV', frameHSV)
    cv2.imshow('Webcam_Canny', frameCanny)
    cv2.imshow('Webcam_Blur', frameBlurred)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()