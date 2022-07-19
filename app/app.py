from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class ColorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWidget()
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.index = 0
        self.colors = []

    def initWidget(self):
        self.resize(960, 680)

    def start(self):
        path = sys.argv[0]
        pathColor = path.replace('app.py', 'color.txt')
        file = QFile(pathColor)
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            fileData = str(file.readAll(), encoding='utf8')
            itmes = fileData.split('\n\n')
            for item in itmes:
                colors = {}
                tmps = item.split('\n')
                for tmp in tmps:
                    t = tmp.split(':')
                    colors[t[0]] = t[1]
                self.colors.append(colors)
            file.close()
        # self.timer.start(1000)

    def onTimer(self):
        self.index += 1
        if self.colors.__len__() == self.index :
            self.index = 0
        self.repaint()

    def mousePressEvent(self, event):
        self.onTimer()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        if self.colors.__len__() <= self.index:
            return
        items = self.colors[self.index]
        width = self.width()
        height = self.height()
        painter = QPainter(self)
        brush = QBrush(QColor(items['hex']))
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 0, width, height))

        pen = QPen(QColor('#ffffff'))
        painter.setPen(pen)
        font = QFont('仿宋', 80, 3)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, width, height), Qt.AlignCenter, items['name'])
        
        font = QFont('仿宋', 20, 3)
        painter.setFont(font)
        header = str(self.index + 1) + '/' + str(self.colors.__len__()) + '\n'
        painter.drawText(QRect(0, 0, width, height), Qt.AlignLeft | Qt.AlignTop, header)
        footer = items['describe'] + '\n' + items['author'] + ' -- 《' + items['book'] + '》'
        painter.drawText(QRect(0, 0, width, height), Qt.AlignRight | Qt.AlignBottom, footer)
        super().paintEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    codec = QTextCodec.codecForName("UTF-8")
    QTextCodec.setCodecForLocale(codec)

    w = ColorWidget()
    w.show()
    w.start()
    sys.exit(app.exec_())