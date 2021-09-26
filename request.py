from tkinter import *
from tkinter import ttk, Scrollbar
from operator import itemgetter


class request(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.list = {'번호': None, '작성번호': None, '아이디': None, '사유': None, '내용': None, '확인': None}
        size = [40, 100, 100, 300, 500, 40]
        self.len_size = len(self.list) - 1

        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.len_size)], height=20)
        vsb = Scrollbar(self, orient="vertical", command=self.treeview.yview)
        vsb.place(relx=0.792, rely=0, relheight=0.409, relwidth=0.010)
        self.treeview.configure(yscrollcommand=vsb.set)
        self.treeview.pack()

        for i, name in enumerate(self.list):
            self.treeview.column('#' + str(i), width=size[i])
            self.treeview.heading('#' + str(i), text=name)

        self.delivery = {}

        self.count = 0
        default_x = 460;
        default_y = 520
        main_title = ttk.Frame(self, style='TFrame', width=950, height=400)
        main_title.place(x=default_x, y=default_y)

        Label(self, text='입력창', width=50, height="3", background="burlywood", foreground="maroon").pack(pady=60)
        self.title = tuple(self.list.keys())[2:]
        for i in self.title:
            Label(self, text=i, width=50, background="burlywood", foreground="maroon").pack()
            self.list[i] = Entry(self, width=50)
            self.list[i].pack()

        def_y = 120

        title_list = {'조회': self.show, '전송': self.insert, '수정': self.retouch, '삭제': self.delete,
                      '취소': lambda: controller.controller.show_frame("security_login")}
        for n, i in title_list.items():
            ttk.Button(self, width=13, text=n, style="TButton",
                       command=i).place(x=default_x + 850,
                                        y=default_y - 60 + def_y)
            def_y += 60
        self.show()

    def insert(self):
        input = []
        for i in self.title:
            input.append(self.list[i].get())
        self.delivery[self.count] = input

        for i in self.title:
            self.list[i].delete(0, 'end')
        self.controller.controller.cur.execute(
            'select 아이디 from 회원목록 where 휴대폰번호 = \'%s\'' % self.delivery[self.count][2])
        self.delivery[self.count].insert(0, self.controller.controller.cur.fetchall()[0][0])

        self.treeview.insert('', 'end', text=self.count + 1, values=self.delivery[self.count],
                             iid=str(self.count) + "번")

        self.controller.controller.cur.execute('insert into 배송정보 values %s' % str(tuple(self.delivery[self.count])))
        self.controller.controller.cur.execute('commit')

        self.count += 1

    def show(self):
        if self.count != 0:
            for i in range(self.count):
                try:
                    self.treeview.delete(str(i) + "번")
                except:
                    pass
            self.count = 0

        self.controller.controller.cur.execute('select * from 요청목록')
        self.fetch = self.controller.controller.cur.fetchall()
        self.fetch = sorted(self.fetch, key=itemgetter(1), reverse=True)
        for i in range(len(self.fetch)):
            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i],
                                 iid=str(self.count) + "번")
            self.count += 1

    def delete(self):
        selected_item = self.treeview.selection()
        leng = len(selected_item)
        for i in range(leng):
            self.controller.controller.cur.execute(
                'delete from 요청목록 where 작성번호=\'%s\'' % self.treeview.set(selected_item[i])['1'])
            self.controller.controller.cur.execute('commit')
            self.treeview.delete(selected_item[i])

    def retouch(self):
        input = []
        for i in self.title:
            input.append(self.list[i].get())
        self.delivery[self.count] = input

        for i in self.title:
            self.list[i].delete(0, 'end')

        selected_item = self.treeview.selection()
        leng = len(selected_item)

        for i in range(leng):
            value = self.treeview.set(selected_item[i])
            for j in range(len(input)):
                if input[j] != '':
                    value[str(j + 2)] = input[j]
                    for i, k in enumerate(self.title):
                        if j == i:
                            self.controller.controller.cur.execute(
                                'update 요청목록 set %s=\'%s\' where 작성번호=\'%s\'' % (
                                    k, input[j], value['1']))

            self.controller.controller.cur.execute('commit')
            print(value.values())
            self.show()
