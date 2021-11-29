import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from addEditCoffeeForm import Ui_MainWindow_1
from main_ui import Ui_MainWindow_2


class Yes(QMainWindow, Ui_MainWindow_1):
    def __init__(self, main):
        self.main = main
        super().__init__()
        #uic.loadUi('addEditCoffeeForm.ui', self)
        self.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())
        self.connection = sqlite3.connect("data/coffee.db")
        self.lines = [self.lineEdit, self.lineEdit_2,self.lineEdit_3,
                  self.lineEdit_4,self.lineEdit_5,self.lineEdit_6]
        self.flag = False
        self.pushButton.clicked.connect(self.p)

    def add(self):
        self.flag = False
        for e in self.lines:
            e.setText("")
        self.show()

    def edit(self, id, six):
        self.flag = True
        self.id = id
        for e in range(6):
            self.lines[e].setText(six[e])
        self.show()

    def p(self):
        if self.flag:
            self.connection.cursor().execute("""UPDATE sorts
                                SET title = ?, power = ?, ground = ?, taste = ?, price = ?, volume = ?
                                WHERE id = ?""", tuple(map(lambda x: x.text(), self.lines)) + tuple([self.id]))
            self.connection.commit()
            self.hide()
            self.main.loadTable()
            return
        else:
            self.connection.cursor().execute("""INSERT INTO sorts(title, power, ground, taste, price, volume)
                                 VALUES(?, ?, ?, ?, ?, ?)""", tuple(map(lambda x: x.text(), self.lines)))
            self.connection.commit()
            self.hide()
            self.main.loadTable()
            return


class MyWidget(QMainWindow, Ui_MainWindow_2):
    def __init__(self):
        super().__init__()
        #uic.loadUi('main.ui', self)
        self.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())
        self.sqlconnect = sqlite3.connect("data/coffee.db")
        self.loadTable()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.yes = Yes(self)

    def loadTable(self):
        data = self.sqlconnect.cursor().execute("""SELECT * FROM sorts""")
        self.tableWidget.setColumnCount(7)
        title = ["id", "title", "power", "ground", "taste", "price", "volume"]
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def add(self):
        self.yes.add()

    def edit(self):
        ind = self.tableWidget.currentRow()
        a = []
        for e in range(1, 7):
            a.append(self.tableWidget.item(ind, e).text())
        ind = int(self.tableWidget.item(ind, 0).text())
        self.yes.edit(ind, a)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
