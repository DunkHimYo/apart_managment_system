from tkinter import *
from tkinter import ttk
from tkinter import font  as tkfont
import StartPage
import signUp
import manager_request
import time
import findIdPs

class App():

    def __init__(self, img=None, db=None):
        self.tk = Tk()
        self.tk.title("Apartment Management System")
        self.tk.geometry("640x400+100+100")
        self.tk.resizable(True, True)
        self.img = PhotoImage(file=img)

        self._set_style()
        self._font_style()

        self.container = ttk.Frame(self.tk, style='TFrame')
        self.container.pack(side="right", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.label = Label(text="", font=('Helvetica', 20), fg='maroon', bg="blanchedalmond")
        self.label.place(x=1700, y=1000)
        self._update_clock()

        self._crate_frame(frame_list=(StartPage.StartPage, signUp.signUp, manager_request.manager_request, findIdPs.findIdPs))
        self._show_frame("StartPage")

        self.tk.mainloop()

    def _connect_DB(self):
        pass
        # self.connection = orcl.connect(db)
        # self.cur = self.connection.cursor()
    def _set_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', bordercolor="white", background="burlywood", foreground="maroon", anchor='center',
                        justify='center')
        style.configure('my.TButton', relief='flat', background="blanchedalmond", anchor='center', justify='center')
        style.configure('TFrame', bordercolor="white", background="blanchedalmond", relief="solid")
        
    def _font_style(self):
        self.title_font = tkfont.Font(family='굴림', size=30, weight='bold')
        self.sub_font = tkfont.Font(family='굴림', size=20)
        self.nomal_font = tkfont.Font(family='굴림', size=13)

    def _crate_frame(self,frame_list:tuple):
        self.frames = {}
        for F in frame_list:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

    def _show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def _update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.tk.after(1000, self._update_clock)
        return time.strftime('%Y'), time.strftime('%m'), time.strftime('%d'), time.strftime('%H'), time.strftime(
            '%M'), time.strftime('%S')

if __name__ =='__main__':
    App(img="./Image/b.gif", db='c##main/1234@localhost:1521/orcl')
