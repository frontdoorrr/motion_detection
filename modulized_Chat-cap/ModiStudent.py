from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
import UserData

form_class_student = loadUiType("modi003.ui")[0]


class StudentClass(QMainWindow, form_class_student):
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
            self.motion_client.setPixmap(QPixmap("present.jpg"))