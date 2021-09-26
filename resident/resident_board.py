from tkinter import *
from tkinter import ttk
from operator import itemgetter
import controlBar
import talkingroom


class resident_board(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.count = 0
        ttk.Button(self, width=30, text='글 작성', style="TButton",
                   command=lambda: controller.controller.show_frame("resident_write_board")).place(x=1300, y=100)
        self.list = ['번호', '날짜', '아이디', '제목', '내용']
        size = [50, 200, 200, 200, 600]
        self.len_size = len(self.list) - 1
        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.len_size)], height=60)
        self.treeview.place(x=0, y=0)
        for i, name in enumerate(self.list):
            self.treeview.column('#' + str(i), width=size[i], anchor='center')
            self.treeview.heading('#' + str(i), text=name, )

        self.treeview.bind('<Double-Button-1>', self.OnDoubleClick)
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

        self.controller.controller.cur.execute('select * from 주민게시판')
        self.fetch = self.controller.controller.cur.fetchall()

        for i in range(len(self.fetch)):
            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i], iid=str(self.count) + "번")
            self.count += 1
        try:
            a = self.controller.controller.tk.after(1000, self.show)
        except:
            self.controller.controller.tk.after_cancel(a)

    def OnDoubleClick(self, event):
        for F in (talkingroom.talkingRoom,):
            page_name = F.__name__
            frame = F(parent=self.controller.controller.container, controller=self, log=self.log,
                      data=self.treeview.item(self.treeview.selection()[0], 'values'),class_=resident_board.__name__)
            self.controller.controller.frames[page_name] = frame

        self.controller.controller.show_frame("talkingRoom")
