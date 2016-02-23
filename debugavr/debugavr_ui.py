# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/debugavr.ui'
#
# Created: Fri Aug 19 16:46:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except:
    from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 715)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitterHorizontal = QtGui.QSplitter(self.centralwidget)
        self.splitterHorizontal.setOrientation(QtCore.Qt.Horizontal)
        self.splitterHorizontal.setObjectName("splitterHorizontal")
        self.splitterVertical = QtGui.QSplitter(self.splitterHorizontal)
        self.splitterVertical.setOrientation(QtCore.Qt.Vertical)
        self.splitterVertical.setObjectName("splitterVertical")
        self.splitterRegStr = QtGui.QSplitter(self.splitterVertical)
        self.splitterRegStr.setOrientation(QtCore.Qt.Horizontal)
        self.splitterRegStr.setObjectName("splitterRegStr")
        self.plainTextEditRegisters = QtGui.QPlainTextEdit(self.splitterRegStr)
        font = QtGui.QFont()
        font.setFamily("Andale Mono")
        font.setPointSize(10)
        self.plainTextEditRegisters.setFont(font)
        self.plainTextEditRegisters.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEditRegisters.setObjectName("plainTextEditRegisters")
        self.plainTextEditStrings = QtGui.QPlainTextEdit(self.splitterRegStr)
        font = QtGui.QFont()
        font.setFamily("Andale Mono")
        font.setPointSize(10)
        self.plainTextEditStrings.setFont(font)
        self.plainTextEditStrings.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEditStrings.setObjectName("plainTextEditStrings")
        self.groupBoxMemory = QtGui.QGroupBox(self.splitterVertical)
        self.groupBoxMemory.setObjectName("groupBoxMemory")
        self.gridLayoutMemory = QtGui.QGridLayout(self.groupBoxMemory)
        #self.gridLayoutMemory.setMargin(5)
        self.gridLayoutMemory.setObjectName("gridLayoutMemory")
        self.gridLayoutMemoryBox = QtGui.QGridLayout()
        self.gridLayoutMemoryBox.setObjectName("gridLayoutMemoryBox")
        self.labelSection = QtGui.QLabel(self.groupBoxMemory)
        self.labelSection.setObjectName("labelSection")
        self.gridLayoutMemoryBox.addWidget(self.labelSection, 0, 0, 1, 1)
        self.comboBoxSection = QtGui.QComboBox(self.groupBoxMemory)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSection.sizePolicy().hasHeightForWidth())
        self.comboBoxSection.setSizePolicy(sizePolicy)
        self.comboBoxSection.setObjectName("comboBoxSection")
        self.gridLayoutMemoryBox.addWidget(self.comboBoxSection, 0, 1, 1, 1)
        self.plainTextEditMemory = QtGui.QPlainTextEdit(self.groupBoxMemory)
        font = QtGui.QFont()
        font.setFamily("Andale Mono")
        font.setPointSize(10)
        self.plainTextEditMemory.setFont(font)
        self.plainTextEditMemory.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEditMemory.setObjectName("plainTextEditMemory")
        self.gridLayoutMemoryBox.addWidget(self.plainTextEditMemory, 1, 0, 1, 2)
        self.gridLayoutMemory.addLayout(self.gridLayoutMemoryBox, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.splitterHorizontal, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuDebug = QtGui.QMenu(self.menubar)
        self.menuDebug.setObjectName("menuDebug")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionStart = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icons/enabled/resume_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStart.setIcon(icon)
        self.actionStart.setObjectName("actionStart")
        self.actionStepInto = QtGui.QAction(MainWindow)
        self.actionStepInto.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icons/enabled/stepinto_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStepInto.setIcon(icon1)
        self.actionStepInto.setObjectName("actionStepInto")
        self.actionStepOver = QtGui.QAction(MainWindow)
        self.actionStepOver.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icons/enabled/stepover_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStepOver.setIcon(icon2)
        self.actionStepOver.setObjectName("actionStepOver")
        self.actionStepReturn = QtGui.QAction(MainWindow)
        self.actionStepReturn.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icons/enabled/stepreturn_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStepReturn.setIcon(icon3)
        self.actionStepReturn.setObjectName("actionStepReturn")
        self.actionTerminate = QtGui.QAction(MainWindow)
        self.actionTerminate.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icons/enabled/terminate_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionTerminate.setIcon(icon4)
        self.actionTerminate.setObjectName("actionTerminate")
        self.actionSetStartAddress = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icons/enabled/goto_input.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetStartAddress.setIcon(icon5)
        self.actionSetStartAddress.setObjectName("actionSetStartAddress")
        self.actionPause = QtGui.QAction(MainWindow)
        self.actionPause.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icons/enabled/suspend_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon6)
        self.actionPause.setObjectName("actionPause")
        self.actionChangeRegisterValue = QtGui.QAction(MainWindow)
        self.actionChangeRegisterValue.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/icons/enabled/register_obj.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChangeRegisterValue.setIcon(icon7)
        self.actionChangeRegisterValue.setObjectName("actionChangeRegisterValue")
        self.actionRunToLine = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/icons/enabled/runtoline_co.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRunToLine.setIcon(icon8)
        self.actionRunToLine.setObjectName("actionRunToLine")
        self.actionMemoryManager = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/icons/enabled/memory_update.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMemoryManager.setIcon(icon9)
        self.actionMemoryManager.setObjectName("actionMemoryManager")
        self.menuDebug.addAction(self.actionStart)
        self.menuDebug.addAction(self.actionPause)
        self.menuDebug.addAction(self.actionTerminate)
        self.menuDebug.addAction(self.actionStepInto)
        self.menuDebug.addAction(self.actionStepOver)
        self.menuDebug.addAction(self.actionStepReturn)
        self.menuDebug.addSeparator()
        self.menuDebug.addAction(self.actionSetStartAddress)
        self.menuDebug.addAction(self.actionChangeRegisterValue)
        self.menuDebug.addAction(self.actionMemoryManager)
        self.menubar.addAction(self.menuDebug.menuAction())
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionTerminate)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStepInto)
        self.toolBar.addAction(self.actionStepOver)
        self.toolBar.addAction(self.actionStepReturn)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSetStartAddress)
        self.toolBar.addAction(self.actionChangeRegisterValue)
        self.toolBar.addAction(self.actionMemoryManager)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "AVR Debugger", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxMemory.setTitle(QtGui.QApplication.translate("MainWindow", "Memory", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSection.setText(QtGui.QApplication.translate("MainWindow", "Section:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDebug.setTitle(QtGui.QApplication.translate("MainWindow", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("MainWindow", "Start / Resume", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setToolTip(QtGui.QApplication.translate("MainWindow", "Start / Resume", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepInto.setText(QtGui.QApplication.translate("MainWindow", "Step Into", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepInto.setToolTip(QtGui.QApplication.translate("MainWindow", "Step Into", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepInto.setShortcut(QtGui.QApplication.translate("MainWindow", "F8", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepOver.setText(QtGui.QApplication.translate("MainWindow", "Step Over", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepOver.setToolTip(QtGui.QApplication.translate("MainWindow", "Step Over", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepReturn.setText(QtGui.QApplication.translate("MainWindow", "Step Return", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStepReturn.setToolTip(QtGui.QApplication.translate("MainWindow", "Step Return", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTerminate.setText(QtGui.QApplication.translate("MainWindow", "Terminate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTerminate.setToolTip(QtGui.QApplication.translate("MainWindow", "Terminate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetStartAddress.setText(QtGui.QApplication.translate("MainWindow", "Set Start Address...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause.setToolTip(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChangeRegisterValue.setText(QtGui.QApplication.translate("MainWindow", "Change Register Value...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChangeRegisterValue.setToolTip(QtGui.QApplication.translate("MainWindow", "Change Register Value", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRunToLine.setText(QtGui.QApplication.translate("MainWindow", "Run To Line", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRunToLine.setToolTip(QtGui.QApplication.translate("MainWindow", "Run To Line", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMemoryManager.setText(QtGui.QApplication.translate("MainWindow", "Memory Manager...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMemoryManager.setToolTip(QtGui.QApplication.translate("MainWindow", "Memory Manager", None, QtGui.QApplication.UnicodeUTF8))

import debugavr_rc
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/mmanager.ui'
#
# Created: Fri Aug 19 16:46:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except:
    from PySide import QtCore, QtGui

class Ui_MemoryManagerDialog(object):
    def setupUi(self, MemoryManagerDialog):
        MemoryManagerDialog.setObjectName("MemoryManagerDialog")
        MemoryManagerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        MemoryManagerDialog.resize(451, 309)
        self.gridLayout = QtGui.QGridLayout(MemoryManagerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.memoryList = QtGui.QTableWidget(MemoryManagerDialog)
        self.memoryList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.memoryList.setAlternatingRowColors(True)
        self.memoryList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.memoryList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.memoryList.setObjectName("memoryList")
        self.memoryList.setColumnCount(3)
        self.memoryList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.memoryList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.memoryList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.memoryList.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.memoryList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = QtGui.QPushButton(MemoryManagerDialog)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(MemoryManagerDialog)
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout.addWidget(self.removeButton)
        self.saveButton = QtGui.QPushButton(MemoryManagerDialog)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(MemoryManagerDialog)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout.addWidget(self.closeButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(MemoryManagerDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), MemoryManagerDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(MemoryManagerDialog)

    def retranslateUi(self, MemoryManagerDialog):
        MemoryManagerDialog.setWindowTitle(QtGui.QApplication.translate("MemoryManagerDialog", "Memory Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.memoryList.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MemoryManagerDialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.memoryList.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MemoryManagerDialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.memoryList.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MemoryManagerDialog", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("MemoryManagerDialog", "Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("MemoryManagerDialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MemoryManagerDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("MemoryManagerDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/addmem.ui'
#
# Created: Fri Aug 19 16:46:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except:
    from PySide import QtCore, QtGui

class Ui_AddMemoryDialog(object):
    def setupUi(self, AddMemoryDialog):
        AddMemoryDialog.setObjectName("AddMemoryDialog")
        AddMemoryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AddMemoryDialog.resize(362, 102)
        self.gridLayout = QtGui.QGridLayout(AddMemoryDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelAddress = QtGui.QLabel(AddMemoryDialog)
        self.labelAddress.setObjectName("labelAddress")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelAddress)
        self.lineEditAddress = QtGui.QLineEdit(AddMemoryDialog)
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditAddress)
        self.lineEditSize = QtGui.QLineEdit(AddMemoryDialog)
        self.lineEditSize.setObjectName("lineEditSize")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditSize)
        self.labelSize = QtGui.QLabel(AddMemoryDialog)
        self.labelSize.setObjectName("labelSize")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelSize)
        self.horizontalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(AddMemoryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(AddMemoryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddMemoryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddMemoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddMemoryDialog)

    def retranslateUi(self, AddMemoryDialog):
        AddMemoryDialog.setWindowTitle(QtGui.QApplication.translate("AddMemoryDialog", "Add Memory Block", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAddress.setText(QtGui.QApplication.translate("AddMemoryDialog", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSize.setText(QtGui.QApplication.translate("AddMemoryDialog", "Size in bytes", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/changeval.ui'
#
# Created: Fri Aug 19 16:46:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except:
    from PySide import QtCore, QtGui

class Ui_ChangeValueDialog(object):
    def setupUi(self, ChangeValueDialog):
        ChangeValueDialog.setObjectName("ChangeValueDialog")
        ChangeValueDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ChangeValueDialog.resize(440, 90)
        self.gridLayout = QtGui.QGridLayout(ChangeValueDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelRegister = QtGui.QLabel(ChangeValueDialog)
        self.labelRegister.setObjectName("labelRegister")
        self.horizontalLayout.addWidget(self.labelRegister)
        self.comboBoxRegister = QtGui.QComboBox(ChangeValueDialog)
        self.comboBoxRegister.setObjectName("comboBoxRegister")
        self.horizontalLayout.addWidget(self.comboBoxRegister)
        self.labelValue = QtGui.QLabel(ChangeValueDialog)
        self.labelValue.setObjectName("labelValue")
        self.horizontalLayout.addWidget(self.labelValue)
        self.lineEditValue = QtGui.QLineEdit(ChangeValueDialog)
        self.lineEditValue.setObjectName("lineEditValue")
        self.horizontalLayout.addWidget(self.lineEditValue)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeValueDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(ChangeValueDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ChangeValueDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ChangeValueDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeValueDialog)

    def retranslateUi(self, ChangeValueDialog):
        ChangeValueDialog.setWindowTitle(QtGui.QApplication.translate("ChangeValueDialog", "Change Register Value", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRegister.setText(QtGui.QApplication.translate("ChangeValueDialog", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.labelValue.setText(QtGui.QApplication.translate("ChangeValueDialog", "Value", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/input.ui'
#
# Created: Fri Aug 19 16:46:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except:
    from PySide import QtCore, QtGui

class Ui_InputDialog(object):
    def setupUi(self, InputDialog):
        InputDialog.setObjectName("InputDialog")
        InputDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        InputDialog.resize(440, 114)
        self.gridLayout = QtGui.QGridLayout(InputDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelField = QtGui.QLabel(InputDialog)
        self.labelField.setObjectName("labelField")
        self.horizontalLayout.addWidget(self.labelField)
        self.lineEditField = QtGui.QLineEdit(InputDialog)
        self.lineEditField.setObjectName("lineEditField")
        self.horizontalLayout.addWidget(self.lineEditField)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(InputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.labelInfo = QtGui.QLabel(InputDialog)
        self.labelInfo.setObjectName("labelInfo")
        self.gridLayout.addWidget(self.labelInfo, 0, 0, 1, 1)

        self.retranslateUi(InputDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), InputDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), InputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InputDialog)

    def retranslateUi(self, InputDialog):
        InputDialog.setWindowTitle(QtGui.QApplication.translate("InputDialog", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.labelField.setText(QtGui.QApplication.translate("InputDialog", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfo.setText(QtGui.QApplication.translate("InputDialog", "Information", None, QtGui.QApplication.UnicodeUTF8))

