import mediapipe as mp
import cv2
import sys
import numpy as np
import pandas as pd
import pickle
import socket
import select
import UserData



def send_detection(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('15.164.244.179', 8889))

    name = UserData.username

    mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
    mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

    # pkl File Load
    with open('body_language.pkl', 'rb') as f:
        model = pickle.load(f)

    cap = cv2.VideoCapture(0)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()

            # BGR2RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detections
            results = holistic.process(image)

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )
            # Export coordinates
            try:
                # Extract Pose landmarks
                pose = results.pose_landmarks.landmark
                pose_row = list(
                    np.array(
                        [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

                # Concate rows
                row = pose_row

                # Make Detections
                X = pd.DataFrame([row])
                body_language_class = model.predict(X)[0]
                body_language_prob = model.predict_proba(X)[0]

                # Print Class name and Probability
                print(body_language_class, body_language_prob)

                # Grab ear coords
                coords = tuple(np.multiply(
                    np.array(
                        (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
                         results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                    , [640, 480]).astype(int))

                cv2.rectangle(image,
                              (coords[0], coords[1] + 5),
                              (coords[0] + len(body_language_class) * 20, coords[1] - 30),
                              (245, 117, 16), -1)
                cv2.putText(image, body_language_class, coords,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Get status box
                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

                # Display Class
                cv2.putText(image, 'CLASS'
                            , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, body_language_class.split(' ')[0]
                            , (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Display Probability
                cv2.putText(image, 'PROB'
                            , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2))
                            , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                read, write, fail = select.select((s, sys.stdin), (), ())
                UserData.motion_msg = body_language_class

                s.send(f'{UserData.username}:{UserData.motion_msg}'.encode())


            except:
                pass

            # 자신의 모습 모니터링
            cv2.imshow('Raw Webcam Feed', image)
            cv2.destroyAllWindows()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()

def receive_name():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('15.164.244.179', 8889))

    motion_class = ['basic', 'PoseO', 'PoseX', 'HandR', 'HandL']
    student = [[], [], [], [], []]

    name = 'HK'
    while True:
        read, write, fail = select.select((s, sys.stdin), (), ())

        for desc in read:
            if desc == s:
                data = s.recv(4096)
                # 받아온 문자열을 출력함
                d = data.decode()

                if ':' in d:
                    name, motion = d.split(':')

                    for i in motion_class:
                        if (motion == i):
                            if (name not in student[motion_class.index(i)]):
                                student[motion_class.index(i)].append(name)
                                print(student)
                            else:
                                pass
                else:
                    pass

                if name is None:
                    name = data.decode()
                    s.send(f'{name} is connected!'.encode())
            else:
                msg = desc.readline()
                # 메시지를 서버로 보냄
                msg = msg.replace('\n', '')
                s.send(f'{name}:{msg}'.encode())
