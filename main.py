import sqlite3
import sys

from UI.UI import *
from UI.addEditCoffeeForm import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QDialog, QTableWidgetItem


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.db")
        self.AddBtn.clicked.connect(self.addCall)
        self.EditBtn.clicked.connect(self.editCall)
        self.show_data()

    def show_data(self):
        res = self.connection.cursor().execute('''
        SELECT * from coffee''').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def addCall(self):
        addEditCoffeeForm(self, None, None).exec_()

    def editCall(self):
        #self.tableWidget = QTableWidget(self)
        try:
            id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        except Exception:
            self.label.setText('Ошибка')
            return
        self.label.setText('')
        data = [self.tableWidget.item(self.tableWidget.currentRow(), i).text()
                for i in range(1, 7)]
        addEditCoffeeForm(self, id, data).exec_()

    def unpack(self, id, data, delete):
        if id is None:
            req = f'''insert into
            coffee(name, obzharka, type, descr, price, volume)
            values('{"', '".join(data)}')'''
        elif delete:
            req = f'''delete from coffee
            where id = {id}'''
        else:
            print('edit', id, data)
            req = f'''update coffee set
            name = "{data[0]}",
            obzharka = "{data[1]}",
            type = "{data[2]}",
            descr = "{data[3]}",
            price = "{data[4]}",
            volume = "{data[5]}" where id = {id}'''
        self.connection.cursor().execute(req).fetchall()
        self.connection.commit()
        self.show_data()

    def closeEvent(self, event):
        self.connection.close()


class addEditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self, win, id, data):
        super().__init__()
        self.setupUi(self)
        self.win = win
        self.id = id
        if id is not None:
            self.setWindowTitle('Редактировать данные')
            self.name.setText(data[0])
            self.obzharka.setText(data[1])
            self.type.setText(data[2])
            self.descr.setText(data[3])
            self.price.setText(data[4])
            self.volume.setText(data[5])
        else:
            self.setWindowTitle('Добавить данные')
            self.DelBtn.setEnabled(False)
        self.DelBtn.clicked.connect(self.confirm)
        self.ConfirmBtn.clicked.connect(self.confirm)

    def confirm(self):
        try:
            self.win.unpack(self.id, (self.name.text(),
                                 self.obzharka.text(),
                                 self.type.text(),
                                 self.descr.text(),
                                 self.price.text(),
                                 self.volume.text()), self.sender() is self.DelBtn)
            self.close()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())