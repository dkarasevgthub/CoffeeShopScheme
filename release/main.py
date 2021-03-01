import sqlite3
from sys import argv, exit

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QTableWidgetItem

from UI.addEditCoffeeForm import Ui_Form
from UI.main_ui import Ui_MainWindow


class CoffeeShop(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.modified = {}
        self.titles = None
        self.update_result()
        self.update_btn.clicked.connect(self.restart)
        self.add_btn.clicked.connect(self.adding)

    def restart(self):
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        self.result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.cellDoubleClicked.connect(self.editing)
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def editing(self):
        self.wind = Editing(self.tableWidget, self.tableWidget.currentRow())
        self.wind.show()

    def adding(self):
        self.add = Adding(self.tableWidget)
        self.add.show()


class Editing(QWidget, Ui_Form):
    def __init__(self, table, row):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.tableWidget = table
        self.row = row
        self.save_btn.clicked.connect(self.save_results)
        self.id_lbl.setText(self.tableWidget.item(self.row, 0).text())
        self.sort_lbl.setText(self.tableWidget.item(self.row, 1).text())
        self.roast_lbl.setText(self.tableWidget.item(self.row, 2).text())
        self.ground_lbl.setText(self.tableWidget.item(self.row, 3).text())
        self.descrip_lbl.setText(self.tableWidget.item(self.row, 4).text())
        self.price_lbl.setText(self.tableWidget.item(self.row, 5).text())
        self.volume_lbl.setText(self.tableWidget.item(self.row, 6).text())

    def close_event(self):
        self.close()
        res = CoffeeShop()
        res.show()

    def save_results(self):
        self.modified = {'sort': self.sort_lbl.text(),
                         'id': int(self.id_lbl.text()),
                         'roast': int(self.roast_lbl.text()),
                         'condition': self.ground_lbl.text(),
                         'description': self.descrip_lbl.text(),
                         'price': int(self.price_lbl.text()),
                         'volume': int(self.volume_lbl.text())}
        if self.modified:
            cur = self.con.cursor()
            idd = 0
            if self.modified.get('id') is not None:
                idd = self.modified.get('id')
            for key in self.modified.keys():
                que = "UPDATE coffee SET\n"
                que += "{} = '{}'\nWHERE id = {}".format(key, self.modified.get(key), idd)
                cur.execute(que)
            self.con.commit()
            self.modified.clear()
            self.close_event()


class Adding(QWidget, Ui_Form):
    def __init__(self, table):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.tableWidget = table
        self.save_btn.clicked.connect(self.save_results)
        self.id_lbl.setText('')
        self.sort_lbl.setText('')
        self.roast_lbl.setText('')
        self.ground_lbl.setText('')
        self.descrip_lbl.setText('')
        self.price_lbl.setText('')
        self.volume_lbl.setText('')

    def close_event(self):
        self.close()
        res = CoffeeShop()
        res.show()

    def save_results(self):
        self.modified = {'sort': self.sort_lbl.text(),
                         'id': int(self.id_lbl.text()),
                         'roast': int(self.roast_lbl.text()),
                         'condition': self.ground_lbl.text(),
                         'description': self.descrip_lbl.text(),
                         'price': int(self.price_lbl.text()),
                         'volume': int(self.volume_lbl.text())}
        if self.modified:
            cur = self.con.cursor()
            que = \
                f"INSERT INTO coffee({', '.join(list(self.modified.keys()))}) VALUES(" \
                f"'{self.modified['sort']}', {self.modified['id']}, {self.modified['roast']}," \
                f" '{self.modified['condition']}', '{self.modified['description']}'," \
                f" {self.modified['price']}, {self.modified['volume']})"
            print(que)
            cur.execute(que)
            self.con.commit()
            self.modified.clear()
            self.close_event()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = CoffeeShop()
    ex.show()
    exit(app.exec_())
