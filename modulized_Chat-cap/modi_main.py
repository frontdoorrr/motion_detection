from ModiProfessor import *
from ModiStudent import *
from ModiDetection import *
import UserData
from PyQt5.QtCore import *
import threading

form_class_main = loadUiType("modi001.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class_main):

    def __init__(self, professor_window, student_window,data_list):
        super().__init__()
        self.setupUi(self)
        widget.setFixedHeight(400)
        widget.setFixedWidth(400)

        self.professor_window = professor_window
        self.student_window = student_window

        #데이터 리스트 초기화
        self.data_list = data_list
        #print("WindowClass __init__ self.data_list",id(self.data_list))

        # 버튼에 기능을 연결하는 코드
        self.makeroom.clicked.connect(self.make_room_function)
        self.enterroom.clicked.connect(self.enter_room_function)
        self.enterroom.clicked.connect(send_detection)

        #스레드

        self.thread_1 = threading.Thread(target=self.receive_list_mem)
        self.thread_1.daemon = True #프로세스 끝날때 스레드종료시켜줌



    def receive_list_mem(self) :

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((UserData.ip_address, UserData.port_num))

        motion_class = ['basic', 'PoseO', 'PoseX', 'HandR', 'HandL']
        # student = [[], [], [], [], []]

        name = "f"
        while True:
            read, write, fail = select.select((s, sys.stdin), (), ())

            for desc in read:
                if desc == s:
                    data = s.recv(4096)
                    # 받아온 문자열을 출력함
                    d = data.decode()
                    # self.data_list = [[], [], [], [], []]
                    # for i in range(5):
                    #     self.data_list[i].clear()

                    # 스레드 데이터 확인
                    #print("DEBUG thread data_list",id(self.data_list))

                    if ':' in d:
                        print(d)
                        try :
                            name, motion = d.split(':')
                        except :
                            print("except")
                            pass

                        for i in motion_class:
                            if (motion == i):
                                for x in range(5) :
                                    if (name in self.data_list[x]):
                                        self.data_list[x].remove(name)
                                if (name not in self.data_list[motion_class.index(i)]):
                                    self.data_list[motion_class.index(i)].append(name)
                                    print(self.data_list)
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



    # 방만들기 버튼이 눌리면 작동할 함수
    def make_room_function(self):
        UserData.room_number = self.get_room_number.text()
        UserData.username = self.get_username.text()

        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedHeight(200)
        widget.setFixedWidth(750)
        professor_window.room_number_lbl.setText(UserData.room_number)
        professor_window.username_lbl.setText(UserData.username)

        #스레드 시작
        self.thread_1.start()


    # 방입장하기 버튼이 눌리면 작동할 함수
    def enter_room_function(self):
        UserData.room_number = self.get_room_number.text()
        UserData.username = self.get_username.text()

        widget.setCurrentIndex(widget.currentIndex() + 2)
        widget.setFixedHeight(200)
        widget.setFixedWidth(400)
        student_window.room_number_lbl.setText(UserData.room_number)
        student_window.username_lbl.setText(UserData.username)

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QStackedWidget()

    # Window Class의 인스턴스 생성
    data_list = [[],[],[],[],[]]
    professor_window = ProfessorClass(data_list)
    student_window = StudentClass()

    main_window = WindowClass(professor_window, student_window,data_list)

    # Widget 추가
    widget.addWidget(main_window)
    widget.addWidget(professor_window)
    widget.addWidget(student_window)

    # 프로그램 화면을 보여주는 코드
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
