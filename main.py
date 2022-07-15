import sys
import pymongo
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from des import *


class Gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.autorization_status = False
        self.client = pymongo.MongoClient(
            "<mongoDB_connect>"
        )
        self.center_on_screen()

        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.register)

    # Центрируем окно
    def center_on_screen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move(int(resolution.width() / 2) - int(self.frameSize().width() / 2),
                  int(resolution.height() / 2) - int(self.frameSize().height() / 2))

    def check_data(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        # Пытаемся найти наше имя в коллекции
        if login and password:
            search_login = self.client.testdata.users.find_one({"name": login})
            if search_login: # Если нашли значение
                return "value_exists"

            else: # Если значение не было найдено
                return "value_not_found"

        # Если данные не заполнены
        else:
            return "no_data_available"

    def register(self):
        if self.autorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                message = "Такое имя уже используется!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                data = {
                    "name": self.ui.lineEdit.text(),
                    "password": self.ui.lineEdit_2.text(),
                    "time": datetime.datetime.now()
                }
                self.client.testdata.users.insert_one(data)
                message = "Регистрация прошла успешно!"
                QtWidgets.QMessageBox.about(self, "Уведомление", message)
                self.autorization_status = True

            elif result == "no_data_available":
                message = "Данные являются обязательными к заполнению!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

        else:
            message = "Вы авторизованы в системе!"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)

    def login(self):
        if self.autorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                found_user = self.client.testdata.users.find_one({"name": self.ui.lineEdit.text()})
                input_password = self.ui.lineEdit_2.text()

                if input_password == found_user["password"]:
                    message = "Вы были успешно авторизованы!"
                    QtWidgets.QMessageBox.about(self, "Уведомление", message)
                    self.autorization_status = True
                else:
                    message = "Вы указали неверный пароль!"
                    QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                message = "Такого пользователя не существует!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "no_data_available":
                message = "Данные являются обязательными к заполнению!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

        else:
            message = "Вы авторизованы в системе!"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec_())
