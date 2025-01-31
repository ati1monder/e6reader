#############################################################################
#
# This file taken from
# https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/layouts/flowlayout/flowlayout.cpp?h=5.13
# Modified/adapted by jon, 10/07/2019, to translate into Python/PyQt
# Modified/adapted by atimonder1, 09/07/2024, to make widgets centered
#
# Copyright (C) 2016 The Qt Company Ltd.
# Contact: https://www.qt.io/licensing/
#
# This file is part of the examples of the Qt Toolkit.
#
# $QT_BEGIN_LICENSE:BSD$
# Commercial License Usage
# Licensees holding valid commercial Qt licenses may use this file in
# accordance with the commercial license agreement provided with the
# Software or, alternatively, in accordance with the terms contained in
# a written agreement between you and The Qt Company. For licensing terms
# and conditions see https://www.qt.io/terms-conditions. For further
# information use the contact form at https://www.qt.io/contact-us.
#
# BSD License Usage
# Alternatively, you may use this file under the terms of the BSD license
# as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of The Qt Company Ltd nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
#
# $QT_END_LICENSE$
#
#############################################################################

import typing

from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtWidgets import QWidget, QLayout, QLayoutItem, QStyle, QSizePolicy


class FlowLayout(QLayout):
    def __init__(self, parent: QWidget=None, margin: int=-1, hSpacing: int=-1, vSpacing: int=-1):
        super().__init__(parent)

        self.itemList = list()
        self.m_hSpace = hSpacing
        self.m_vSpace = vSpacing
        self.items = list()

        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        # copied for consistency, not sure this is needed or ever called
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        self.itemList.append(item)

    def horizontalSpacing(self) -> int:
        if self.m_hSpace >= 0:
            return self.m_hSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def clearlayout(self):
        for i in reversed(range(self.count())):
            widget = self.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def verticalSpacing(self) -> int:
        if self.m_vSpace >= 0:
            return self.m_vSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def count(self) -> int:
        return len(self.itemList)

    def itemAt(self, index: int) -> typing.Union[QLayoutItem, None]:
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        else:
            return None
        
    def itemAppend(self, item):
        self.items.append(item)
    
    def inLayout(self, object) -> bool:
        if object in self.items:
            return True
        else:
            return False

    def takeAt(self, index: int) -> typing.Union[QLayoutItem, None]:
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        else:
            return None

    def expandingDirections(self) -> Qt.Orientations:
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def smartSpacing(self, pm: QStyle.PixelMetric) -> int:
        parent = self.parent()
        if not parent:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()

    def doLayout(self, rect: QRect, testOnly: bool) -> int:
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0
        rowItems = []
        rowWidth = 0

        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for item in self.itemList:
            wid = item.widget()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                totalRowWidth = rowWidth - spaceX
                offset = (effectiveRect.width() - totalRowWidth) / 2
                for rowItem in rowItems:
                    rowItem[1].moveLeft(rowItem[1].left() + offset)
                    if not testOnly:
                        rowItem[0].setGeometry(rowItem[1])
                rowItems.clear()
                rowWidth = 0

                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            rectItem = QRect(QPoint(x, y), item.sizeHint())
            rowItems.append((item, rectItem))
            rowWidth += item.sizeHint().width() + spaceX

            if not testOnly:
                item.setGeometry(rectItem)

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        totalRowWidth = rowWidth - spaceX
        offset = (effectiveRect.width() - totalRowWidth) / 2
        for rowItem in rowItems:
            rowItem[1].moveLeft(rowItem[1].left() + offset)
            if not testOnly:
                rowItem[0].setGeometry(rowItem[1])

        return y + lineHeight - rect.y() + bottom
