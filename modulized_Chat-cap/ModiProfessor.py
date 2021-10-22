from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from UserData import *
import ModiDetection

form_class_professor = loadUiType("modi002.ui")[0]


class ProfessorClass(QMainWindow, form_class_professor):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    # 교수용 화면에서 모션별 이미지 UI
    def init_ui(self):
        student_list = ModiDetection.student
        basic_list = ''.join(student_list[0])
        hands_up_list = ''.join(student_list[1] + student_list[2])
        pose_o_cnt = str(len(student_list[3]))
        pose_x_cnt = str(len(student_list[4]))


        self.hand_up_img.setPixmap(QPixmap("handup.jpg"))
        self.absent_img.setPixmap(QPixmap("absent_img.jpg"))
        self.O_img.setPixmap(QPixmap("O_img.jpg"))
        self.X_img.setPixmap(QPixmap("X_img.jpg"))

        self.room_number_lbl.setText(room_number)
        self.username_lbl.setText(username)
        self.hand_up_name.setText(hands_up_list)
        # self.absent_name.setText()
        self.O_count.setText(pose_o_cnt)
        self.X_count.setText(pose_x_cnt)
