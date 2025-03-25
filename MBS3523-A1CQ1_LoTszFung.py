import cv2
import serial

cam = cv2.VideoCapture(0)
arduino = serial.Serial('COM5', 9600)

while True:
    ret, frame = cam.read()
    if not ret: break

    light = arduino.readline().decode().strip()

    cv2.putText(frame, f"light: {light}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 0), 2)

    cv2.imshow('hello', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
arduino.close()