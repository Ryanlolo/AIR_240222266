import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    flip_h = cv2.flip(frame, 1)
    flip_v = cv2.flip(frame, 0)
    flip_both = cv2.flip(frame, -1)

    top_row = np.hstack((frame, flip_h))
    bottom_row = np.hstack((flip_v, flip_both))
    combined = np.vstack((top_row, bottom_row))

    cv2.imshow('Multiple_outputs', combined)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()