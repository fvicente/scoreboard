#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os, re, sys, string, math, time, datetime
try:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import QTextCursor
    pyside = False
except:
    from PySide import QtCore, QtGui
    from PySide.QtGui import QTextCursor
    pyside = True
from debugavr_ui import Ui_MainWindow, Ui_MemoryManagerDialog, Ui_AddMemoryDialog, Ui_ChangeValueDialog, Ui_InputDialog
from cStringIO import StringIO
from lntextedit import LNTextEdit
from avr import AVR

import codecs

#psyco.cannotcompile(re.compile)
try:
    import psyco
    psyco.full()
except:
    pass

printable = "".join(["%c"%(i if "%c"%i in string.printable and i not in (8, 9, 10, 11, 12, 13) else ord(".")) for i in range(256)])

# program options
options = {}

# dictionary with strings
strings = {}

# binary program
memblocks = []

# breakpoints
brkpt = []

# one time breakpoints
ot_brkpt = []

# debug breakpoints for cycle measure 
dbg_brkpt = []

# current 'list' index when debugging
current_inst = -1

def load_strings(file):
    global strings
    if not os.path.isfile(file):
        return
    print "Reading program strings from %s..."%file
    fin = open(file, "r")
    for line in fin.readlines():
        strings[line[0:8]] = line[9:]
    fin.close()
    print "Reading strings done done."

def print_usage():
    print "Usage:\n\t./debugavr.py [asm_name]\n\n"

class MemoryManager(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_MemoryManagerDialog()
        self.ui.setupUi(self)
        self.fill_list()
        if pyside:
            # signal new style
            self.ui.removeButton.clicked.connect(self.on_removeButton_clicked)
            self.ui.saveButton.clicked.connect(self.on_saveButton_clicked)
            self.ui.addButton.clicked.connect(self.on_addButton_clicked)

    def fill_list(self):
        list = self.ui.memoryList
        list.setRowCount(0)
        list.setRowCount(len(memblocks))
        for row, memblock in enumerate(memblocks):
            list.setItem(row, 0, QtGui.QTableWidgetItem("0x%.8x"%memblock['addr']))
            list.setItem(row, 1, QtGui.QTableWidgetItem("0x%.8x"%(memblock['addr']+len(memblock['mem']))))
            list.setItem(row, 2, QtGui.QTableWidgetItem("%d"%len(memblock['mem'])))

    def on_removeButton_clicked(self, checked=None):
        if not pyside and checked is None: return
        list = self.ui.memoryList
        if list.selectedIndexes():
            index = list.selectedIndexes()[0].row()
            for i, memblock in enumerate(memblocks):
                if i == index:
                    if QtGui.QMessageBox.question(self, "Remove memory block", "Confirm delete block on address 0x%.8x"%memblock['addr'], QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                        memblocks.remove(memblock)
                        self.fill_list()
                        break
        else:
            QtGui.QMessageBox.critical(self, 'Error', "Select the block to delete")

    def on_saveButton_clicked(self, checked=None):
        if not pyside and checked is None: return
        timestamp = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
        for i, memblock in enumerate(memblocks):
            filename = "mem_0x%.8x_to_0x%.8x_block_%d_%s.bin"%(memblock['addr'], memblock['addr'] + len(memblock['mem']), i, timestamp)
            with open(filename, "w+") as f:
                #for ch in memblock['mem']:
                f.write("%s"%memblock['mem'])
        if i > 0:
            QtGui.QMessageBox.information(self, 'Save', "Memory saved, see file(s) mem*_%s.bin"%timestamp)

    def on_addButton_clicked(self, checked=None):
        if not pyside and checked is None: return
        dlg = QtGui.QDialog()
        input = Ui_AddMemoryDialog()
        input.setupUi(dlg)
        if dlg.exec_() == 1:
            try:
                addr = str(input.lineEditAddress.text().trimmed())
                size = str(input.lineEditSize.text().trimmed())
                valaddr = int(addr, 0)
                valsize = int(size, 0)
                if addr == "" or addr is None or valaddr > 0xffffffff:
                    QtGui.QMessageBox.critical(self, 'Error', "Invalid address (must be an integer between 0x0 and 0xFFFFFFFF)")
                    return
                if size == "" or size is None or valsize <= 0 or valsize > 0xffffffff:
                    QtGui.QMessageBox.critical(self, 'Error', "Invalid size (must be an integer between 0x0 and 0xFFFFFFFF)")
                    return
                mem = bytearray()
                mem.extend('\0'*valsize)
                memblocks.append({ 'mem': mem, 'addr': valaddr, 'len': valsize })
                self.fill_list()
            except:
                QtGui.QMessageBox.critical(self, 'Error', "Invalid address or size")
                return

class MainForm(QtGui.QMainWindow):

    def __init__(self, parent=None, app=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEditCode = LNTextEdit(self.set_breakpoint, self.ui.splitterHorizontal)
        font = QtGui.QFont()
        font.setFamily("Andale Mono")
        font.setPointSize(10)
        edit = self.ui.textEditCode.edit
        edit.setFont(font)
        edit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        edit.setReadOnly(True)
        edit.setObjectName("textEditCode")                                                        
        self.ui.textEditCode.number_bar.setFont(font)
        self.avr = AVR(memblocks, None) # self.mem_block_changed
        # debug modes
        self.DM_TERMINATED = 0
        self.DM_RUNNING = 1
        self.DM_PAUSED = 2
        self.debug_mode = self.DM_TERMINATED
        self.pause_asap = False
        self.reset()
        if pyside:
            # signal new style
            self.ui.actionStart.triggered.connect(self.on_actionStart_triggered)
            self.ui.actionMemoryManager.triggered.connect(self.on_actionMemoryManager_triggered)
            self.ui.actionChangeRegisterValue.triggered.connect(self.on_actionChangeRegisterValue_triggered)
            self.ui.actionSetStartAddress.triggered.connect(self.on_actionSetStartAddress_triggered)
            self.ui.actionTerminate.triggered.connect(self.on_actionTerminate_triggered)
            self.ui.actionPause.triggered.connect(self.on_actionPause_triggered)
            self.ui.actionStepInto.triggered.connect(self.on_actionStepInto_triggered)

    def set_breakpoint(self, lineno, state):
        """
        Add or remove breakpoint for given line
        @param  lineno  line number for the breakpoint
        @param  state   0: remove breakpoint, 1: add breakpoint
        @return: True if the breakpoint to Add is in a valid line
        """
        found = False
        for line in self.avr.list:
            if line['line'] == lineno:
                found = True
                break
            if line['line'] > lineno:
                break
        if found:
            if state == 0:
                brkpt.remove(lineno)
            elif state == 1:
                brkpt.append(lineno)
        return found

    def enable_debug_buttons(self):
        if self.debug_mode is self.DM_RUNNING:
            enable = play = False
            pause = True
        elif self.debug_mode is self.DM_PAUSED:
            enable = play = True
            pause = False
        else:
            # default terminated
            enable = pause = False
            play = True
        self.ui.actionStart.setEnabled(play)
        self.ui.actionPause.setEnabled(pause)
        self.ui.actionTerminate.setEnabled(enable)
        self.ui.actionStepInto.setEnabled(enable)
        self.ui.actionStepOver.setEnabled(enable)
        self.ui.actionStepReturn.setEnabled(enable)
        self.ui.actionChangeRegisterValue.setEnabled(enable)

    def set_current_line(self, line):
        """Sets the cursor and 'current instruction' arrow icon to the given line in the text editor"""
        # move the cursor to the beginning of the specified line
        edit = self.ui.textEditCode.edit
        cursor = edit.textCursor()
        cursor.setPosition(edit.document().findBlockByLineNumber(line).position() - 1)
        cursor.movePosition(QTextCursor.StartOfLine)
        edit.setTextCursor(cursor)
        # set the icon
        self.ui.textEditCode.setCurrentInstruction(line)

    def set_next_addr(self, next_addr, animate=False):
        global current_inst
        # move to following instruction
        if next_addr == -1:
            # have to move to the next instruction
            if current_inst + 1 >= len(self.avr.list):
                QtGui.QMessageBox.critical(self, 'Error', "Cannot move to next instruction. Program end.")
                return False
            current_inst += 1
        else:
            current_inst = next_addr
        if animate:
            self.set_current_line(self.avr.list[current_inst]['line'])
        return True

    def reset(self):
        self.avr.reset()

    def on_actionMemoryManager_triggered(self, checked=None):
        if not pyside and checked is None: return
        mman = MemoryManager()
        mman.exec_()

    def on_actionChangeRegisterValue_triggered(self, checked=None):
        if not pyside and checked is None: return
        dlg = QtGui.QDialog()
        chval = Ui_ChangeValueDialog()
        chval.setupUi(dlg)
        for key in sorted(self.avr.r.keys()):
            chval.comboBoxRegister.addItem(key)
        if dlg.exec_() == 1:
            try:
                value = "%s"%chval.lineEditValue.text().trimmed()
                valint = int(value, 0)
                if value == "" or value is None or valint > 0xffffffff:
                    QtGui.QMessageBox.critical(self, 'Error', "Invalid value (must be an integer between -2,147,483,648 and +2,147,483,647)")
                    return
                self.avr.r["%s"%chval.comboBoxRegister.currentText()] = valint
                self.update_reg_view()
            except:
                QtGui.QMessageBox.critical(self, 'Error', "Invalid value (must be an integer between -2,147,483,648 and +2,147,483,647)")
                return

    def on_actionSetStartAddress_triggered(self, checked=None):
        if not pyside and checked is None: return
        dlg = QtGui.QDialog()
        input = Ui_InputDialog()
        input.setupUi(dlg)
        input.labelField.setText("Start Address")
        input.labelInfo.setText("Select the start address for the program")
        input.lineEditField.setText("0x%.8x"%options['start'])
        if dlg.exec_() == 1:
            try:
                value = str(input.lineEditField.text().trimmed())
                valint = int(value, 0)
                if value == "" or value is None or valint > 0xffffffff:
                    QtGui.QMessageBox.critical(self, 'Error', "Invalid start address (must be an integer between 0x0 and 0xFFFFFFFF)")
                    return
                options['start'] = valint
            except:
                QtGui.QMessageBox.critical(self, 'Error', "Invalid start address (must be an integer between 0x0 and 0xFFFFFFFF)")
                return

    def on_actionTerminate_triggered(self, checked=None):
        if not pyside and checked is None: return
        self.debug_mode = self.DM_TERMINATED
        self.enable_debug_buttons()
        self.ui.textEditCode.setCurrentInstruction(None)
        global current_inst
        current_inst = -1
        self.reset()
        self.update_reg_view()

    def start_program(self, checked=None, animate=False):
        if not pyside and checked is None: return
        global current_inst
        list = self.avr.list
        if self.debug_mode == self.DM_TERMINATED:
            self.reg_prev = self.avr.r.copy()
            self.f_prev = self.avr.f.copy()
            self.cycles_prev = 0
            current_inst = 0
            start = options['start']
            ot_brkpt.append(list[0]['line'])
        # run/resume the program
        self.debug_mode = self.DM_RUNNING
        self.enable_debug_buttons()
        self.pause_asap = False
        self.ui.textEditCode.setCurrentInstruction(None)
        first = True
        print "Start: %s"%datetime.datetime.now()
        i = 0
        # TODO: scoreboard debug only
        testcase = { 'bp': [299, 210], 'exp': 19 } # front porch
        testcase = { 'bp': [324, 299], 'exp': 74 } # hsync pulse
        testcase = { 'bp': [353, 324], 'exp': 38 } # back porch
        testcase = { 'bp': [210, 353], 'exp': 503 } # line painting
        testcase = { 'bp': [], 'exp': 0 } # nothing
        dbg_brkpt = testcase['bp']
        dbg_first = True
        while not self.pause_asap:
            # backup registers and flags
#            self.reg_prev = self.avr.r.copy()
#            self.f_prev = self.avr.f.copy()
            # check one-time breakpoints
            line = list[current_inst]['line']
            if line in ot_brkpt:
                ot_brkpt.remove(line)
                break
            # check regular breakpoints
            if not first and line in brkpt:
                print "Breakpoint: %s"%datetime.datetime.now()
                break
            if line in dbg_brkpt:
                d = self.avr.cycles - self.cycles_prev
                if not dbg_first and dbg_brkpt[0] == line:
                    print "Diff Cycles: %d [ @20MHz = %.2fus ] Line: %d<br>"%(d, d * 0.05, line)
                    if d != testcase['exp']:
                        break
                dbg_first = False
                self.cycles_prev = self.avr.cycles
            first = False
            # execute assembly line
            err, next_addr = self.avr.execute_asm_line(current_inst)
            if err is not None:
                # show message and break on error
                QtGui.QMessageBox.critical(self, 'Error', err)
                break
            if not self.set_next_addr(next_addr, animate):
                break
            if animate:
                self.update_reg_view()
            if i > 100:
                # process GUI events
                self.app.processEvents()
                i = 0
            i += 1
        # program paused
        self.update_reg_view()
        self.set_current_line(list[current_inst]['line'])
        self.debug_mode = self.DM_PAUSED
        self.enable_debug_buttons()

    def on_actionStart_triggered(self, checked=None):
        #global GLOBAL
        #GLOBAL = self
        #import cProfile
        #cProfile.run("GLOBAL.start_program(%r,%r)"%(checked, animate))
        self.start_program(checked, False)

    def on_actionPause_triggered(self, checked=None):
        if not pyside and checked is None: return
        if self.debug_mode == self.DM_RUNNING:
            self.pause_asap = True

    def update_reg_view(self):
        edit = self.ui.plainTextEditRegisters
        # list of registers in the order they should appear on screen
        regs = ('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12',
                'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'r22', 'r23', 'r24', 'r25',
                'r26', 'r27', 'r28', 'r29', 'r30', 'r31')
        lines = len(regs) / 2
        html = ""
        strs = ""
        for i in range(lines):
            reg1 = regs[i]
            reg2 = regs[i+lines] if i+lines < len(regs) else None
            for reg in (reg1, reg2):
                if reg == None: continue
                end = 5*"&nbsp;" if reg == reg1 else "<br>"
                color = "red" if self.reg_prev[reg] != self.avr.r[reg] else "black"
                spaces = (9-len(reg))*"&nbsp;"
                html += "<font color='%s'>%s:%s0x%.8x</color>%s"%(color, reg, spaces, self.avr.r[reg] or 0, end)
        # strings
        for reg in regs:
            # find the memory block
            addr = self.avr.r[reg]
            value = ""
            for i, memblock in enumerate(memblocks):
                if addr >= memblock['addr'] and addr <= memblock['addr'] + len(memblock['mem']):
                    addr -= memblock['addr']
                    endaddr = addr
                    while endaddr < len(memblock['mem']):
                        if memblock['mem'][endaddr] == 0:
                            break
                        endaddr += 1
                    value = "%s"%str(memblock['mem'][addr:endaddr])
            if value == "" and addr < 256:
                value = "'%c'"%(addr & 0xFF, ) if addr else "NULL"
            #value = strings.get("%.8x"%self.avr.r[key]) or ""
            strs += "%s: %s<br>"%(reg, value, )

        html += "<br><br>"
        strs += "<br><br>"
        flags = ('Z', 'N', 'C', 'V')
        for flag in flags:
            color = "red" if self.f_prev[flag] != self.avr.f[flag] else "black"
            html += "<font color='%s'>%s: %s</color>&nbsp;&nbsp;"%(color, flag, self.avr.f[flag])
        html += "<br>"
        html += "Cycles: %d<br>"%(self.avr.cycles)
        d = self.avr.cycles - self.cycles_prev
        html += "Diff Cycles: %d [ @20MHz = %.2fus ]"%(d, d * 0.05)
        html += "<br>"
        edit.clear()
        edit.appendHtml(html)
        self.cycles_prev = self.avr.cycles
        self.ui.plainTextEditStrings.clear()
        self.ui.plainTextEditStrings.appendHtml(strs)

    def mem_block_changed(self, index, pos, size):
        if index != 3: return
        edit = self.ui.plainTextEditMemory
        cursor = edit.textCursor()
        cursor.beginEditBlock()
        for i in range(size):
            offset = pos + i
            lines = math.trunc(offset / 32)
            line_offset = offset % 32
            # each line has 10 + (3 * 32) + 32 + 1 = 139
            cursor.setPosition((lines * 139) + 10 + (line_offset * 3))
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 2)
            cursor.removeSelectedText()
            cursor.insertText("%.2x"%(memblocks[index]['mem'][offset] & 0xFF))
            # now replace the 'readable' part
            cursor.setPosition((lines * 139) + 106 + line_offset)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
            cursor.removeSelectedText()
            cursor.insertText("%s"%(memblocks[index]['mem'][offset:offset + 1].translate(printable)))
        cursor.endEditBlock()

    def on_actionStepInto_triggered(self, checked=None):
        if not pyside and checked is None: return
        global current_inst
        if current_inst < 0 or current_inst >= len(self.avr.list):
            return
        self.reg_prev = self.avr.r.copy()
        self.f_prev = self.avr.f.copy()
        err, next_addr = self.avr.execute_asm_line(current_inst)
        if err is not None:
            QtGui.QMessageBox.critical(self, 'Error', err)
            return
        # update registers view
        self.update_reg_view()
        if next_addr is None:
            return
        self.set_next_addr(next_addr, True)

def load_file_to_mem(file, addr):
    """
    Load binary file and put it in a memory block
    """
    with open(file, 'rb') as fin:
        # first block of memory is displayed in the Memory view panel
        if len(memblocks) == 3:
            data = StringIO()
            pos = addr
            while True:
                bytes = fin.read(32)
                read = len(bytes)
                if not bytes or read == 0:
                    break
                data.write("%.8x: "%(pos, ))
                for i in range(read):
                    data.write("%.2x "%ord(bytes[i]))
                if read < 32:
                    data.write("   "*(32-read))
                data.write("%s\n"%(bytes.translate(printable), ))
                pos += 32
            mainapp.ui.plainTextEditMemory.setPlainText(data.getvalue())
            data.close()
        fin.seek(0, os.SEEK_SET)
        mem = bytearray()
        mem.extend(fin.read())
        memblocks.append({ 'mem': mem, 'addr': addr, 'len': len(mem) })

def add_empty_mem(addr, size):
    mem = bytearray()
    mem.extend('\0'*size)
    memblocks.append({ 'mem': mem, 'addr': addr, 'len': size })

def copy_mem_block(memfrom, memto, size):
    """
    Copy a memory block to another
    """
    for memblock in memblocks:
        if memfrom >= memblock['addr'] and memfrom <= memblock['addr'] + len(memblock['mem']):
            memfrom -= memblock['addr']
            # find the destination
            for memblockdest in memblocks:
                if memto >= memblockdest['addr'] and memto <= memblockdest['addr'] + len(memblockdest['mem']):
                    memto -= memblockdest['addr']
                    for i in range(size):
                        memblockdest['mem'][memto+i] = memblock['mem'][memfrom+i]
                    break
            break

def main():
    global mainapp
    # read options from arguments
    options['filename'] = "../src/main.S"
    options['start'] = 0
    arglen = len(sys.argv)
    if arglen > 1: options['filename'] = sys.argv[1]
    if arglen > 2: options['start'] = int(sys.argv[2], 0)
    # check if the file exists
    if not os.path.isfile(options['filename']):
        print "File %s not found!\n"%options['filename']
        print_usage()
        exit(0)
    # instantiate and show the GUI
    app = QtGui.QApplication(sys.argv)
    mainapp = MainForm(None, app)
    # assembly listing
    print "Appending lines to editor..."
    with codecs.open(options['filename'], "r", "utf-8") as fin:
        mainapp.ui.textEditCode.edit.setPlainText(fin.read())
        fin.seek(0, os.SEEK_SET)
        cnt = 1
        for line in fin.readlines():
            mainapp.avr.parse_asm_line(line, cnt)
            cnt += 1
    # TODO: make this generic
    print "Appending other files..."
    with codecs.open("../src/const.S", "r", "utf-8") as fin:
        for line in fin.readlines():
            mainapp.avr.parse_asm_line(line, cnt)
            cnt += 1
    # memory window
    print "Appending memory lines..."
    add_empty_mem(0x00300000, 0x100000)
    add_empty_mem(0x00f00000, 0xfffff) # stack
    print "Appending done."
    # main application
    mainapp.show()
    mainapp.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
