import tkinter
from enum import Enum
from tkinter import *

from sorter import Sorter
import tkinter.messagebox as mb

def browsePatch():
    sorter.browsePatch()

def browsePatchToExit():
    sorter.browsePatchToExit()

def startSort():
    sorter.startSort()

def setIsDir():
    sorter.setIsDir(var.get())


class App(Frame):

    def __init__(self):
        super().__init__()
        global sorter
        self.initUI()
        sorter = Sorter(self, self.entryPatch, self.entryPatchToExit, self.lblProcess, self.btnStart, self.troubleFrame, self.troublesList)
        self.lblPatch = Label
        self.lblProcess = Label
        self.btnStart = Button
        self.entryPatch = Entry
        self.entryPatchToExit = Entry
        self.boxUseDirs = Checkbutton
        self.troublesList = Text
        self.troubleFrame = Frame
        # self.entryDate1 = Entry
        # self.entryDate2 = Entry

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        patchesFrame = Frame(self, pady=5)
        patchesFrame.pack(side=TOP, fill=X)

        patchToExitFrame = Frame(patchesFrame, pady=5)
        patchToExitFrame.pack(side=TOP, fill=X)
        self.lblPatchToExit = Label(patchToExitFrame, text="отсортировать в:", width=15)
        self.lblPatchToExit.pack(side=LEFT, padx=5, pady=5)
        self.entryPatchToExit = Entry(patchToExitFrame)
        self.entryPatchToExit.pack(side=LEFT, fill=X, padx=5, expand=True)
        btnPatchToExitFind = Button(patchToExitFrame, cursor="hand2", text="поиск", command=browsePatchToExit)
        btnPatchToExitFind.pack(side=LEFT, padx=5)

        patchFrame = Frame(patchesFrame)
        patchFrame.pack(side=TOP, fill=X)
        self.lblPatch = Label(patchFrame, text="каталог с фото:", width=15)
        self.lblPatch.pack(side=LEFT, padx=5, pady=5)
        self.entryPatch = Entry(patchFrame)
        self.entryPatch.pack(side=LEFT, fill=X, padx=5, expand=True)
        btnPatchFind = Button(patchFrame, cursor="hand2", text="поиск", command=browsePatch)
        btnPatchFind.pack(side=LEFT, padx=5)

        dirFrame = Frame(self)
        dirFrame.pack(side=TOP, fill=X)
        global var
        var = IntVar()
        var.set(0)
        self.boxUseDirs = Checkbutton(dirFrame, text="просмотр внутренних папок", variable=var,
                 onvalue=1, offvalue=0,
                 command=setIsDir)
        self.boxUseDirs.pack(side=LEFT, padx=5, pady=5)

        # dateFrame = Frame(self)
        # dateFrame.pack(side=TOP, fill=X)
        # lblDate1 = Label(dateFrame, text="дата с:", width=8)
        # lblDate1.pack(side=LEFT, padx=5, pady=5)
        # self.entryDate1 = Entry(dateFrame)
        # self.entryDate1.pack(side=LEFT, fill=X, padx=5, expand=True)
        # lblDate2 = Label(dateFrame, text="по:", width=2)
        # lblDate2.pack(side=LEFT, padx=5, pady=5)
        # self.entryDate2 = Entry(dateFrame)
        # self.entryDate2.pack(side=LEFT, fill=X, padx=5, expand=True)


        self.troubleFrame = Frame(self)
        self.troubleFrame.pack(side=TOP, fill=X)
        # lblTroubles = Label(self.troubleFrame, text="не удалось обработать", width=30)
        # lblTroubles.pack(side=TOP, padx=5, pady=5)

        listFrame = Frame(self.troubleFrame)
        listFrame.pack(side=TOP, fill=X)

        scrollbar = Scrollbar(listFrame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)
        self.troublesList = Text(listFrame, width=20, height=4, yscrollcommand=scrollbar.set)
        self.troublesList.pack(anchor=CENTER, padx=5, pady=5, fill=X)
        scrollbar.config(command=self.troublesList.yview)

        #self.troubleFrame.pack_forget()

        startFrame = Frame(self)
        startFrame.pack(anchor=S,  expand=True, pady=20)
        self.btnStart = Button(startFrame, cursor="hand2", text="начать", command=startSort)
        self.btnStart.pack(side=LEFT, fill=X, padx=5)
        self.lblProcess = Label(startFrame, text="идет обработка", width=15)
        self.lblProcess.pack(side=LEFT, padx=5)
        self.lblProcess.pack_forget()


    class Message(Enum):
        ERROR = 1
        WARNING = 2
        INFO = 3
        ASK_START = 4

    def messageWindow(self, type, msg):
        answ = 0
        match type:
            case self.Message.WARNING: mb.showwarning("предупреждение", msg)
            case self.Message.INFO: mb.showinfo("информация", msg)
            case self.Message.ERROR: mb.showerror("ошибка", msg)
            case self.Message.ASK_START: answ = mb.askokcancel("путь не задан", msg)

        if answ == 1:
            browsePatch()


def main():
    root = Tk()
    app = App()
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    x = (width / 2) - (width / 6)
    y = (height / 2) - (height / 8)
    root.geometry('%dx%d+%d+%d' % (width / 4, height / 3, x, y))
    root.minsize(int(width / 4), int(height / 3))
    root.maxsize(int(width / 2), int(height / 3))
    root.iconphoto(True, tkinter.PhotoImage(file='./icon.png'))
    root.title("Сортировщик фото")
    root.mainloop()


if __name__ == '__main__':
    main()

