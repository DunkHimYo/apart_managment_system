from tkinter import *
from tkinter import ttk
import controlBar
import StartPage


class security_login(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.delivery_count = 0
        self.delivery_list = ['번호', '아이디', '운송번호', '받는사람', '휴대폰번호', '도착지', '현재위치']
        delivery_size = [40, 70, 90, 90, 150, 250, 250]
        self.delivery_len_size = len(self.delivery_list) - 1

        self.delivery_treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.delivery_len_size)],
                                              displaycolumns=[str(i + 1) for i in range(self.delivery_len_size)],
                                              height=20)
        self.delivery_treeview.place(x=0, y=50)

        for i, name in enumerate(self.delivery_list):
            self.delivery_treeview.column('#' + str(i), width=delivery_size[i])
            self.delivery_treeview.heading('#' + str(i), text=name)

        self.request_count = 0
        self.request_list = ['번호', '작성번호', '아이디', '사유', '내용', '확인']
        request_size = [40, 150, 100, 200, 400, 50]
        self.request_len_size = len(self.request_list) - 1

        self.request_treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.request_len_size)],
                                             displaycolumns=[str(i + 1) for i in range(self.request_len_size)],
                                             height=20)
        self.request_treeview.place(x=0, y=550)

        for i, name in enumerate(self.request_list):
            self.request_treeview.column('#' + str(i), width=request_size[i], anchor='center')
            self.request_treeview.heading('#' + str(i), text=name)

        controlBar.controlBar(self)
        self.delivery_show()
        self.request_show()

    def delivery_show(self):
        if self.delivery_count != 0:
            for i in range(self.delivery_count):
                try:
                    self.delivery_treeview.delete(str(i) + "번")
                except:
                    pass
            self.delivery_count = 0

        self.controller.controller.cur.execute('select * from 배송정보 where 현재위치=\'경비실\'')
        self.fetch = self.controller.controller.cur.fetchall()
        self.fetch = sorted(self.fetch)
        for i in range(len(self.fetch)):
            self.delivery_treeview.insert('', END, text=self.delivery_count + 1, values=self.fetch[i],
                                          iid=str(self.delivery_count) + "번")
            self.delivery_count += 1

        try:
            a = self.controller.controller.tk.after(1000, self.delivery_show)
        except:
            self.controller.controller.tk.after_cancel(a)

    def request_show(self):
        if self.request_count != 0:
            for i in range(self.request_count):
                try:
                    self.request_treeview.delete(str(i) + "번")
                except:
                    pass
            self.request_count = 0

        self.controller.controller.cur.execute('select * from 요청목록')
        self.fetch = self.controller.controller.cur.fetchall()
        for i in range(len(self.fetch)):
            self.request_treeview.insert('', END, text=self.request_count + 1, values=self.fetch[i],
                                         iid=str(self.request_count) + "번")
            self.request_count += 1
        try:
            a = self.controller.controller.tk.after(1000, self.request_show)
        except:
            self.controller.controller.tk.after_cancel(a)
