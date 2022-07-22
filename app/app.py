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
        self.resize(960, 680)

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
        flashCount = self.flashConut
        color = QColor(items['hex'])
        rect = QRect(0, 0, width, height)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawRect(rect)

        polygon = QPolygonF()
        polygon.append(QPointF(width -  width * shadow / flashCount, 0))
        polygon.append(QPointF(width, height * shadow / flashCount))
        polygon.append(QPointF(width, 0))

        polygon2 = QPolygonF()
        polygon2.append(QPointF(0, height - height * shadow / flashCount))
        polygon2.append(QPointF(width * shadow / flashCount, height))
        polygon2.append(QPointF(0, height))

        paintPath = QPainterPath()
        paintPath.addPolygon(polygon)
        paintPath.addPolygon(polygon2)
        paintPath.closeSubpath()

        color2 = QColor("#ffffff")
        color2.setRed(min(color.red() + 30, 255))
        color2.setGreen(min(color.green() + 30, 255))
        color2.setBlue(min(color.blue() + 30, 255))

        radialGradient = QLinearGradient(0, height, width, 0)
        radialGradient.setColorAt(0, color2)
        radialGradient.setColorAt(0.3, color)
        radialGradient.setColorAt(0.6, color)
        radialGradient.setColorAt(1, color2)
        # painter.setBrush(QBrush(radialGradient))
        # painter.drawPath(paintPath)

        cOffset = float(255 * shadow / flashCount)
        cTmep = color.red() + color.green() + color.blue()
        if  cTmep > 360:
            color2.setRed(max(color.red() - cOffset, 0))
            color2.setGreen(max(color.green() - cOffset, 0))
            color2.setBlue(max(color.blue() - cOffset, 0))
        else:
            color2.setRed(min(color.red() + cOffset, 255))
            color2.setGreen(min(color.green() + cOffset, 255))
            color2.setBlue(min(color.blue() + cOffset, 255))
        
        offset = width / 20
        rect.adjust(offset, offset, -offset, -offset)

        header = 'R' + str(color.red()) + ' G' + str(color.green()) + ' B' + str(color.blue())
        painter.setPen(QPen(color2))
        painter.setFont(QFont('仿宋', 14))
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, header)

        footer = ''
        if items['book'].__len__() > 0:
            footer += '《' + items['book'] + '》'
        if items['author'].__len__() > 0:
            footer += ' -- ' + items['author']
        if items['describe'].__len__() > 0:
            footer += '\n' + items['describe']
        painter.setPen(QPen(color2))
        painter.setFont(QFont('仿宋', 14))
        painter.drawText(rect, Qt.AlignRight | Qt.AlignBottom, footer)

        rect.adjust(offset, offset, 0, -offset)
        painter.setPen(QPen(color2))
        painter.setFont(QFont('仿宋', 60))
        painter.drawText(rect, Qt.AlignRight | Qt.AlignBottom, items['name'])

        super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ColorWidget()
    w.start()
    w.show()
    sys.exit(app.exec_())