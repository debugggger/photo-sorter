import shutil
import threading
from datetime import datetime
from tkinter import filedialog, END
from threading import Thread

from exif import Image
import os
import pipes
import platform
import subprocess

class Sorter(object):
    def __init__(self, app, entryPatch, entryPatchToExit, procLabel, btnStart, troubleFrame, troublesList, entryDate1, entryDate2):
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
        self.date1 = ''
        self.date2 = ''
        self.entryDate1 = entryDate1
        self.entryDate2 = entryDate2
        self.startDate = datetime.strptime("1970-01-01", "%Y-%m-%d")
        self.endDate = datetime.now()

    def setIsDir(self, var):
        self.isDir = var

    def checkDate(self):
        self.date1 = self.entryDate1.get()
        self.date2 = self.entryDate2.get()

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
                            self.readDataFromImage(file, path, current.split('.')[-1], month_list)
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

        self.date1 = self.entryDate1.get()
        self.date2 = self.entryDate2.get()

        if self.date1 != '':
            try:
                self.startDate = datetime.strptime(self.date1, "%Y-%m-%d")
            except:
                self.app.messageWindow(self.app.Message.WARNING, "Укажите дату в формате YYYY-MM-DD")
                return
            if self.date2 == '':
                self.date2 = datetime.now().date()

                self.entryDate2.insert("end", self.date2)
            else:
                if self.date2 > datetime.now():
                    self.date2 = datetime.now().date()
                try:
                    self.endDate = datetime.strptime(self.date2, "%Y-%m-%d")
                except:
                    self.app.messageWindow(self.app.Message.WARNING, "Укажите дату в формате YYYY-MM-DD")


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
                        self.readDataFromImage(file, self.patch, file.split('.')[-1], month_list)
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

    def readDataFromImage(self, file, patch, fileType, month_list=[]):

        global metaDate, dateStr
        isFile = 0
        year = 0
        month = 0
        if fileType == 'jpg' or fileType == 'JPG' or fileType == 'png' or fileType == 'PNG':
            image = Image(patch + "/" + file)
            if image.has_exif:
                isFile = 1
                metaDatePh = image.datetime_original
                data = str(metaDatePh).split(':')
                metaDatePhData = str(metaDatePh).split(' ')
                dateStr = datetime.strptime(metaDatePhData[0], "%Y:%m:%d").date()
                year = data[0]
                month = data[1]

        if fileType == 'mp4' or fileType == 'MP4':

            path_to_video = patch + "/" + file
            try:
                with open(os.devnull, 'w') as tempf:
                    subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
            except FileNotFoundError:
                raise IOError('ffprobe not found.')

            if os.path.isfile(path_to_video):
                if platform.system() == 'Windows':
                    cmd = ["ffprobe", "-show_streams", path_to_video]
                else:
                    cmd = ["ffprobe -show_streams " + pipes.quote(path_to_video)]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                stream = False

                for line in iter(p.stdout.readline, b''):
                    line = line.decode('UTF-8')
                    if '[STREAM]' in line:
                        stream = True
                    elif '[/STREAM]' in line and stream:
                        stream = False
                    elif stream:
                        if line.__contains__("TAG:creation_time"):
                            data = str(line).split('=')
                            metaDate = str(data[1]).split('T')
                            break

            dateStr = datetime.strptime(metaDate[0], "%Y-%m-%d").date()
            isFile = 1
            data = str(dateStr).split('-')
            year = data[0]
            month = data[1]

        if self.startDate.date() <= dateStr and self.endDate.date() >= dateStr and isFile == 1:
            exitPatch = self.PatchToExit + "/" + year + "/" + month_list[int(month) - 1]
            if not os.path.exists(exitPatch):
                os.makedirs(exitPatch)
            shutil.copyfile(patch + "/" + file, exitPatch + "/" + file)

        percent = int(self.fineshedCount / self.countImages * 100)
        if percent > 100:
            percent = 100
        self.procLbl.configure(text="обработано " + str(percent) + "%")
