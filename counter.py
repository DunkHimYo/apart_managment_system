from tkinter import *
from tkinter import ttk
import controlBar
import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import *


class counter(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.value = {'Date': None, 'Open': 0, 'High': 0, 'Low': 0, 'Close': 0}
        size = {'x': 70, 'y': 150}
        ttk.Frame(self, style='TFrame', width=500, height=600).place(x=size['x'], y=size['y'])
        self.count = 0
        ttk.Label(self, text="최대 수용인원 50명", style='my.TButton', font=('굴림', 20)).place(x=size['x'] * 2 + 40, y=200)
        self.label = ttk.Label(self, text="0" + "명", style='my.TButton', font=('굴림', 50))
        self.label.place(x=size['x'] * 2 - 40, y=400)

        ttk.Button(self, text='+', width=15, command=self.countUP, style='TButton').place(x=size['x'] * 2,
                                                                                          y=700)

        ttk.Button(self, text='-', width=15, command=self.countDown, style='TButton').place(x=size['x'] * 2 + 180,
                                                                                            y=700)

        self.date_id = '-'.join(self.controller.controller.update_clock()[0:3]) + ' ' + ':'.join(
            [self.controller.controller.update_clock()[3], '00'])
        print(self.controller.controller.update_clock()[0:6])
        self.gra()

        controlBar.controlBar(self)

    def gra(self):
        try:
            self.controller.controller.cur.execute('select * from 시간대목록')
            self.graph_data = self.controller.controller.cur.fetchall()
            self.graph_data = pd.DataFrame(self.graph_data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
            self.graph_data.index = pd.DatetimeIndex(self.graph_data['Date'])
            del self.graph_data['Date']
            try:
                self.fig, self.ax = mpf.plot(self.graph_data, type='candle', style='charles', returnfig=True, ylabel='',
                                             figsize=(7, 4))
                canvas = FigureCanvasTkAgg(self.fig, master=self)
                canvas.get_tk_widget().place(x=585, y=300)
                a = self.controller.controller.tk.after(60000, self.gra)
            except:
                pass
            else:
                self.update()
        except:
            self.controller.controller.tk.after_cancel(a)

    def update(self):
        date = list(map(int, self.controller.controller.update_clock()))

        label = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
        date = {key: value for key, value in zip(label, date)}
        if date['Hour'] == 13 and date['Minute'] == 0:

            self.value['Date'] = self.date_id
            self.value['Open'] = self.count
            self.value['High'] = self.count
            self.value['Low'] = self.count
            self.value['Close'] = self.count
            self.controller.controller.cur.execute(
                'insert into 시간대목록 values %s' % str(tuple(self.value.values())))
            self.controller.controller.cur.execute('commit')

        elif date['Hour'] > 13 and date['Minute'] == 0:
            date_id = '-'.join(self.controller.controller.update_clock()[0:3]) + ' ' + ':'.join(
                [str(eval(self.controller.controller.update_clock()[3] + '-1')), '00'])

            self.controller.controller.cur.execute(
                'select \"Close\" from 시간대목록 where \"Date\" = \'%s\'' % date_id)
            try:
                Close = self.controller.controller.cur.fetchall()[0][0]
                self.value['Date'] = self.date_id
                self.value['Open'] = Close
                self.value['High'] = Close
                self.value['Low'] = Close
                self.value['Close'] = Close
                self.controller.controller.cur.execute(
                    'insert into 시간대목록 values %s' % str(tuple(self.value.values())))
                self.controller.controller.cur.execute('commit')
            except:
                pass
            else:
                self.controller.controller.tk.after(1000, self.update)

    def countUP(self):

        if self.count < 50:
            self.count += 1
            self.label.config(text=str(self.count) + '명')

        if self.value['High'] > self.count:
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"Close\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))

        else:
            self.value['High'] = self.count
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"High\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"Close\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))

        self.controller.controller.cur.execute('commit')

    def countDown(self):
        if self.count == 0:
            pass
        else:
            self.count -= 1
            self.label.config(text=str(self.count) + '명')

        if self.value['Low'] < self.count:
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"Close\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))

        else:
            self.value['Low'] = self.count
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"Low\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))
            self.controller.controller.cur.execute(
                'update 시간대목록 set \"Close\"=\'%s\' where \"Date\"=\'%s\'' % (self.count, self.date_id))

        self.controller.controller.cur.execute('commit')
