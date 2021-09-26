from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import table
import signUpList
import counter
from security import security_login
import delivery_login
import manager_login
import send_request
import request
from resident import resident_write_board, residents_login, resident_board
import notice
import write_notice
import employee_board
import employee_write_board


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        Label(self, image=controller.img, width=1200).pack(side="left", fill="both", expand=False)

        default_x = 1300;
        default_y = 150
        ttk.Frame(self, style='TFrame', width=500, height=600).place(x=default_x, y=default_y)

        ttk.Label(self, text='AMS', width=10, style='TButton', font=controller.title_font).place(x=default_x + 130,
                                                                                                 y=default_y + 50)
        self.values = ['주민', '경비원', '택배기사', '관리자']

        id_ps_list = ['아이디', '비밀번호']
        self.data_entries = {}
        self.len_size = len(id_ps_list)
        y = 275
        for i in range(len(id_ps_list)):
            label = ttk.Label(self, text=id_ps_list[i], style='TButton', width=9, )
            label.place(x=default_x + 30, y=y)
            self.data_entries[i] = Entry(self, font="굴림 20", width=15)
            self.data_entries[i].place(x=default_x + 135, y=y)
            y += 50

        ttk.Button(self, width=30, text='AMS 회원가입', style="TButton",
                   command=lambda: controller.show_frame("signUp")).place(x=default_x + 135, y=400)

        id_ps_list = ['아이디/비밀번호 찾기', '관리사무실 문의']
        y = 550
        for i in range(len(id_ps_list)):
            if i == 0:
                id_ps = ttk.Button(self, width=20, text=id_ps_list[i], style="TButton",
                                   command=lambda: self.controller.show_frame("findIdPs"))
                id_ps.place(x=default_x + 200, y=y)
            else:
                id_ps = ttk.Button(self, width=20, text=id_ps_list[i], style="TButton",
                                   command=lambda: self.controller.show_frame("manager_request"))
                id_ps.place(x=default_x + 200, y=y)
            y += 50

        Label(self, text="제작자 : 김도현 and 김태완", width=25, height=3, bg="blanchedalmond", relief="flat", font=1,
              fg='maroon').place(x=default_x + 20, y=default_y + 530)
        Button(self, text="로그인", overrelief="solid", width=8, height=3, bg="burlywood", fg='maroon',
               command=self.quest).place(x=default_x + 400, y=default_y + 130)

    def quest(self):
        data = {}
        for i in range(self.len_size):
            data[i] = self.data_entries[i].get()

        for i in range(self.len_size):
            self.data_entries[i].delete(0, 'end')
        """try:"""
        self.controller.cur.execute('select 아이디, 소속 from 총원명부 where 아이디 = \'%s\'' % data[0])

        answer = list(self.controller.cur.fetchall()[0])

        if answer[1] in self.values:
            self.controller.cur.execute('select 비밀번호 from %s where 아이디 = \'%s\'' % (answer[1], data[0]))
            ps = self.controller.cur.fetchall()[0][0]

        answer.insert(1, ps)
        if data[0] == answer[0] and data[1] == answer[1] and answer[2] == '주민':

            for F in (residents_login.residents_login, counter.counter, table.table, signUpList.signUpList,
                      send_request.send_request, resident_board.resident_board, resident_write_board.resident_write_board, notice.notice,
                      write_notice.write_notice):
                page_name = F.__name__
                frame = F(parent=self.controller.container, controller=self, log=answer)
                self.controller.frames[page_name] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.controller.show_frame("residents_login")
        elif data[0] == answer[0] and data[1] == answer[1] and answer[2] == '경비원':

            for F in (
                    security_login.security_login, counter.counter, table.table, signUpList.signUpList,
                    request.request, employee_board.employee_board, employee_write_board.employee_write_board,
                    notice.notice, write_notice.write_notice):
                page_name = F.__name__
                frame = F(parent=self.controller.container, controller=self, log=answer)
                self.controller.frames[page_name] = frame

            self.controller.show_frame("security_login")

        elif data[0] == answer[0] and data[1] == answer[1] and answer[2] == '택배기사':

            for F in (
                    delivery_login.delivery_login, table.table, send_request.send_request, employee_board.employee_board,
                    employee_write_board.employee_write_board,
                    notice.notice, write_notice.write_notice):
                page_name = F.__name__
                frame = F(parent=self.controller.container, controller=self, log=answer)
                self.controller.frames[page_name] = frame

            self.controller.show_frame("delivery_login")
        elif data[0] == answer[0] and data[1] == answer[1] and answer[2] == '관리자':

            for F in (
                    manager_login.manager_login, signUpList.signUpList, send_request.send_request,
                    employee_board.employee_board,
                    employee_write_board.employee_write_board, write_notice.write_notice, notice.notice):
                page_name = F.__name__
                frame = F(parent=self.controller.container, controller=self, log=answer)
                self.controller.frames[page_name] = frame

            self.controller.show_frame("manager_login")

        else:
            messagebox.showinfo("에러", "일치하지 않습니다.")