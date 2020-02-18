from PyQt5.QtWidgets import QApplication, QDialog
import sys
from support.gui2 import Ui_Dialog
from support.model import Model
from queue import Queue
import threading
import time
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from support.pybot2 import PyBot
from support.fuzzy import Fuzzy
from support.database import Dbase


class Ctrl(QDialog):
    def __init__(self):
        super(Ctrl,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.model = Model()
        self.q = Queue()
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.StartButton.clicked.connect(self.process)
        canvas = FigureCanvas(Figure(figsize=(5,3)))
        self.ui.verticalLayout.addWidget(canvas)
        self.axline = canvas.figure.subplots()
        self.x = []
        self.y = []
        self.z = []
        self.bot = PyBot()
        self.fuzy = Fuzzy()
        self.datBase =Dbase()

    def process(self):
        nama = self.ui.lineEdit.text()
        self.datBase.create(nama)
        self.tanggal = time.strftime('%d_%m_%Y')
        self.datBase.WFile(self.tanggal)
        self.runner = True
        self.t2 = threading.Thread(target=self.get_data)
        self.t3 = threading.Thread(target=self.bot.init)
        self.t2.start()
        self.t3.start()

    def stop(self):
        self.datBase.saveit(self.tanggal)
        self.runner = False
        self.t2.join()
        self.t3.join()
        self.bot.updater.stop()


    def get_data(self):
        while self.runner:
            port = self.ui.lineEdit_3.text()
            self.model.comm(port)
            self.data = self.model.rawdata
            self.raw = self.data.split(";")
            self.hbeat = float(self.raw[0])
            self.oxy = float(self.raw[1])
            self.waktu = time.strftime("%H:%S")
            self.fuzy.fuzzifikasi(self.hbeat, self.oxy)
            self.z.append(self.hbeat)
            self.x.append(self.waktu)
            self.y.append(self.oxy)
            self.datBase.Fillinit(self.hbeat, self.oxy, self.fuzy.keputusan, self.waktu)
            self.ui.label_9.setText(self.fuzy.keputusan)
            self.bot.get_val(self.hbeat,self.oxy, self.fuzy.keputusan)
            if self.fuzy.keputusan == 'Kritis':
                self.bot.warning()
            if len(self.x) == 10:
                self.up_plot()

    def up_plot(self):
        self.axline.clear()
        line1, = self.axline.plot(self.x, self.y, label='SpO2')
        line2, = self.axline.plot(self.x, self.z, label='Detak Jantung')
        self.axline.legend(handles=[line1, line2])
        self.axline.figure.canvas.draw()
        self.x.pop(0)
        self.y.pop(0)
        self.z.pop(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ctrl()
    window.setWindowTitle("Monitoring Vital Sign")
    window.show()
    sys.exit(app.exec_())