from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from UserData import *
import ModiDetection
from PyQt5.QtCore import *


form_class_professor = loadUiType("modi002.ui")[0]


class ProfessorClass(QMainWindow, form_class_professor):

    def __init__(self,data_list):
        super().__init__()
        self.setupUi(self)
        self.data_list = data_list
        self.init_ui()


        self.room_number_lbl.setText(room_number)
        self.username_lbl.setText(username)

        #UI 업데이트
        self.timer_one = QTimer(self)
        self.timer_one.start(300)
        self.timer_one.timeout.connect(self.init_ui)

    # 교수용 화면에서 모션별 이미지 UI
    def init_ui(self):
        # 데이터리스트 확인
        #print("DEBUG professor data_list",self.data_list,id(self.data_list))

        # student_list = self.data_list
        basic_list = ''.join(self.data_list[0])
        hands_up_list = ', '.join(self.data_list[3] + self.data_list[4])
        pose_o_cnt = str(len(self.data_list[1]))
        pose_x_cnt = str(len(self.data_list[2]))


        self.hand_up_img.setPixmap(QPixmap("handup.jpg"))
        self.absent_img.setPixmap(QPixmap("absent_img.jpg"))
        self.O_img.setPixmap(QPixmap("O_img.jpg"))
        self.X_img.setPixmap(QPixmap("X_img.jpg"))

        #print("hands_up_list",hands_up_list,type(hands_up_list))
        self.hand_up_name.setText(hands_up_list)
        # self.absent_name.setText()
        self.O_count.setText(pose_o_cnt)
        self.X_count.setText(pose_x_cnt)

        #UI 업데이트 되는지 확인
        # import numpy as np
        # random_value = np.random.choice([1,2,3,4,5],[1,],False)
        # self.hand_up_name.setText("%d %s"%(random_value[0],hands_up_list))

import sys
if __name__ == "__main__":

    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QStackedWidget()

    # Window Class의 인스턴스 생성
    professor_window = ProfessorClass()

    widget.addWidget(professor_window)

    # 프로그램 화면을 보여주는 코드
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    ProfessorClass()