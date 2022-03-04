# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testrotate.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from configparser import SafeConfigParser
import os, ast

parser = SafeConfigParser()
custom_file = 'custom_setup.cfg'
exists = os.path.isfile(custom_file)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(721, 794)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(701, 541))
        self.textEdit.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.textEdit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 4)

        self.pushButtonNewnote = QPushButton(self.centralwidget)
        self.pushButtonNewnote.setObjectName(u"pushButtonNewnote")
        self.pushButtonDelete = QPushButton(self.centralwidget)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")
        self.pushButtonSaveas = QPushButton(self.centralwidget)
        self.pushButtonSaveas.setObjectName(u"pushButtonSaveas")
        self.pushButtonRenameTab = QPushButton(self.centralwidget)
        self.pushButtonRenameTab.setObjectName(u"pushButtonRenameTab")

        self.gridLayout.addWidget(self.pushButtonNewnote, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.pushButtonDelete, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.pushButtonRenameTab, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.pushButtonSaveas, 1, 3, 1, 1)
        

        self.textEdit_console = QTextEdit(self.centralwidget)
        self.textEdit_console.setObjectName(u"textEdit_console")
        self.textEdit_console.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_console.setFont(font)
        self.textEdit_console.setReadOnly(True)

        self.gridLayout.addWidget(self.textEdit_console, 2, 0, 1, 4)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 721, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
        # setupUi

        # add custom tab if user setting exist
        if exists:
            with open(custom_file,"r") as fdict:
                mydict = ast.literal_eval(fdict.read())
            count_tab = 1
            maxcount_tab = len(mydict['tabname'])
            while count_tab <= int(maxcount_tab):
                for value in mydict['tabname'].keys():
                    nametab = mydict['tabname'][value]['name']
                    #print("debug:",nametab)
                    self.create_import(value,nametab)
                    count_tab += 1
        else:
            self.CreateDefault(MainWindow)

    def create_import(self,keytab,nametab):
        self.tab_value = QWidget()
        self.tab_value.setObjectName(keytab)
        self.tabWidget.addTab(self.tab_value, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_value), QCoreApplication.translate("MainWindow", nametab, None))

    def CreateDefault(self, MainWindow):
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textEdit = QPlainTextEdit(self.tab)
        self.textEdit.setObjectName(u"textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.textEdit2 = QPlainTextEdit(self.tab_2)
        self.textEdit2.setObjectName(u"textEdit2")
        self.gridLayout_3.addWidget(self.textEdit2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))

    def CreateCustom(self, MainWindow, value):
        self.tab_value = QWidget()
        self.tab_value.setObjectName(u"tab_"+value)
        self.gridLayout_value = QGridLayout(self.tab_value)
        self.gridLayout_value.setObjectName(u"gridLayout_"+value)
        
        self.tabWidget.addTab(self.tab_value, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_value), QCoreApplication.translate("MainWindow", value, None))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButtonNewnote.setText(QCoreApplication.translate("MainWindow", u"Add note", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("MainWindow", u"Delete note", None))
        self.pushButtonSaveas.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.pushButtonRenameTab.setText(QCoreApplication.translate("MainWindow", u"Rename note", None))

    # retranslateUi

