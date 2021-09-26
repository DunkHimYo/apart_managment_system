from tkinter import *
from tkinter import ttk


class table(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.list = ['번호', '아이디', '운송번호', '받는사람', '휴대폰번호', '도착지', '현재위치']
        size = [40, 100, 100, 100, 300, 500, 500]
        self.len_size = len(self.list) - 1

        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.len_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.len_size)], height=20)
        self.treeview.pack()

        for i, name in enumerate(self.list):
            self.treeview.column('#' + str(i), width=size[i])
            self.treeview.heading('#' + str(i), text=name)

        self.delivery_entries = {}
        self.delivery = {}

        self.count = 0
        default_x = 460;
        default_y = 520
        main_title = ttk.Frame(self, style='TFrame', width=950, height=400)
        main_title.place(x=default_x, y=default_y)

        Label(self, text='입력창', width=50, height="3", background="burlywood", foreground="maroon").pack(pady=60)

        i = 1
        count = 0
        while i <= self.len_size:
            if i == 1:
                i += 1
            Label(self, text=self.list[i], width=50, background="burlywood", foreground="maroon").pack()
            self.delivery_entries[count] = Entry(self, width=50)
            self.delivery_entries[count].pack()
            i += 1
            count += 1

        def_y = 120
        title = ['조회', '전송', '수정', '삭제', '취소']
        comm = [self.show, self.insert, self.update, self.delete,
                lambda: controller.controller.show_frame("delivery_login")]
        for i in range(len(title)):
            ttk.Button(self, width=13, text=title[i], style="TButton",
                       command=comm[i]).place(x=default_x + 850,
                                              y=default_y - 60 + def_y)
            def_y += 60
        self.show()

    def insert(self):
        input = []
        for i in range(self.len_size - 1):
            input.append(self.delivery_entries[i].get())
        self.delivery[self.count] = input

        for i in range(self.len_size - 1):
            self.delivery_entries[i].delete(0, 'end')
        self.controller.controller.cur.execute(
            """select 총원명부.아이디,관리자.비밀번호,관리자.휴대폰번호 from 총원명부,관리자 where 총원명부.아이디=관리자."아이디" and 관리자.휴대폰번호=\'%s\'
            union select 총원명부.아이디,경비원.비밀번호,경비원.휴대폰번호 from 총원명부,경비원 where 총원명부.아이디=경비원."아이디"and 경비원.휴대폰번호=\'%s\'
            union select 총원명부.아이디,주민.비밀번호,주민.휴대폰번호 from 총원명부,주민 where 총원명부.아이디=주민."아이디"and 주민.휴대폰번호=\'%s\'
            union select 총원명부.아이디,택배기사.비밀번호,택배기사.휴대폰번호 from 총원명부,택배기사 where 총원명부.아이디=택배기사."아이디"and 택배기사.휴대폰번호=\'%s\'"""
            % (self.delivery[self.count][2],self.delivery[self.count][2],self.delivery[self.count][2],self.delivery[self.count][2]))
        self.delivery[self.count].insert(0, self.controller.controller.cur.fetchall()[0][0])
        self.delivery[self.count].append('X')
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

        self.controller.controller.cur.execute('select * from 배송정보')
        self.fetch = self.controller.controller.cur.fetchall()
        self.fetch = sorted(self.fetch)
        for i in range(len(self.fetch)):
            self.treeview.insert('', END, text=self.count + 1, values=self.fetch[i],
                                 iid=str(self.count) + "번")
            self.count += 1

    def delete(self):
        selected_item = self.treeview.selection()
        leng = len(selected_item)
        for i in range(leng):
            self.controller.controller.cur.execute(
                'delete from 배송정보 where 운송번호=\'%s\'' % self.treeview.set(selected_item[i])['2'])
            self.controller.controller.cur.execute('commit')
            self.treeview.delete(selected_item[i])

    def update(self):

        input = []
        for i in range(self.len_size - 1):
            input.append(self.delivery_entries[i].get())
        self.delivery[self.count] = input

        for i in range(self.len_size - 1):
            self.delivery_entries[i].delete(0, 'end')

        selected_item = self.treeview.selection()
        leng = len(selected_item)

        for i in range(leng):
            value = self.treeview.set(selected_item[i])
            for j in range(len(input)):
                if input[j] != '':
                    value[str(j + 2)] = input[j]
                    for k in range(4):
                        if j == k + 1:
                            self.controller.controller.cur.execute(
                                'update 배송정보 set %s=\'%s\' where 운송번호=\'%s\'' % (
                                    self.list[3:][k], input[j], value['2']))

            self.controller.controller.cur.execute('commit')
            self.treeview.item(selected_item[i], values=tuple(value.values()))
