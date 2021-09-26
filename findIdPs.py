from tkinter import *
from tkinter import ttk
from operator import itemgetter


class findIdPs(ttk.Frame):

    def __init__(self, parent, controller):

        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.list = {'번호': None, '이름': None, '휴대폰번호': None, '이용자': None, '주소(동/호)': None}
        size = [50, 100, 200, 80, 200, 80, 100]
        self.find_list = {'번호': None, '아이디': None, '비밀번호': None}
        fsize = [50,200, 300]
        self.len_size = len(self.list) - 1
        self.flen_size = len(self.find_list) - 1
        self.treeview = ttk.Treeview(self, columns=[str(i + 1) for i in range(self.flen_size)],
                                     displaycolumns=[str(i + 1) for i in range(self.flen_size)], height=20)
        self.treeview.pack()
        for i, name in enumerate(self.find_list.keys()):
            self.treeview.column('#' + str(i), width=fsize[i], anchor='center')
            self.treeview.heading('#' + str(i), text=name, )

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

            if i == '번호':
                pass
            elif i == '이용원':
                Label(self, text=i, width=50, background="burlywood", foreground="maroon").pack()
                self.combobox = ttk.Combobox(self, height=15, values=self.values, width=48, justify='center')
                self.combobox.pack()
                self.combobox.set("목록 선택")
                self.list[i] = self.combobox

            elif i == '허용여부':
                Label(self, text=i, width=50, background="burlywood", foreground="maroon").pack()
                self.combobox2 = ttk.Combobox(self, height=15, values=self.check, width=48, justify='center')
                self.combobox2.pack()
                self.combobox2.set("목록 선택")
                self.list[i] = self.combobox2

            else:
                Label(self, text=i, width=50, background="burlywood", foreground="maroon").pack()
                self.list[i] = Entry(self, width=50)
                self.list[i].pack()

        def_y = 120
        title = ['조회', '이전']
        comm = [self.show, lambda: controller.show_frame("StartPage")]
        for i in range(len(title)):
            ttk.Button(self, width=13, text=title[i], style="TButton",
                       command=comm[i]).place(x=default_x + 850,
                                              y=default_y - 60 + def_y)
            def_y += 60

    def show(self):
        print(1)

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
        print(self.delivery)
        print('select 아이디,비밀번호 from %s where 주소=\'%s\'' % (
            self.delivery['이용자'], self.delivery['주소(동/호)']))
        self.controller.cur.execute(
            'select 아이디,비밀번호 from %s where 주소=\'%s\'' % (self.delivery['이용자'], self.delivery['주소(동/호)']))
        fetch = self.controller.cur.fetchall()
        print(fetch)

        self.treeview.insert('', END, text=self.count + 1, values=fetch[0], iid=str(self.count) + "번")
        self.count += 1
