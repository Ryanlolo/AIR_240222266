import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_head_angle(ear, shoulder, nose):
    ear = np.array(ear)
    shoulder = np.array(shoulder)
    nose = np.array(nose)

    vec_shoulder_ear = ear - shoulder

    vec_shoulder_nose = nose - shoulder

    angle = np.degrees(np.arctan2(vec_shoulder_nose[1], vec_shoulder_nose[0]) -
                       np.arctan2(vec_shoulder_ear[1], vec_shoulder_ear[0]))

    angle = (angle + 180) % 360 - 180

    return angle

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FPS, 40)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

head_position = None

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
    while cam.isOpened():
        ret, img = cam.read()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        results = pose.process(imgRGB)
        imgRGB.flags.writeable = True
        img = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            left_ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            vertical_angle = calculate_head_angle(left_ear, left_shoulder, nose)

            if vertical_angle <= -20:
                head_position = "Looking Down"
            elif -10 < vertical_angle < 10:
                head_position = "Looking Up"
            else:
                head_position = "middle"

            cv2.putText(img, f"{vertical_angle:.1f}o",
                        tuple(np.multiply(left_ear, [1280, 720]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 225), 2, cv2.LINE_AA)

        except:
            pass

        cv2.rectangle(img, (0, 0), (350, 100), (240, 100, 80), -1)

        cv2.putText(img, 'HEAD POSITION', (15, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, head_position if head_position else "Not Detected",
                    (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (255, 255, 115), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Detection', img)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cam.release()
cv2.destroyAllWindows()