from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
import UserData

form_class_professor = loadUiType("modi002.ui")[0]


class ProfessorClass(QMainWindow, form_class_professor):

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
