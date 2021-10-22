from ModiProfessor import *
from ModiStudent import *
from ModiDetection import *

form_class_main = loadUiType("modi001.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class_main):

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
        self.enterroom.clicked.connect(send_detection)

    # 방만들기 버튼이 눌리면 작동할 함수
    def make_room_function(self):
        room_number = self.get_room_number.text()
        username = self.get_username.text()

        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedHeight(200)
        widget.setFixedWidth(750)
        self.professor_window.room_number_lbl.setText(room_number)
        self.professor_window.username_lbl.setText(username)

    # 방입장하기 버튼이 눌리면 작동할 함수
    def enter_room_function(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
        room_number = self.get_room_number.text()
        username = self.get_username.text()

        widget.setFixedHeight(200)
        widget.setFixedWidth(400)
        self.student_window.room_number_lbl.setText(room_number)
        self.student_window.username_lbl.setText(username)


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
