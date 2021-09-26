from tkinter import *
from tkinter import ttk
from operator import itemgetter


class signUpList(ttk.Frame):

    def __init__(self, parent, controller, log):

        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.list = {'사용자': None, '아이디': None, '비밀번호': None, '이름': None, '휴대폰번호': None, '이용원': None, '주소(동/호)': None,
                     '허용여부': None}
        size = [50, 100, 200, 80, 200, 80, 100, 100]
        self.len_size = len(self.list) - 1
        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.len_size)], height=20)
        self.treeview.pack()
        for i, name in enumerate(self.list.keys()):
            if i != '사용자':
                self.treeview.column('#' + str(i), width=size[i], anchor='center')
                self.treeview.heading('#' + str(i), text=name, )
            else:
                self.treeview.column('#' + '번호', width=size[i], anchor='center')
                self.treeview.heading('#' + '번호', text=name, )

        self.delivery = {}

        self.count = 0
        default_x = 460;
        default_y = 510
        main_title = ttk.Frame(self, style='TFrame', width=950, height=500)
        main_title.place(x=default_x, y=default_y)

        self.values = ['주민', '경비원', '택배기사', '관리자']
        self.check = ['O', 'X']

        Label(self, text='입력창', width=50, height="3", background="burlywood", foreground="maroon").pack(pady=40)

        for i in self.list.keys():

            Label(self, text=i, width=50, background="burlywood", foreground="maroon").pack()
            if i == '사용자':
                self.combobox = ttk.Combobox(self, height=15, values=self.values, width=48, justify='center')
                self.combobox.pack()
                self.combobox.set("")
                self.list[i] = self.combobox

            elif i == '이용원':
                self.combobox = ttk.Combobox(self, height=15, values=self.values, width=48, justify='center')
                self.combobox.pack()
                self.combobox.set("목록 선택")
                self.list[i] = self.combobox

            elif i == '허용여부':
                self.combobox2 = ttk.Combobox(self, height=15, values=self.check, width=48, justify='center')
                self.combobox2.pack()
                self.combobox2.set("목록 선택")
                self.list[i] = self.combobox2

            else:
                self.list[i] = Entry(self, width=50)
                self.list[i].pack()

        def_y = 120
        title = ['조회', '전송', '수정', '삭제', '이전']
        comm = [self.show, self.insert, self.update, self.delete,
                lambda: controller.controller.show_frame("manager_login")]
        for i in range(len(title)):
            ttk.Button(self, width=13, text=title[i], style="TButton",
                       command=comm[i]).place(x=default_x + 850,
                                              y=default_y - 60 + def_y)
            def_y += 60

        self.show()

    def show(self):
        if self.count != 0:
            for i in range(self.count):
                try:
                    self.treeview.delete(str(i) + "번")
                except:
                    pass
            self.count = 0

        if self.list['사용자'].get() == '':
            self.controller.controller.cur.execute('select * from 회원목록')
            self.fetch = self.controller.controller.cur.fetchall()
            self.fetch = sorted(self.fetch, key=itemgetter(6), reverse=True)

        elif self.list['사용자'].get() in self.values:
            self.controller.controller.cur.execute('select * from %s' % self.list['사용자'].get())
            self.fetch = self.controller.controller.cur.fetchall()

        for i in range(len(self.fetch)):
            if self.list['사용자'].get() in self.values:
                self.fetch[i] = list(self.fetch[i])
                self.fetch[i].insert(4, self.list['사용자'].get())

            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i], iid=str(self.count) + "번")
            self.count += 1

    def insert(self):
        for key, value in self.list.items():
            if key != '사용자':
                self.delivery[key] = value.get()
        c = list(self.delivery.values())
        normal = c[0], c[4]
        self.controller.controller.cur.execute(
            'insert into 총원명부 values %s' % str(tuple(normal)))
        self.controller.controller.cur.execute('commit')

        if self.delivery['이용원'] in self.values and self.delivery['허용여부'] == 'O':
            self.controller.controller.cur.execute(
                'insert into %s values %s' % (self.delivery['이용원'], str(tuple(c[0:4] + c[5:6]))))

        self.controller.controller.cur.execute('commit')
        for i in self.list.keys():
            try:
                self.list[i].delete(0, END)
            except:
                pass

        self.count += 1

    def delete(self):
        selected_item = self.treeview.selection()
        leng = len(selected_item)
        for i in range(leng):
            self.controller.controller.cur.execute(
                'delete from 회원목록 where 아이디=\'%s\'' % self.treeview.set(selected_item[i])['1'])
            self.controller.controller.cur.execute('commit')
            self.treeview.delete(selected_item[i])

    def update(self):
        for key, value in self.list.items():
            try:
                self.delivery[key] = value.get()
            except:
                pass
        for i in self.list.keys():
            try:
                self.list[i].delete(0, END)
            except:
                pass
        selected_item = self.treeview.selection()
        size = len(selected_item)
        for i in range(size):
            t_value = self.treeview.set(selected_item[i])
            check = [i == '' or i == '목록 선택' for i in self.delivery.values()]
            if True in check:
                for j, (key, value) in enumerate(self.delivery.items()):
                    check = [i == '' or i == '목록 선택' for i in self.delivery.values()]
                    if check[j] == False:
                        t_value[str(j + 1)] = key[1]
                        self.controller.controller.cur.execute(
                            'update 회원목록 set %s=\'%s\' where 아이디=\'%s\'' % (key, value, t_value['1']))
                        self.controller.controller.cur.execute('commit')

        self.controller.controller.cur.execute('select * from 회원목록')
        c = self.controller.controller.cur.fetchall()
        for i in range(len(c)):
            if c[i][6] == 'O':
                normal = c[i][0], c[i][4]
                self.controller.controller.cur.execute(
                    'insert into 총원명부 values %s' % str(tuple(normal)))
                self.controller.controller.cur.execute('commit')

                if normal[1] in self.values:
                    self.controller.controller.cur.execute(
                        'insert into %s values %s' % (normal[1], str(tuple(c[i][0:4] + c[i][5:6]))))
                self.controller.controller.cur.execute('commit')
                self.delete()
        self.show()
