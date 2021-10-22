import socket
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

motion_class = ['basic', 'PoseO', 'PoseX', 'HandR', 'HandL']
student = [[], [], [], [], []]

name = 'HK'
while True:
    read, write, fail = select.select((s, sys.stdin), (), ())

    for desc in read:
        if desc == s:
            data = s.recv(4096)
            # 받아온 문자열을 출력함
            d = data.decode()

            if ':' in d:
                name, motion = d.split(':')
                print(motion)
                for i in motion_class:
                    if (motion == i):
                        if (name not in student[motion_class.index(i)]):
                            student[motion_class.index(i)].append(name)
                            # print(student)
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
