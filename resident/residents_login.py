from tkinter import *
from tkinter import ttk
import controlBar

class residents_login(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log

        self.count = 0

        self.list = ['번호', '아이디', '운송번호', '받는사람', '휴대폰번호', '도착지', '현재위치']
        size = [40, 70, 90, 70, 150, 250, 250]
        self.len_size = len(self.list) - 1

        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.len_size)], height=20)
        self.treeview.place(x=0, y=0)

        for i, name in enumerate(self.list):
            self.treeview.column('#' + str(i), width=size[i])
            self.treeview.heading('#' + str(i), text=name)

        controlBar.controlBar(self)
        self.show()



    def show(self):
        if self.count != 0:
            for i in range(self.count):
                try:
                    self.treeview.delete(str(i) + "번")
                except:
                    pass
            self.count = 0

        self.controller.controller.cur.execute('select * from 배송정보 where 아이디=\'%s\'' % self.log[0])
        self.fetch = self.controller.controller.cur.fetchall()
        self.fetch = sorted(self.fetch)
        for i in range(len(self.fetch)):
            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i],
                                 iid=str(self.count) + "번")
            self.count += 1
        try:
            a=self.controller.controller.tk.after(1000, self.show)
        except:
            self.controller.controller.tk.after_cancel(a)
