'''
Text widget with support for line numbers
'''

try:
    from PyQt4.QtGui import QFrame, QHBoxLayout, QPainter, QPlainTextEdit, QTextEdit
    from PyQt4.QtGui import QTextFormat, QWidget, QImage
    from PyQt4.QtCore import QRect, QPoint, QVariant, Qt
except:
    from PySide.QtGui import *
    from PySide.QtGui import *
    from PySide.QtCore import *

import debugavr_rc

class LNTextEdit(QFrame):

    class NumberBar(QWidget):

        def __init__(self, edit):
            QWidget.__init__(self, edit)

            self.edit = edit
            self.adjustWidth(1)

        def paintEvent(self, event):
            self.edit.numberbarPaint(self, event)
            QWidget.paintEvent(self, event)

        def adjustWidth(self, count):
            width = self.fontMetrics().width(unicode(count)) + 16
            if self.width() != width:
                self.setFixedWidth(width)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                # It would be nice to do
                # self.update(0, rect.y(), self.width(), rect.height())
                # But we can't because it will not remove the bold on the
                # current line if word wrap is enabled and a new block is
                # selected.
                self.update()

        def mouseDoubleClickEvent(self, ev):
            # Set the cursor to current line
            edit = self.edit
            edit.setCursor(ev.y() + 1)
            edit.toggleBreakpoint(edit.document().findBlock(edit.textCursor().position()).blockNumber() + 1)
            self.update()

    class PlainTextEdit(QPlainTextEdit):

        def __init__(self, *args):
            QPlainTextEdit.__init__(self, *args)
            self.instPtrImage = QImage(":/images/icons/enabled/inst_ptr_top.gif")
            self.brkpObjImage = QImage(":/images/icons/enabled/brkp_obj.gif")
            self.breakpoints = set()

            #self.setFrameStyle(QFrame.NoFrame)

            self.setFrameStyle(QFrame.NoFrame)
            self.highlight()
            #self.setLineWrapMode(QPlainTextEdit.NoWrap)

            self.cursorPositionChanged.connect(self.highlight)

        def highlight(self):
            hi_selection = QTextEdit.ExtraSelection()

            hi_selection.format.setBackground(self.palette().alternateBase())
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()

            self.setExtraSelections([hi_selection])

        def setCursor(self, y):
            self.setTextCursor(self.cursorForPosition(QPoint(0, y)))

        def toggleBreakpoint(self, line):
            if line in self.breakpoints:
                self.breakpoints.remove(line)
                self.brkp_callback(line, 0)
            else:
                if self.brkp_callback(line, 1):
                    self.breakpoints.add(line)

        def numberbarPaint(self, number_bar, event):
            font_metrics = self.fontMetrics()
            current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1

            block = self.firstVisibleBlock()
            line_count = block.blockNumber()
            painter = QPainter(number_bar)
            painter.fillRect(event.rect(), self.palette().base())

            # Iterate over all visible text blocks in the document.
            while block.isValid():
                line_count += 1
                block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

                # Check if the position of the block is out side of the visible
                # area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break

                # We want the line number for the selected line to be bold.
                if line_count == current_line:
                    font = painter.font()
                    font.setBold(True)
                    painter.setPen(Qt.black)
                    painter.setFont(font)
                else:
                    font = painter.font()
                    font.setBold(False)
                    painter.setPen(Qt.darkGray)
                    painter.setFont(font)

                if self.instLine is not None and line_count == self.instLine:
                    painter.drawImage(QRect(0, block_top, 16, 16), self.instPtrImage)

                if line_count in self.breakpoints:
                    painter.drawImage(QRect(0, block_top, 16, 16), self.brkpObjImage)

                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
                painter.drawText(paint_rect, Qt.AlignRight, unicode(line_count))

                block = block.next()

            painter.end()

    def __init__(self, brkp_callback, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.edit = self.PlainTextEdit()
        self.edit.brkp_callback = brkp_callback
        self.edit.instLine = None

        self.number_bar = self.NumberBar(self.edit)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        #hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)

    def getText(self):
        return unicode(self.edit.toPlainText())

    def setText(self, text):
        self.edit.setPlainText(text)

    def isModified(self):
        return self.edit.document().isModified()

    def setModified(self, modified):
        self.edit.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.edit.setLineWrapMode(mode)

    def setCurrentInstruction(self, line):
        self.edit.instLine = line
        self.number_bar.update()

    def setBreakpoints(self, brkp):
        self.breakpoints = brkp
        self.number_bar.update()
