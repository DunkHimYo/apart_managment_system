from tkinter import ttk
from tkinter import *
import controlBar2
import manager_login

class show_request(ttk.Frame):

    def __init__(self, parent, controller, log, data):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.data=data
        self.log = log
        self.information_entity = {}
        self.information = {}
        self.str_information = {}
        self.count = 0
        default_x = 100
        default_y = 150

        main_title = ttk.Frame(self, style='TFrame', width=1100, height=600)
        main_title.place(x=default_x, y=default_y)

        main_label = ttk.Label(self, text='요청 문의', width=21, style='TButton', foreground="maroon", font="굴림 30")
        main_label.place(x=default_x, y=default_y)
        # id_start

        #   id_label_start
        x_st = 40
        x_nd = 140
        y_st = 130

        # label
        label_list = ['제목', '내용']
        self.size = len(label_list)
        for i in range(self.size):
            label = ttk.Label(self, text=label_list[i], style='TButton', width=9, foreground="maroon")
            label.place(x=default_x + x_st, y=default_y + y_st)
            if i == 0:
                self.information_entity[i] = Entry(self, font="굴림 20", width=50,disabledbackground='white')
                self.information_entity[i].place(x=default_x + x_nd, y=default_y + y_st)
                self.information_entity[i].insert(0,data[1])
                self.information_entity[i].configure(state='disabled')

            else:
                self.information_entity[i] = Text(self, font="굴림 20", width=50, height=10)
                self.information_entity[i].place(x=default_x + x_nd, y=default_y + y_st)
                self.information_entity[i].insert(INSERT, data[2])
                self.information_entity[i].configure(state='disabled')
            y_st += 60
        controlBar2.controlBar2(self)
