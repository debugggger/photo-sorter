import os
import shutil
import threading
from datetime import datetime
from tkinter import filedialog, END

import time

from threading import Thread

class Sorter(object):
    def __init__(self, app, entryPatch, entryPatchToExit, procLabel, btnStart, troubleFrame, troublesList):
        self.patch = ''
        self.PatchToExit = ''
        self.countImages = 0
        self.app = app
        self.entryPatch = entryPatch
        self.entryPatchToExit = entryPatchToExit
        self.procLbl = procLabel
        self.stopThread = threading.Event()
        self.btnStart = btnStart
        self.troubleFrame = troubleFrame
        self.troublesList = troublesList
        self.isDir = 0
        self.fineshedCount = 0
        self.troubleFiles = []
        self.errorCount = 0

    def setIsDir(self, var):
        self.isDir = var

    def browsePatch(self):
        self.entryPatch.delete(0, END)
        self.patch = filedialog.askdirectory(initialdir="/", title="Выбор папки")
        self.entryPatch.insert(0, self.patch)
        self.troubleFiles = []
        self.findImages()

    def browsePatchToExit(self):
        self.entryPatchToExit.delete(0, END)
        self.PatchToExit = filedialog.askdirectory(initialdir="/", title="Выбор папки")
        self.entryPatchToExit.insert(0, self.PatchToExit)
        self.troubleFiles = []
        for i in range(len(self.troubleFiles)):
            self.troublesList.insert("end", self.troubleFiles[i])
        self.troubleFrame.pack()

    def checkDirs(self, path, mode, **kwargs):
        month_list = kwargs.get('month_list', None)
        for file in os.listdir(path):
            current = path + "/" + file
            if os.path.isdir(current):
                self.checkDirs(current, mode, month_list=month_list)
            if current.split('.')[-1] == 'jpg' or current.split('.')[-1] == 'JPG' or current.split('.')[-1] == 'png'\
                    or current.split('.')[-1] == 'PNG' or current.split('.')[-1] == 'mp4' or current.split('.')[-1] == 'MP4':
                if mode == "find":
                    self.countImages += 1
                if mode == "work":
                    self.fineshedCount += 1
                    with open(current, "rb"):
                        try:
                            self.readDataFromImage(file, path, month_list)
                        except:
                            self.errorCount += 1
                            self.troubleFiles.append(path + "/" + file+"\n")

    def findImages(self):
        if self.patch == '':
            return

        self.countImages = 0
        for file in os.listdir(self.patch):
            current = self.patch+"/"+file
            if os.path.isdir(current) and self.isDir == 1:
                self.checkDirs(current, "find")

            if current.split('.')[-1] == 'jpg' or current.split('.')[-1] == 'JPG' or current.split('.')[-1] == 'png'\
                    or current.split('.')[-1] == 'PNG' or current.split('.')[-1] == 'mp4' or current.split('.')[-1] == 'MP4':
                self.countImages += 1

        if self.countImages == 0:
            self.app.messageWindow(self.app.Message.WARNING, "фото не найдены")

    def startSort(self):
        threadSorting = Thread(target=self.sortByData)
        threadSorting.start()

    def sortByData(self):

        # if self.date1 != '':
        #     try:
        #         datetime.datetime.strptime(str(self.date1), '%Y-%m-%d')
        #     except:
        #         self.app.messageWindow(self.app.Message.WARNING, "Укажите дату в формате YYYY-MM-DD")
        #         return

        self.findImages()
        if self.countImages == 0:
            return

        self.troubleFiles = []
        self.troublesList.delete(1.0, END)

        self.errorCount = 0
        if self.patch == '':
            self.app.messageWindow(self.app.Message.ASK_START, "не указан путь для поиска файлов\n\nуказать?")
            return

        if self.PatchToExit == '':
            self.PatchToExit = self.patch
            self.entryPatchToExit.insert(0, self.PatchToExit)

        self.procLbl.pack()
        self.btnStart.pack_forget()

        exitErrorPatch = self.PatchToExit + "/error/"

        month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

        for file in os.listdir(self.patch):

            current = self.patch + "/" + file
            if os.path.isdir(current) and self.isDir == 1:
                self.checkDirs(current, "work", month_list=month_list)

            if file.split('.')[-1] == 'jpg' or file.split('.')[-1] == 'JPG' or file.split('.')[-1] == 'png'\
                    or current.split('.')[-1] == 'PNG' or current.split('.')[-1] == 'mp4' or current.split('.')[-1] == 'MP4':
                try:
                    with open(current, "rb"):
                        self.readDataFromImage(file, self.patch, month_list)
                except:
                    self.errorCount += 1
                    self.troubleFiles.append(self.patch + "/" + file + "\n")
                    if not os.path.exists(exitErrorPatch):
                        os.makedirs(exitErrorPatch)
                    shutil.copyfile(self.patch + "/" + file, exitErrorPatch + file)
            self.fineshedCount += 1
        if self.errorCount != 0:
            self.troublesList.insert("end", "не удалось обработать:\n")

            for i in range(len(self.troubleFiles)):
                self.troublesList.insert("end", self.troubleFiles[i])
            self.troublesList.insert("end", "\n" + "Файлы размещены в: " + exitErrorPatch + "\n")
            self.troubleFrame.pack()
        else:
            self.app.messageWindow(self.app.Message.INFO, "обработка успешна завершена")
        self.procLbl.pack_forget()
        self.btnStart.pack()
        self.stopThread.set()

    def readDataFromImage(self, file, patch, month_list=[]):

        ti_m = os.path.getmtime(patch+"/"+file)
        dateStr = datetime.strptime(time.ctime(ti_m), "%a %b %d %H:%M:%S %Y")

        data = str(dateStr).split('-')
        year = data[0]
        month = data[1]

        exitPatch = self.PatchToExit + "/" + year + "/" + month_list[int(month) - 1]
        if not os.path.exists(exitPatch):
            os.makedirs(exitPatch)
        shutil.copyfile(patch + "/" + file, exitPatch + "/" + file)

        percent = int(self.fineshedCount / self.countImages * 100)
        if percent > 100:
            percent = 100
        self.procLbl.configure(text="обработано " + str(percent) + "%")
