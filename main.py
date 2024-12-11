import sys
import os
import sqlite3
import mutagen
import datetime

import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.play_stop_Button = QPushButton(parent=self.centralwidget)
        self.play_stop_Button.setGeometry(QRect(340, 500, 101, 51))
        self.play_stop_Button.setObjectName("pushButton")

        self.new_music_button = QPushButton(parent=self.centralwidget)
        self.new_music_button.setGeometry(QRect(450, 500, 61, 51))
        self.new_music_button.setObjectName("pushButton_2")

        self.back_music_Button = QPushButton(parent=self.centralwidget)
        self.back_music_Button.setGeometry(QRect(270, 500, 61, 51))
        self.back_music_Button.setObjectName("pushButton_3")

        self.choose_folder = QPushButton(parent=self.centralwidget)
        self.choose_folder.setGeometry(QRect(20, 240, 191, 61))
        self.choose_folder.setObjectName("pushButton_4")

        self.new_playlist_button = QPushButton(parent=self.centralwidget)
        self.new_playlist_button.setGeometry(QRect(20, 170, 191, 61))
        self.new_playlist_button.setObjectName("pushButton_5")

        self.listView = QListWidget(parent=self.centralwidget)
        self.listView.setGeometry(QRect(240, 40, 531, 431))
        self.listView.setObjectName("listView")

        self.playlistView = QListWidget(parent=self.centralwidget)
        self.playlistView.setGeometry(QRect(10, 40, 211, 121))
        self.playlistView.setObjectName("listView")

        self.volume_Slider = QSlider(parent=self.centralwidget)
        self.volume_Slider.setGeometry(QRect(580, 520, 160, 22))
        self.volume_Slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_Slider.setObjectName("horizontalSlider")

        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(620, 500, 91, 20))
        self.label.setObjectName("label")

        self.label_2 = QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QRect(70, 10, 81, 21))
        self.label_2.setObjectName("label_2")

        self.current_playlist_label = QLabel(parent=self.centralwidget)
        self.current_playlist_label.setGeometry(QRect(480, 10, 81, 21))
        self.current_playlist_label.setObjectName("label_3")

        self.author_label = QLabel(parent=self.centralwidget)
        self.author_label.setGeometry(QRect(10, 290, 221, 71))
        self.author_label.setObjectName("label_4")

        self.name_label = QLabel(parent=self.centralwidget)
        self.name_label.setGeometry(QRect(10, 370, 221, 51))
        self.name_label.setObjectName("label_5")

        self.time_music = QLabel(parent=self.centralwidget)
        self.time_music.setGeometry(QRect(60, 490, 151, 51))
        self.time_music.setObjectName("label_6")

        self.radioButton = QRadioButton(parent=self.centralwidget)
        self.radioButton.setGeometry(QRect(50, 440, 131, 31))
        self.radioButton.setObjectName("radioButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MP3 player"))
        self.play_stop_Button.setText(_translate("MainWindow", "►"))
        self.new_music_button.setText(_translate("MainWindow", ">>"))
        self.back_music_Button.setText(_translate("MainWindow", "<<"))
        self.radioButton.setText(_translate("MainWindow", "Случайный порядок"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">громкость</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Плейлисты</span></p></body></html>"))
        self.current_playlist_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">music</span></p></body></html>"))
        self.author_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Автор</span></p></body></html>"))
        self.choose_folder.setText(_translate("MainWindow", "Добавить музыку"))
        self.name_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Название</span></p></body></html>"))
        self.time_music.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:24pt;\"></span></p></body></html>"))
        self.new_playlist_button.setText(_translate("MainWindow", "Добавить плейлист"))

class MIDI(QMainWindow, Ui_MainWindow):
    # создаем параметы и инициализацию обьекта класса
    def __init__(self):
        super().__init__()
        self.random_choice = False
        # считываем громкость поставленную в предыдущем запуске
        with open("settings.txt", 'r') as settings:
            line = settings.readline()
            self.volume = int(line) / 100
        self.setupUi(self)
        # подключаем слайдер громкости
        self.volume_Slider.setTracking(True)
        self.play = True
        # подключаем таймер PYQT
        self.music_timer = QTimer()
        self.music_timer.setInterval(1000)
        self.music_timer.timeout.connect(lambda: self.blit_time())
        # создаем историю айди прослушанных композиций
        self.history = []
        # насколько далеко мы ушли от текущей композиции
        self.len_recursion = 1
        # слушаем мы текущую или прошлые треки
        self.back = False
        # подключаемся к БД
        self.con = sqlite3.connect('music.sqlite')
        self.cur = self.con.cursor()
        # подключаем плейлисты
        self.playlists = self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()
        self.current_playlist = self.playlists[0][0]
        # сохраняем информацию о текущем треке
        self.current_music_info = [None, None, 1]

        # отображаем плейлисты в виджете
        self.blit_playlists()
        # для случайного переключения создаем список айди непрослушанных треков чтобы случайно из него выбирать
        self.no_played = [i[0] for i in self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]
        # создаем реакции на нажатия кнопок
        self.play_stop_Button.clicked.connect(lambda: self.change_play_stop())
        self.back_music_Button.clicked.connect(lambda: self.music_back())
        self.new_music_button.clicked.connect(lambda: self.change_music())
        self.volume_Slider.sliderReleased.connect(lambda: self.value_changed(self.volume_Slider.value()))
        self.choose_folder.clicked.connect(lambda: self.choose_folder_())
        self.new_playlist_button.clicked.connect(lambda: self.create_new_playlist())
        self.radioButton.toggled.connect(lambda: self.switch_choice())
        self.listView.currentRowChanged.connect(lambda: self.if_new_row())
        self.listView.itemDoubleClicked.connect(lambda: self.delete_music())
        self.playlistView.currentRowChanged.connect(lambda: self.if_playlist_changed(self.playlistView.currentRow()))
        self.playlistView.itemDoubleClicked.connect(lambda: self.delete_playlist())
        #отображаем названия треков в виджете
        self.blit_music()

    # обрабатываем переключение на случайное/последовательное переключение
    def switch_choice(self):
        self.random_choice = self.radioButton.isChecked()

    # обрабатываем смену трека пользователем
    def if_new_row(self):
        if self.listView.currentRow() != -1:
            # загружаем информацию о новом треке
            self.load_mp3(self.cur.execute(f"""SELECT file FROM {self.current_playlist} 
            WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0][0])
            # так как песня изменилась то нужно обновить данные
            self.current_music_info = self.cur.execute(f"""SELECT author, name, duration, file 
            FROM {self.current_playlist} 
            WHERE id = {int(self.listView.currentRow()) + 1}""").fetchall()[0]
            # добавляем предыдущий трек в историю прослушиваний
            if not self.back:
                self.history.append(int(self.listView.currentRow()) + 1)
            self.back = False
            # обновляем надписи автора и названия
            _translate = QCoreApplication.translate
            self.author_label.setText(_translate("MainWindow",
                f"<html><head/><body><p><span style=\" font-size:20pt;\">{self.current_music_info[0]}</span>"
                f"</p></body></html>"))
            self.name_label.setText(_translate("MainWindow",
      f"<html><head/><body><p><span style=\" font-size:16pt;\">{self.current_music_info[1]}</span>"
                f"</p></body></html>"))
            # запускаем отсчет для времени прослушивания
            self.cur_time = 0
            self.music_timer.start(1000)

    # обрабатываение изменения в треках и обновление их в специальном виджете
    def blit_music(self):
        # удаляем чтобы заново записать в виджет
        self.listView.clear()
        # узнаем названия из БД и записываем их в виджет
        for i in self.cur.execute(f"""SELECT name FROM {self.current_playlist} """).fetchall():
            i = i[0]
            self.listView.addItem(i)

    # обрабатывание выбора папки
    def choose_folder_(self):
        # диалог выбора папки
        dirname = QFileDialog.getExistingDirectory(self, 'Выбрать папку', '')
        try:
            # получаем файлы в папке
            files = os.listdir(dirname)
            # получаем максимальный айди если файлы есть и 1 если нет
            try:
                new_id = self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()[-1][0] + 1
            except:
                new_id = 1
            # проверка на mp3
            for i in files:
                if i[-3:] == 'mp3':
                    # записываем в БД сведения
                    self.find_data(dirname, i)
                    new_id += 1
        except:
            pass

    # создание нового плейлиста
    def create_new_playlist(self):
        # диалог выбора названия
        name_playlist, ok = QInputDialog().getText(self, 'Новый плейлист', 'Название:')
        # если не пустая строка и не cancel
        if name_playlist and ok:
            # добавляем новую таблицу и сохраняем изменения
            self.cur.execute(f"""CREATE TABLE {name_playlist} (id INTEGER PRIMARY KEY UNIQUE NOT NULL, author TEXT, 
            name TEXT, file TEXT, duration INTEGER)""")
            self.con.commit()
            # отображаем изменения
            self.playlistView.addItem(name_playlist)

    # загрузка трека из мп3 файла
    def load_mp3(self, filename):
        # создаем ссылку на файл
        media = QUrl.fromLocalFile(filename)
        # создаем экземпляр класса QAudioOutput для загрузки данных о композиции
        self.audio_output = QAudioOutput()
        # создаем экземпляр класса QMediaPlayer для преобразования и вывода аудио
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        # задаем громкость
        self.audio_output.setVolume(self.volume)
        # подгружаем данные
        self.player.setSource(media)
        self.play = False
        self.change_play_stop()

    # изменение параметров и виджетов при включении/выключении музыки
    def change_play_stop(self):
        # если музыка играет, то останавливаем
        if self.play:
            # если ничего не играет чтобы не было ошибки
            if len(self.cur.execute(f"""SELECT name FROM {self.current_playlist} """).fetchall()) != 0:
                # выключаем проигрывание
                self.player.pause()
                self.play = False
                # изменяем надпись кнопки
                _translate = QCoreApplication.translate
                self.play_stop_Button.setText(_translate("MainWindow", "►"))
                self.music_timer.stop()
        # если музыка не играла, то запускаем ее
        else:
            # включаем проигрывание
            self.player.play()
            self.play = True
            # изменяем надпись кнопки
            _translate = QCoreApplication.translate
            self.play_stop_Button.setText(_translate("MainWindow", "||"))
            # включаем таймер для времени прослушивания
            self.music_timer.start()

    # обрабатывание нажатия на виджет возвращающий прошлый трек/ перематывающий в начало
    def music_back(self):
        # останавливаем таймер
        self.music_timer.stop()
        # если двойной клик, то переключаем на предыдущую в истории
        if self.cur_time < 3:
            self.back = True
            # если история пуста
            try:
                # прибавляем в длине рекурсии и изменяем текущий элемент
                self.len_recursion += 1
                self.listView.setCurrentRow(self.history[-1 * self.len_recursion] - 1)
            except:
                self.len_recursion -= 1
        # если музыка играла, то продолжаем проигрывание с начала
        if self.play:
            self.player.play()
            self.cur_time = 0
            self.music_timer.start()

    # обработка изменения громкости
    def value_changed(self, value):
        # Получаем громкость из слайдера, и делим на 100 т.к. громкость в PYQT (0, 1)
        self.volume = value / 100
        # если трека нет, то ничего не делаем
        try:
            self.audio_output.setVolume(self.volume)
        except:
            pass
        # для удобства записываем данные в файл чтобы заново не настраивать
        with open("settings.txt", 'w') as settings:
            settings.write(str(value))

    # заполнение базы данных после выбора папки
    def find_data(self, dirname, filename):
        # получаем путь к файлу
        filename = dirname + '/' + filename
        # считываем информацию о файле через библиотеку mutagen
        audiofile = mutagen.File(filename)
        # получаем данные разделов ID3 - длительность, название, автор
        duration = int(datetime.timedelta(seconds=audiofile.info.length).total_seconds())
        song_title = str(audiofile.tags.getall('TIT2')[0])
        singer_title = str(audiofile.tags.getall('TPE1')[0])
        # получаем айди записи - максимальный айди + 1, если есть записи, 1 если нет записей
        try:
            max_id = self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()[-1][0]
        except:
            max_id = 0
        # проверка на то, что у нас уже есть такой трек
        if len(self.cur.execute(f"""SELECT * FROM {self.current_playlist} WHERE author = ? and name = ?""",
                           (singer_title, song_title)).fetchall()) == 0:
            # добавляем трек в БД
            self.cur.execute(f"""INSERT INTO {self.current_playlist} (id, author, name, file, duration) 
            VALUES (?, ?, ?, ?, ?);""",
                           (max_id + 1, singer_title, song_title, filename, duration))
        # подтверждаем изменения
        self.blit_music()
        self.con.commit()

    # обработка изменения текущего плейлиста
    def if_playlist_changed(self, row):
        # получаем новый плейлист
        self.current_playlist = self.cur.execute("""SELECT name FROM 
        sqlite_master WHERE type='table'""").fetchall()[row][0]
        # изменяем надпись
        _translate = QCoreApplication.translate
        self.current_playlist_label.setText(_translate("MainWindow",f"<html><head/><body><p><span style=\" font-size:12pt;\">{self.current_playlist}</span></p></body></html>"))
        # отображаем новые композиции и обновляем историю и непрослушанные композиции
        self.blit_music()
        self.no_played = [i[0] for i in
                          self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]
        self.history = []

    # отображение текущего времени проигрывания композиции
    def blit_time(self):
        # если время прослушивания не изменилось
        self.cur_time = self.cur_time + 1
        # если музыка все еще идет, то изменяем данные о времени прослушивания
        if int(self.cur_time) <= self.current_music_info[2]:
            _translate = QCoreApplication.translate
            self.time_music.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:24pt;\">{int(self.cur_time)}|{self.current_music_info[2]}</span></p></body></html>"))
        # если музыка кончилась, то изменяем композицию
        else:
            self.change_music()

    # обработка смены музыки
    def change_music(self):
        # если мы сменили музыку на новый трек
        if self.len_recursion == 1:
            # ищем максимальный айди, если не находим то останавливаем
            try:
                max_id = self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()[-1][0]
            except:
                self.player.stop()
                return
            # если переключение случайное, то из не прослушанных случайно выбираем
            if self.random_choice:
                next_music = random.choice(self.no_played)
                # так как композицию мы слушаем то удаляем из не прослушанных
                self.no_played.remove(next_music)
                # если прослушали все, то идем по второму кругу и обновляем список не прослушанных на всю музыку
                if len(self.no_played) == 0:
                    self.no_played = [i[0] for i in
                                      self.cur.execute(f"""SELECT id FROM {self.current_playlist}""").fetchall()]
                    self.no_played.remove(next_music)
            # если последовательное переключение
            else:
                # новый айди
                next_music = self.listView.currentRow() + 2
                # если композиция была последняя, то переключаем в начало
                if next_music > max_id:
                    next_music = 1
        # если мы в истории прослушивания и будет играть не новый трек
        else:
            # позиция глубины рекурсии уменьшается
            self.len_recursion -= 1
            self.back = True
            # переключаем трек на следующий в истории
            next_music = self.history[-1 * (self.len_recursion)]
        # обновляем текущий элемент в виджете вызвав событие которое нам все обработает
        self.listView.setCurrentRow(next_music - 1)
        # запускаем таймер, чтобы показывать время прослушивания
        self.music_timer.stop()
        self.music_timer.start()

    # удалить музыку(двойной лкм)
    def delete_music(self):
        # айди музыки для удаления
        current_id = self.listView.currentRow() + 1
        # создаем список новой истории
        new = []
        # пробегаемся по истории и меняем айди трекам после удаленного в БД
        for j in self.history:
            if j < current_id:
                new.append(j)
            if j > current_id:
                new.append(j - 1)

        self.history = new
        # удаляем нужную композицию из БД
        self.cur.execute(f"""DELETE FROM {self.current_playlist} WHERE id = {current_id}""")
        # для треков, с айди больше, чем айди удаленного трека, понижаем их айди на 1
        result = self.cur.execute(f"""SELECT * FROM {self.current_playlist} WHERE id >= {current_id}""")
        for elem in result:
            self.cur.execute(f"""DELETE FROM {self.current_playlist} WHERE id = {elem[0]}""")
            self.cur.execute(f"""INSERT INTO {self.current_playlist} (id, author, name, file, duration) 
            VALUES (?, ?, ?, ?, ?);""",
                        (elem[0] - 1, elem[1], elem[2], elem[3], elem[4]))
        # подтверждаем изменения и обновляем виджеты
        self.con.commit()
        self.blit_music()
        self.music_timer.stop()
        self.change_music()

    # удалить плейлист(двойной лкм)
    def delete_playlist(self):
        if self.current_playlist != 'music':
            # удаляем плейлист с помощью DROP и подтверждаем, а так же меняем текущий плейлист
            self.cur.execute(f"""DROP TABLE {self.current_playlist}""")
            self.current_playlist = 'music'
            self.con.commit()
        # останавливаем музыку
        self.player.pause()
        self.play = False
        self.music_timer.stop()
        # отображаем плейлисты с изменениями
        self.blit_playlists()

    # отобразить плейлисты в виджете
    def blit_playlists(self):
        self.playlistView.clear()
        # подключаемся к БД и получаем плейлисты
        self.playlists = self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()
        for j in self.playlists:
            j = j[0]
            self.playlistView.addItem(j)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MIDI()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())