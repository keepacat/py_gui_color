#!/usr/bin/env python3
#coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import resource
import sys

class ColorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWidget()
        self.path = sys.argv[0]
        self.colors = []
        self.mpos = QPoint()
        self.mouse = QPoint()

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.index = 0
        self.shadow = 0
        self.flash = 16
        self.flashTime = 0
        self.flashConut = 200

    def initWidget(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(':/logo.ico'))
        self.setWindowTitle('Color')
        self.resize(1280, 800)

    def start(self):
        file = QFile(':/color_utf8.txt')
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            fileWord = file.readAll().data()
            fileData = fileWord.decode(encoding="utf-8", errors="ignore")
            itmes = fileData.split('\n\n')
            for item in itmes:
                tmps = item.split('\n')
                colors = {}
                for tmp in tmps:
                    t = tmp.split(':')
                    if t.__len__() == 2:
                        colors[t[0]] = t[1]
                if colors.__len__() > 0:
                    self.colors.append(colors)
            file.close()

        rect = QRectF(0, 0, self.width(), self.height())
        painterPath = QPainterPath()
        painterPath.addRoundedRect(rect, 10, 10)
        polygon = painterPath.toFillPolygon().toPolygon()
        self.setMask(QRegion(polygon))

        self.timer.start(self.flash)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.mpos = self.pos()
        self.mouse = event.globalPos()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos = self.mpos + event.globalPos() - self.mouse
        self.move(pos)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_Space:
            if self.timer.isActive() :
                self.timer.stop()
            else:
                self.timer.start()
        elif event.key() == Qt.Key_Left:
            self.index -= 1
            if 0 > self.index :
                self.index = self.colors.__len__() - 1
            self.repaint()
        elif event.key() == Qt.Key_Right:
            self.index += 1
            if self.colors.__len__() == self.index :
                self.index = 0
            self.repaint()

    def getColor(self, index):
        if index < 0:
            return QColor('ffffff')
        elif self.colors.__len__() > index:
            return QColor(self.colors[index]['hex'])
        else:
            index2 = index - self.colors.__len__()
            return self.getColor(index2)


    def onTimer(self):
        self.flashTime += 1
        if self.flashTime > self.flashConut:
            self.flashTime = 0
            self.shadow = 0
            self.index += 1
            if self.colors.__len__() == self.index :
                self.index = 0
        else:
            self.shadow += 1
        self.repaint()

    def paintEvent(self, event):
        if self.colors.__len__() <= self.index:
            return
        items = self.colors[self.index]
        width = self.width()
        height = self.height()
        shadow = self.shadow
        spring = 10
        radius = 10
        flashCount = self.flashConut
        color = self.getColor(self.index)
        color2 = self.getColor(self.index + 1)
        color3 = QColor('#ffffff')
        color4 = QColor('#eeeeee')
        rect = QRectF(0, 0, width, height)
        rectGroud = QRectF(0, 0, width, height)
        rectColor = QRectF(0, 0, width, height)
        rectColor2 = QRectF(0, 0, width, height)
        rectColor3 = QRectF(0, 0, width, height)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        
        painter.setBrush(QBrush(color3))
        painter.drawRect(rect)
        
        rectGroud.adjust(width / 10, 0, 0, 0)
        painter.setBrush(QBrush(color4))
        painter.drawRoundedRect(rectGroud, radius, radius)

        rectColor.adjust(width / 10, 0, -width * 2 / 10, -height / 5)
        rectColor.adjust(spring, spring, -spring, -spring)
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(rectColor, radius, radius)

        rectColor2.adjust(width * 8 / 10, 0, 0, -height / 5)
        rectColor2.adjust(0, spring, -spring, -spring)
        painter.setBrush(QBrush(color3))
        painter.drawRoundedRect(rectColor2, radius, radius)

        rectColor3.adjust(width / 10, height * 4 / 5, 0, 0)
        rectColor3.adjust(spring, 0, -spring, -spring)
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(rectColor3, radius, radius)

        #header
        recthead = QRectF(0, 0, width / 10, height)
        recthead.adjust(spring, spring, -spring, -spring)
        recthead.setHeight(recthead.width())
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(recthead, radius, radius)

        recthead.adjust(0, recthead.height() + spring, 0, recthead.height() + spring)
        painter.setBrush(QBrush(color2))
        painter.drawRoundedRect(recthead, radius, radius)

        recthead.adjust(0, recthead.height() + spring, 0, recthead.height() + spring)
        painter.setBrush(QBrush(self.getColor(self.index + 2)))
        painter.drawRoundedRect(recthead, radius, radius)

        recthead.adjust(0, recthead.height() + spring, 0, recthead.height() + spring)
        painter.setBrush(QBrush(self.getColor(self.index + 3)))
        painter.drawRoundedRect(recthead, radius, radius)

        recthead.adjust(0, recthead.height() + spring, 0, recthead.height() + spring)
        painter.setBrush(QBrush(self.getColor(self.index + 4)))
        painter.drawRoundedRect(recthead, radius, radius)

        recthead.adjust(0, recthead.height() + spring, 0, recthead.height() + spring)
        painter.setBrush(QBrush(self.getColor(self.index + 5)))
        painter.drawRoundedRect(recthead, radius, radius)

        #color3
        lOffset = (1 - float(shadow / flashCount)) * rectColor3.width()
        rectColor3.adjust(lOffset, 0, 0, 0)
        painter.setBrush(QBrush(color2))
        painter.drawRoundedRect(rectColor3, radius, radius)

        #color2
        radialGradient = QLinearGradient(rectColor2.topRight(), rectColor2.bottomLeft())
        radialGradient.setColorAt(0, color2)
        radialGradient.setColorAt(1, color)
        painter.setBrush(QBrush(radialGradient))
        painter.drawRoundedRect(rectColor2, radius, radius)

        #color1
        cOffset = int(180 * shadow / flashCount)
        cTmep = color.red() + color.green() + color.blue()
        if  cTmep > 360:
            color3.setRed(max(color.red() - cOffset, 0))
            color3.setGreen(max(color.green() - cOffset, 0))
            color3.setBlue(max(color.blue() - cOffset, 0))
        else:
            color3.setRed(min(color.red() + cOffset, 255))
            color3.setGreen(min(color.green() + cOffset, 255))
            color3.setBlue(min(color.blue() + cOffset, 255))

        painter.setPen(QPen(color3))
        painter.setFont(QFont('仿宋', 60))
        painter.drawText(rectColor, Qt.AlignCenter, items['name'])
        
        rectColor.adjust(spring, spring, -spring, -spring)
        header = 'R' + str(color.red()) + ' G' + str(color.green()) + ' B' + str(color.blue())
        painter.setPen(QPen(color3))
        painter.setFont(QFont('仿宋', 14))
        painter.drawText(rectColor, Qt.AlignLeft | Qt.AlignTop, header)

        footer = ''
        if items['book'].__len__() > 0:
            footer += '《' + items['book'] + '》'
        if items['author'].__len__() > 0:
            footer += ' -- ' + items['author']
        if items['describe'].__len__() > 0:
            footer += '\n' + items['describe']
        painter.setPen(QPen(color3))
        painter.setFont(QFont('仿宋', 14))
        painter.drawText(rectColor, Qt.AlignRight | Qt.AlignBottom, footer)

        super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ColorWidget()
    w.start()
    w.show()
    sys.exit(app.exec_())