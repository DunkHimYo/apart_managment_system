from tkinter import ttk
from tkinter import *
import controlBar2
import manager_login


class talkingRoom(ttk.Frame):

    def __init__(self, parent, controller, log, data, class_):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.data = data
        self.log = log
        self.count = 0
        default_x = 100
        default_y = 150

        main_title = ttk.Frame(self, style='TFrame', width=1100, height=900)
        main_title.place(x=default_x, y=default_y)

        main_label = ttk.Label(self, text=data[1] + '님의 글', width=21, style='TButton', foreground="maroon",
                               font="굴림 30")
        main_label.place(x=default_x, y=default_y)
        # id_start

        #   id_label_start
        x_st = 40
        x_nd = 140
        y_st = 130

        # label
        self.label_list = {'제목': None, '내용': None, '댓글\n작성': None}
        self.size = len(self.label_list)
        for k in self.label_list.keys():

            if k == '제목':
                label = ttk.Label(self, text=k, style='TButton', width=9, foreground="maroon")
                label.place(x=default_x + x_st, y=default_y + y_st)

                self.label_list[k] = Entry(self, font="굴림 20", width=50, disabledbackground='white')
                self.label_list[k].place(x=default_x + x_nd, y=default_y + y_st)
                self.label_list[k].insert(0, data[2])
                self.label_list[k].configure(state='disabled')
            elif k == '댓글\n작성' and class_ != 'notice':
                label = ttk.Label(self, text=k, style='TButton', width=9, foreground="maroon")
                label.place(x=default_x + x_st, y=default_y + y_st)
                self.label_list[k] = Text(self, font="굴림 20", width=50, height=3)
                self.label_list[k].place(x=default_x + x_nd, y=default_y + y_st)

            elif k == '내용':
                label = ttk.Label(self, text=k, style='TButton', width=9, foreground="maroon")
                label.place(x=default_x + x_st, y=default_y + y_st)
                self.label_list[k] = Text(self, font="굴림 20", width=50, height=6)
                self.label_list[k].place(x=default_x + x_nd, y=default_y + y_st)
                self.label_list[k].insert(INSERT, data[3])
                self.label_list[k].configure(state='disabled')
                y_st += 140
            y_st += 60

        a = y_st + x_nd
        if class_ == 'notice':
            a = y_st

        label = ttk.Button(self, text='전송', width=15, style='TButton',
                           command=self.insert)
        label.place(x=x_nd * 7 + 75, y=a)

        self.list = {'번호': None, '아이디': None, '댓글': None}
        size = [50, 100, 900]
        self.len_size = len(self.list) - 1
        print(class_)
        if class_ != 'notice':
            self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                         displaycolumns=[str(i + 1) for i in range(self.len_size)], height=16)
            self.treeview.place(x=x_nd, y=y_st + 200)
            for i, name in enumerate(self.list.keys()):
                self.treeview.column('#' + str(i), width=size[i], anchor='center')
                self.treeview.heading('#' + str(i), text=name, )
            self.show()

        controlBar2.controlBar2(self)

    def show(self):
        if self.count != 0:
            for i in range(self.count):
                try:
                    self.treeview.delete(str(i) + "번")
                except:
                    pass
            self.count = 0
        if self.log[2] == '관리자' or self.log[2] == '경비원':
            self.controller.controller.controller.cur.execute('select * from 직원게시댓글')
        elif self.log[2] == '주민':
            self.controller.controller.controller.cur.execute('select * from 주민게시댓글')

        self.fetch = self.controller.controller.controller.cur.fetchall()

        for i in range(len(self.fetch)):
            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i][1:-1], iid=str(self.count) + "번")
            self.count += 1

    def insert(self):
        self.delivery = (self.data[0], self.log[0],
                         self.label_list['댓글\n작성'].get('1.0', END).replace('\n', ' '),
                         '-'.join(self.controller.controller.controller.update_clock()))
        if self.log[2] == '관리자' or self.log[2] == '경비원':
            self.controller.controller.controller.cur.execute('insert into 직원게시댓글 values %s' % str(self.delivery))
        elif self.log[2] == '주민':
            self.controller.controller.controller.cur.execute(
                'insert into 주민게시댓글 values %s' % str(self.delivery))
        self.controller.controller.controller.cur.execute('commit')

        self.label_list['댓글\n작성'].delete('1.0', END)

        self.count += 1
        self.show()
