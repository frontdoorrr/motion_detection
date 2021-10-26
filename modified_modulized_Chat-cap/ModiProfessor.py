from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from UserData import *
from ModiDetection import *

form_class_professor = loadUiType("modi002.ui")[0]


class ProfessorClass(QMainWindow, form_class_professor):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    # 교수용 화면에서 모션별 이미지 UI
    def init_ui(self):

        hand_up_list = ''
        absent_name =
        O_count =
        X_count =
        attendants = ''


        self.hand_up_img.setPixmap(QPixmap("handup.jpg"))
        self.absent_img.setPixmap(QPixmap("absent_img.jpg"))
        self.O_img.setPixmap(QPixmap("O_img.jpg"))
        self.X_img.setPixmap(QPixmap("X_img.jpg"))


        self.hand_up_name.setText(hand_up_list)
        self.absent_name.se
        self.O_count.se
        self.X_count.se
        self.get_count_attendants.setText()

        self.room_number_lbl.setText(room_number)
        self.username_lbl.setText(username)
