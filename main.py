from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from enter import Ui_Menu
from two import Ui_two
from one import Ui_one
import sys
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator



def predict(fname):
    model = load_model('my_model.h5')
    test_dir = fname
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_datagen.flow_from_directory(
        test_dir,

        target_size=(224, 224),

        batch_size=16,

        class_mode='binary',

        shuffle=False)
    res = model.predict(test_generator)
    return res
def predict2():
    model = load_model('my_model.h5')
    test_dir = "one"
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_datagen.flow_from_directory(
        test_dir,

        target_size=(224, 224),

        batch_size=16,

        class_mode='binary',

        shuffle=False)
    res = model.predict(test_generator)
    return res



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Table = QtWidgets.QTableWidget()
    One = QtWidgets.QDialog()
    label = QLabel()
    ui =  Ui_Menu()
    ui.setupUi(Dialog)
    twoUi = Ui_two()
    twoUi.setupUi(Table)
    oneUi = Ui_one()
    oneUi.setupUi(label)
    Dialog.show()

    def two():
        fname = QFileDialog.getExistingDirectory(Dialog, 'Open file', '/home')
        text = os.listdir(path=fname+ '/test_dir')
        Table.setColumnCount(2)
        Table.setWindowTitle('Результат')
        Table.setRowCount(len(text))
        Table.setMinimumSize(QSize(500, 500))
        Table.setHorizontalHeaderLabels(["Изображение", "Диагноз"])
        Table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        Table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        res = predict(fname)


        for i in range(len(res)):
            if res[i][0] > 0.9:
                t = "Результат: положительный"
            else:
                t = "Результат: отрицательный"
            Table.setItem(i, 1, QTableWidgetItem(str(t)))
            Table.setItem(i, 0, QTableWidgetItem(str(text[i])))
            if res[i][0] > 0.9:
                Table.item(i, 0).setBackground(QtGui.QColor(255,0,0))
                Table.item(i, 1).setBackground(QtGui.QColor(255,0,0))
            else:
                Table.item(i, 0).setBackground(QtGui.QColor(0,255,0))
                Table.item(i, 1).setBackground(QtGui.QColor(0,255,0))
        Table.resizeColumnsToContents()
        Table.show()
    def one():
        fname = QFileDialog.getOpenFileName(Dialog, 'Open file', '/home')[0]
        shutil.copy(fname, "one/test/img.jpeg")
        img = Image.open("one/test/img.jpeg").convert("RGB")
        img = img.resize((427, 247), PIL.Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 26)
        text = predict2()
        #text = os.listdir(path="C:/Users/user/Desktop/Перевод/main/main_dir/test_dir")
        if text[0] > 0.9:
            text = "Результат: положительный"
        else:
            text = "Результат: отрицательный"
        draw.text((100, 200), str(text) ,(0,0,255),font=font)
        img.save("one/test/img.jpeg")
        label.title = 'Результат'
        label.left = 200
        label.top = 200
        label.width = 300
        label.height = 300
        label.setWindowTitle(label.title)
        label.setGeometry(label.left, label.top, label.width, label.height)
        img = Image.open("one/test/img.jpeg").convert("RGB")
        img = img.resize((700, 700), PIL.Image.ANTIALIAS)
        img.save("one/test/img.jpeg")
        pixmap = QPixmap("one/test/img.jpeg")
        

        label.label = QLabel(label)
        label.label.setPixmap(pixmap)
        label.label.resize(pixmap.width(), pixmap.height())

        label.resize(pixmap.width(), pixmap.height())
        label.show()
        os.remove("one/test/img.jpeg")


    ui.oneButton.clicked.connect(one)
    ui.twoButton.clicked.connect(two)

    sys.exit(app.exec_())

exit=str(input())
if exit=="Выйти":
    exit()    
