from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
import sys
import socket
import select
import UserData
import ModiDetection

form_class_professor = loadUiType("modi002.ui")[0]


class ProfessorClass(QMainWindow, form_class_professor):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

        self.room_number_lbl.setText(UserData.room_number)
        self.username_lbl.setText(UserData.username)


    # 교수용 화면에서 모션별 이미지 UI
    def init_ui(self):

        # student_list = [[],[],[],[],[]]
        #
        #
        # hand_up_list = str(student_list[3] + student_list[4])
        # absent_list = 'absent'
        # O_count_list = str(len(student_list[1]))
        # X_count_list = str(len(student_list[2]))
        # # attendants_list = str(sum(len(student_list[:])))
        # attendants_list = 'none'


        self.hand_up_img.setPixmap(QPixmap("handup.jpg"))
        self.absent_img.setPixmap(QPixmap("absent_img.jpg"))
        self.O_img.setPixmap(QPixmap("O_img.jpg"))
        self.X_img.setPixmap(QPixmap("X_img.jpg"))


        # self.hand_up_name.setText(hand_up_list)
        # self.absent_name.setText(absent_list)
        # self.O_count.setText(O_count_list)
        # self.X_count.setText(X_count_list)
        # self.get_count_attendants.setText(attendants_list)
        #
        # self.room_number_lbl.setText(room_number)
        # self.username_lbl.setText(username)
