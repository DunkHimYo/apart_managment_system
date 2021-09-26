from tkinter import *
from tkinter import ttk
from operator import itemgetter
import controlBar
import show_manager_request

class manager_login(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.signUpcount = 0
        self.signUplist = ['번호', '아이디', '비밀번호', '이름', '휴대폰번호', '이용원', '주소(동/호)', '허용여부']
        size = [50, 100, 200, 80, 200, 80, 80, 80, 100]
        self.signUplen_size = len(self.signUplist) - 1
        self.signUptreeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.signUplen_size)],
                                           displaycolumns=[str(i + 1) for i in range(self.signUplen_size)], height=20)
        self.signUptreeview.place(x=0, y=50)
        for i, name in enumerate(self.signUplist):
            self.signUptreeview.column('#' + str(i), width=size[i], anchor='center')
            self.signUptreeview.heading('#' + str(i), text=name, )

        self.board_count = 0
        self.board_list = ['번호', '작성번호', '제목', '내용', '확인']
        size = [50, 200, 200, 600, 50]
        self.board_len_size = len(self.board_list) - 1
        self.board_treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.board_len_size)],
                                           displaycolumns=[str(i + 1) for i in range(self.board_len_size)], height=20)
        self.board_treeview.place(x=0, y=550)
        for i, name in enumerate(self.board_list):
            self.board_treeview.column('#' + str(i), width=size[i], anchor='center')
            self.board_treeview.heading('#' + str(i), text=name, )
        self.board_treeview.bind('<Double-Button-1>', self.OnDoubleClick)

        controlBar.controlBar(self)
        self.signUpshow()
        self.board_show()

    def signUpshow(self):
        if self.signUpcount != 0:
            for i in range(self.signUpcount):
                try:
                    self.signUptreeview.delete(str(i) + "번")
                except:
                    pass
            self.signUpcount = 0

        self.controller.controller.cur.execute('select * from 회원목록')
        self.fetch = self.controller.controller.cur.fetchall()
        self.fetch = sorted(self.fetch, key=itemgetter(6), reverse=True)

        for i in range(len(self.fetch)):
            self.signUptreeview.insert('', END, text=self.signUpcount + 1, values=self.fetch[i],
                                       iid=str(self.signUpcount) + "번")
            self.signUpcount += 1
        try:
            a = self.controller.controller.tk.after(1000, self.signUpshow)
        except:
            self.controller.controller.tk.after_cancel(a)

    def board_show(self):
        if self.board_count != 0:
            for i in range(self.board_count):
                try:
                    self.board_treeview.delete(str(i) + "번")
                except:
                    pass
            self.board_count = 0

        self.controller.controller.cur.execute('select * from 문의목록')
        self.fetch = self.controller.controller.cur.fetchall()

        for i in range(len(self.fetch)):
            self.board_treeview.insert('', END, text=self.board_count + 1, values=self.fetch[i],
                                       iid=str(self.board_count) + "번")
            self.board_count += 1
        try:
            a = self.controller.controller.tk.after(1000, self.board_show)
        except:
            self.controller.controller.tk.after_cancel(a)

    def OnDoubleClick(self, event):
        for F in (show_manager_request.show_request,):
            page_name = F.__name__
            frame = F(parent=self.controller.controller.container, controller=self, log=self.log,
                      data=self.board_treeview.item(self.board_treeview.selection()[0], 'values'))
            self.controller.controller.frames[page_name] = frame

        self.controller.controller.show_frame("show_request")
