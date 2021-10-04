import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

#UI파일 연결
form_class1 = uic.loadUiType("modi001.ui")[0]
form_class2 = uic.loadUiType("modi002.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class1) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        widget.setFixedHeight(275)
        widget.setFixedWidth(390)

        # 버튼에 기능을 연결하는 코드
        self.makeroom.clicked.connect(self.makeroomFunction)
        self.enterroom.clicked.connect(self.enterroomFunction)

    # 방만들기 버튼이 눌리면 작동할 함수
    def makeroomFunction(self):
        roomnumb1 = self.roomnumb.text()
        username = self.nametxt.text()
        print(roomnumb1,username)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedHeight(200)
        widget.setFixedWidth(600)

    # 방입장하기 버튼이 눌리면 작동할 함수
    def enterroomFunction(self) :
        roomnumb1 = self.roomnumb.text()
        username = self.nametxt.text()
        print(roomnumb1, username)

#화면을 띄우는데 사용되는 Class 선언 2 교수자용 화면
class ProfClass(QMainWindow, form_class2) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pixmap_1 = QPixmap
        self.name1.setText("")



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()


    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    profWindow = ProfClass()

    #Widget 추가
    widget.addWidget(myWindow)
    widget.addWidget(profWindow)

    #프로그램 화면을 보여주는 코드
    widget.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
