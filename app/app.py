#!/usr/bin/env python3
#coding=utf-8
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, QPoint, QFile, QIODevice, QTextCodec, QRect, QPointF, Qt
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPainterPath, QBrush, QPen, QFont, QIcon
import sys
import os

class ColorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWidget()
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.index = 0
        self.colors = []
        self.mpos = QPoint()
        self.mouse = QPoint()

    def initWidget(self):
        self.resize(960, 680)

    def start(self):
        path = sys.argv[0]
        pathColor = path.replace('app.py', 'color_utf8.txt')
        # pathColor = os.path.dirname(sys.executable) + '\\color_utf8.txt'
        file = QFile(pathColor)
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
        self.timer.start(2000)

    def onTimer(self):
        self.index += 1
        if self.colors.__len__() == self.index :
            self.index = 0
        self.repaint()

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

    def paintEvent(self, event):
        if self.colors.__len__() <= self.index:
            return
        items = self.colors[self.index]
        width = self.width()
        height = self.height()
        color = QColor(items['hex'])
        rect = QRect(0, 0, width, height)

        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawRect(rect)

        polygon = QPolygonF()
        polygon.append(QPointF(width * 2 / 3, 0))
        polygon.append(QPointF(width, height / 3))
        polygon.append(QPointF(width, 0))

        polygon2 = QPolygonF()
        polygon2.append(QPointF(0, height * 2 / 3))
        polygon2.append(QPointF(width / 3, height))
        polygon2.append(QPointF(0, height))

        paintPath = QPainterPath()
        paintPath.addPolygon(polygon)
        paintPath.addPolygon(polygon2)
        paintPath.closeSubpath()

        color2 = QColor("#ffffff")
        color2.setRed(min(color.red() + 30, 255))
        color2.setGreen(min(color.green() + 30, 255))
        color2.setBlue(min(color.blue() + 30, 255))
        painter.setBrush(QBrush(color2))
        painter.drawPath(paintPath)

        cTmep = color.red() + color.green() + color.blue()
        if  cTmep > 360:
            color2.setRed(max(color.red() - 120, 0))
            color2.setGreen(max(color.green() - 120, 0))
            color2.setBlue(max(color.blue() - 120, 0))
        else:
            color2.setRed(min(color.red() + 120, 255))
            color2.setGreen(min(color.green() + 120, 255))
            color2.setBlue(min(color.blue() + 120, 255))
        
        painter.setPen(QPen(color2))
        font = QFont('仿宋', 80)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, items['name'])
        
        font = QFont('仿宋', 14)
        painter.setFont(font)
        rect.adjust(10, 10, -10, -10)
        header = 'R' + str(color.red()) + ' G' + str(color.green()) + ' B' + str(color.blue())
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, header)
        footer = ''
        if items['book'].__len__() > 0:
            footer += '《' + items['book'] + '》'
        if items['author'].__len__() > 0:
            footer += ' -- ' + items['author']
        if items['describe'].__len__() > 0:
            footer += '\n' + items['describe']
        painter.drawText(rect, Qt.AlignRight | Qt.AlignBottom, footer)
        super().paintEvent(event)

#main
app = QApplication(sys.argv)
codec = QTextCodec.codecForName("utf-8")
QTextCodec.setCodecForLocale(codec)

# path = sys.argv[0]
# pathIcon = path.replace('app.py', 'logo.ico')

w = ColorWidget()
w.setWindowFlags(Qt.FramelessWindowHint)
# w.setWindowIcon(QIcon(pathIcon))
w.show()
w.start()
sys.exit(app.exec_())