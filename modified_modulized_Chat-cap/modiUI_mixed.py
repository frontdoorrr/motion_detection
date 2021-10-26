from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mediapipe as mp
import cv2

import numpy as np
import pandas as pd
import pickle
import socket
import select
import sys



# 유저 데이터
class UserData:
    username = "Jeongmun"
    room_number = "ROOM"
    motion_msg = "NONE"


# UI파일 연결
form_class1 = uic.loadUiType("modi001.ui")[0]
form_class2 = uic.loadUiType("modi002.ui")[0]
form_class3 = uic.loadUiType("modi003.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class1):
    def __init__(self, professor_window, student_window):
        super().__init__()
        self.setupUi(self)
        widget.setFixedHeight(400)
        widget.setFixedWidth(400)

        self.professor_window = professor_window
        self.student_window = student_window

        # 버튼에 기능을 연결하는 코드
        self.makeroom.clicked.connect(self.make_room_function)
        self.enterroom.clicked.connect(self.enter_room_function)
        self.enterroom.clicked.connect(self.detection)

    # 방만들기 버튼이 눌리면 작동할 함수
    def make_room_function(self):
        UserData.room_number = self.get_room_number.text()
        UserData.username = self.get_username.text()

        # print("USER",USER_DATA.username,USER_DATA.room_number)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedHeight(200)
        widget.setFixedWidth(750)
        self.professor_window.room_number_lbl.setText(UserData.room_number)
        self.professor_window.username_lbl.setText(UserData.username)

    # 방입장하기 버튼이 눌리면 작동할 함수
    def enter_room_function(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
        UserData.room_number = self.get_room_number.text()
        UserData.username = self.get_username.text()

        widget.setFixedHeight(200)
        widget.setFixedWidth(400)
        self.student_window.room_number_lbl.setText(UserData.room_number)
        self.student_window.username_lbl.setText(UserData.username)

    # 모션 검출하는 딥러닝 모델
    def detection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 8000))

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
                    msg = body_language_class
                    UserData.motion_msg = body_language_class

                    s.send(f'{name}:{msg}'.encode())


                except:
                    pass

                # 자신의 모습 모니터링
                cv2.imshow('Raw Webcam Feed', image)
                cv2.destroyAllWindows()

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()


# 화면을 띄우는데 사용되는 Class 선언 1 학생용 화면
class StudentClass(QMainWindow, form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui2()

        self.room_number_lbl.setText(UserData.room_number)
        self.username_lbl.setText(UserData.username)

        self.timer_one = QTimer(self)
        self.timer_one.start(300)
        self.timer_one.timeout.connect(self.init_ui2)

    # 학생용 화면에서 모션별 이미지 UI
    def init_ui2(self):
        if UserData.motion_msg == 'HandL' or UserData.motion_msg == 'HandR':
            self.motion_client.setPixmap(QPixmap("handup.jpg"))
        elif UserData.motion_msg == 'PoseO':
            self.motion_client.setPixmap(QPixmap("O_img.jpg"))
        elif UserData.motion_msg == 'PoseX':
            self.motion_client.setPixmap(QPixmap("X_img.jpg"))
        else:
            self.motion_client.setPixmap(QPixmap("absent_img.jpg"))


# 화면을 띄우는데 사용되는 Class 선언 2 교수자용 화면
class ProfessorClass(QMainWindow, form_class2):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    # 교수용 화면에서 모션별 이미지 UI
    def init_ui(self):
        self.hand_up_img.setPixmap(QPixmap("handup.jpg"))
        self.absent_img.setPixmap(QPixmap("absent_img.jpg"))
        self.O_img.setPixmap(QPixmap("O_img.jpg"))
        self.X_img.setPixmap(QPixmap("X_img.jpg"))

        self.room_number_lbl.setText(UserData.room_number)
        self.username_lbl.setText(UserData.username)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QStackedWidget()

    # WindowClass의 인스턴스 생성
    professor_window = ProfessorClass()
    student_window = StudentClass()
    main_window = WindowClass(professor_window, student_window)

    # Widget 추가
    widget.addWidget(main_window)
    widget.addWidget(professor_window)
    widget.addWidget(student_window)

    # 프로그램 화면을 보여주는 코드
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
