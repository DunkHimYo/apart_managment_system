from tkinter import ttk
from tkinter import *
from tkinter import messagebox


class signUp(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.information = {}

        x_main = 690
        y_main = 100

        main_title = ttk.Frame(self, style='TFrame', width=500, height=600)
        main_title.place(x=x_main, y=y_main)

        main_label = ttk.Label(self, text='AMS', width=21, style='TButton', foreground="maroon", font="굴림 30")
        main_label.place(x=x_main, y=y_main)
        # id_start

        #   id_label_start
        x_st = 40
        x_nd = 140
        y_st = 130

        # label
        self.label_list = {'아이디': None, '비밀번호': None, '이름': None, '휴대폰 번호': None, '이용자': None, '주소(동/호)': None}
        self.values = ['주민', '경비원', '택배기사']
        self.size = len(self.label_list)
        for i in self.label_list.keys():
            label = ttk.Label(self, text=i, style='TButton', width=9, foreground="maroon")
            label.place(x=x_main + x_st, y=y_main + y_st)

            if i == '이용자':
                self.combobox = ttk.Combobox(self, height=15, values=self.values)
                self.combobox.place(x=x_main + x_nd, y=y_main + y_st)
                self.combobox.set("목록 선택")
                self.label_list[i] = self.combobox

            else:
                self.label_list[i] = Entry(self, font="굴림 20", width=13)
                self.label_list[i].place(x=x_main + x_nd, y=y_main + y_st)

            y_st += 60

        # tail_start
        y_st += 60
        label_list = ['회원가입', '취소']
        for i, label_i in enumerate(label_list):
            x_main += x_st
            if label_i == '회원가입':
                label = ttk.Button(self, text=label_list[i], width=15, style='TButton',
                                   command=lambda: controller.show_frame("StartPage"))
                label.bind("<Button-1>", self.com)
            else:
                label = ttk.Button(self, text=label_list[i], width=15, style='TButton',
                                   command=lambda: controller.show_frame("StartPage"))
                label.bind("<Button-1>", self.clearTextInput)
            label.place(x=x_main, y=y_main + y_st)
            x_main += x_nd

    # tail_end

    def com(self, event):
        for key, value in self.label_list.items():
            self.information[key] = value.get()
        b = list(self.information.values())
        b.insert(self.size + 1, 'X')

        try:
            self.controller.cur.execute('insert into 회원목록 values %s' % str(tuple(b)))
            self.controller.cur.execute('commit')
        except:
            messagebox.showinfo("에러", "동일한 아이디가 존재합니다.")
        self.clearTextInput()

    def clearTextInput(self, event=0):

        for i in range(self.size):
            try:
                self.label_list[i].delete(0, END)
            except:
                pass
