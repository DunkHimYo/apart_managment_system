from tkinter import *
from tkinter import ttk


def controlBar(self):
    default_x = 1300
    default_y = 150
    ttk.Frame(self, style='TFrame', width=500, height=600).place(x=default_x, y=150)

    ttk.Label(self, text=str(self.log[0]) + '님 안녕하세요', width=30, style='TButton',
              ).place(x=default_x + 130, y=default_y + 50)

    title_list = {'관리자':
                      {'신청자 관리': lambda: self.controller.controller.show_frame("signUpList"),
                       '요청하기': lambda: self.controller.controller.show_frame('send_request'),
                       '게시판\n확인': lambda: self.controller.controller.show_frame('employee_board'),
                       '공지\n확인': lambda: self.controller.controller.show_frame('notice'),
                       '홈': lambda: self.controller.controller.show_frame('manager_login')},
                  '경비원':
                      {'헬스장\n인원 확인': lambda: self.controller.controller.show_frame("counter"),
                       '요청보기': lambda: self.controller.controller.show_frame('request'),
                       '게시판\n확인': lambda: self.controller.controller.show_frame('employee_board'),
                       '공지\n확인': lambda: self.controller.controller.show_frame('notice'),
                       '홈': lambda: self.controller.controller.show_frame('security_login')},
                  '택배기사':
                      {'배송\n정보 관리': lambda: self.controller.controller.show_frame("table"),
                       '요청하기': lambda: self.controller.controller.show_frame('send_request'),
                       '게시판\n확인': lambda: self.controller.controller.show_frame('employee_board'),
                       '공지\n확인': lambda: self.controller.controller.show_frame('notice'),
                       '홈': lambda: self.controller.controller.show_frame('delivery_login')},
                  '주민':
                      {'헬스장\n인원 확인': lambda: self.controller.controller.show_frame("counter"),
                       '요청하기': lambda: self.controller.controller.show_frame('send_request'),
                       '게시판\n확인': lambda: self.controller.controller.show_frame('resident_board'),
                       '공지\n확인': lambda: self.controller.controller.show_frame('notice'),
                       '홈': lambda: self.controller.controller.show_frame('residents_login')}
                  }

    x_list = [default_x + 100, default_x + 100, default_x + 100, default_x + 320, default_x + 320]
    y_list = [default_y + 150, default_y + 280, default_y + 410, default_y + 150, default_y + 280]

    for num, i in enumerate(title_list[self.log[2]].keys()):
        Button(self, width=10, height=3, text=i, relief='flat', background="burlywood",
               anchor='center', justify='center', foreground="maroon", command=title_list[self.log[2]][i]).place(
            x=x_list[num],
            y=y_list[num])

        Button(self, width=40, height=1, text='로그아웃', relief='flat', background="burlywood", anchor='center',
               justify='center', foreground="maroon",
               command=lambda: self.controller.controller.show_frame("StartPage")
               ).place(x=default_x + 100, y=690)
