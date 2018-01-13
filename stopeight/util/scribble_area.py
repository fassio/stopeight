#!/usr/bin/env python

# Copyright (C) 2016 Specific Purpose Software GmbH

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from PyQt5.QtGui import QTabletEvent
from PyQt5.QtCore import QEvent

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

from stopeight.util.editor_data import ScribbleData,ScribbleBackup

class ScribbleArea(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(Qt.WA_StaticContents)
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.lastPoint = QPoint()

        self.data = ScribbleData()

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.update()

    def _input(self, x, y):
        self.data.append((x,y))

    def _press(self,event):
        self.scribbling = True
        self.lastPoint = event.pos()
        self.clearImage()
        log.info("Erasing scribble data")
        #don't assign new self.data = [], maybe self.data[:] = []
        del self.data[:]
        if (len(self.data)>0):
            raise "Data clear failed!"

    def _move(self, event):
        self.drawLineTo(event.pos())

    def _release(self, event):
        self.drawLineTo(event.pos())
        self.scribbling = False

    def tabletEvent(self, event):
        if event.type() == QEvent.TabletPress:
            self._press(event)
        elif (event.type() == QEvent.TabletMove) and self.scribbling:
            self._move(event)
            self._input(event.posF().x(),event.posF().y())            
        elif (event.type() == QEvent.TabletRelease) and self.scribbling:
            self._release(event)
            self._input(event.posF().x(),event.posF().y())
            try:
                self.tablet_id=event.uniqueId()
            except:
                self.__dict__.__delattr__('tablet_id')


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._press(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self._move(event)
            self._input(event.pos().x(),event.pos().y())            

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton) and self.scribbling:
            self._release(event)
            self._input(event.pos().x(),event.pos().y())            

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)        

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))

        painter.drawLine(self.lastPoint, endPoint)
        rad = self.myPenWidth / 2 + 2
        self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = QPoint(endPoint)

    def __call__(self, points=[], color=Qt.black):
        painter = QPainter(self.image)
        painter.setPen(QPen(color, self.myPenWidth, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))

        for n in range(len(points)-1):
            painter.drawLine(points[n][0],points[n][1],points[n+1][0],points[n+1][1])            
        self.update()    

    def _scribble(self):
        self.clearImage()
        #for d,c in self.data,self.colors:
            #self.scribble.plot(d,c)
        self(ScribbleBackup(),Qt.red)
        self(ScribbleData(),Qt.blue)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage

    def print_(self):
        printer = QPrinter(QPrinter.HighResolution)

        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
            painter.end()

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

#    def penColor(self):
#        newColor = QColorDialog.getColor(self.penColor())
#        if newColor.isValid():
#            self.setPenColor(newColor)

#    def penWidth(self):
#        newWidth, ok = QInputDialog.getInt(self, "Scribble",
#                "Select pen width:", self.penWidth(), 1, 50, 1)
#        if ok:
#            self.setPenWidth(newWidth)

