""" UI """
# -*- coding: utf-8 -*-
# pylint: disable=E0602

################################################################################
## Form generated from reading UI file 'testrotate.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
import ast
from pathlib import Path

from PySide2.QtCore import ( QCoreApplication, Qt, QSize, QRect, QMetaObject )
from PySide2.QtWidgets import ( QTabWidget, QTextEdit,QStatusBar, QMenuBar, QGridLayout,
    QPushButton, QWidget, QLabel, QPlainTextEdit )
from PySide2.QtGui import QFont

HOMEDIR = os.path.expanduser('~')
DATADIR = HOMEDIR+'/.lxnotit/data/'
CHECKINSTALL = os.path.isdir(HOMEDIR+'/.lxnotit')
CUSTOM_FILE = DATADIR + "custom_setup.cfg"
LIBDIRPARENT = Path(__file__).resolve().parents[1]
EXISTS = os.path.isfile(CUSTOM_FILE)

class UiMainWindow():
    """ Main class """

    def __init__(self):
        """ Init  """
        self.tabwidget = None
        self.gridlayout_2 = None
        self.gridlayout = None
        self.textedit = None
        self.textedit2 = None
        self.tab_2 = None
        self.tab = None
        self.statusbar = None
        self.menubar = None
        self.gridlayout_value = None
        self.label = None
        self.textedit_console = None
        self.tab_value = None
        self.pushbuttondelete = None
        self.pushbuttonsaveas = None
        self.pushbuttonnewnote = None
        self.pushbuttonrenametab = None
        self.gridlayout_3 = None
        self.centralwidget = None

    def init_widget(self,mainwindow):
        """ init widget """
        self.centralwidget = QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridlayout_2 = QGridLayout(self.centralwidget)
        self.gridlayout_2.setObjectName("gridlayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridlayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.tabwidget = QTabWidget(self.centralwidget)
        self.tabwidget.setObjectName("tabWidget")
        self.tabwidget.setMaximumSize(QSize(16777215, 30))
        self.tabwidget.setElideMode(Qt.ElideNone)
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.setMovable(False)
        self.tabwidget.setTabBarAutoHide(False)

        self.gridlayout_2.addWidget(self.tabwidget, 1, 0, 1, 1)

        self.gridlayout = QGridLayout()
        self.gridlayout.setObjectName("gridLayout")
        self.textedit = QTextEdit(self.centralwidget)
        self.textedit.setObjectName("textEdit")
        self.textedit.setMinimumSize(QSize(701, 541))
        self.textedit.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.textedit.setAcceptRichText(False)

        self.gridlayout.addWidget(self.textedit, 0, 0, 1, 4)

        self.pushbuttonnewnote = QPushButton(self.centralwidget)
        self.pushbuttonnewnote.setObjectName("pushbuttonnewnote")
        self.pushbuttondelete = QPushButton(self.centralwidget)
        self.pushbuttondelete.setObjectName("pushbuttondelete")
        self.pushbuttonsaveas = QPushButton(self.centralwidget)
        self.pushbuttonsaveas.setObjectName("pushbuttonsaveas")
        self.pushbuttonrenametab = QPushButton(self.centralwidget)
        self.pushbuttonrenametab.setObjectName("pushbuttonrenametab")

        self.gridlayout.addWidget(self.pushbuttonnewnote, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.pushbuttondelete, 1, 1, 1, 1)
        self.gridlayout.addWidget(self.pushbuttonrenametab, 1, 2, 1, 1)
        self.gridlayout.addWidget(self.pushbuttonsaveas, 1, 3, 1, 1)

        self.textedit_console = QTextEdit(self.centralwidget)
        self.textedit_console.setObjectName("textedit_console")
        self.textedit_console.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textedit_console.setFont(font)
        self.textedit_console.setReadOnly(True)

        self.gridlayout.addWidget(self.textedit_console, 2, 0, 1, 4)

        self.gridlayout_2.addLayout(self.gridlayout, 2, 0, 1, 1)

    def setup_ui(self, mainwindow):
        """ Define widget """
        if not mainwindow.objectName():
            mainwindow.setObjectName("mainwindow")

        self.init_widget(mainwindow)
        mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainwindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 721, 22))
        mainwindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslate_ui(mainwindow)

        self.tabwidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mainwindow)
        # setupUi

        # add custom tab if user setting exist
        if EXISTS:
            with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
                mydict = ast.literal_eval(fdict.read())
            count_tab = 1
            maxcount_tab = len(mydict['tabname'])
            while count_tab <= int(maxcount_tab):
                for value in mydict['tabname'].keys():
                    nametab = mydict['tabname'][value]['name']
                    self.create_import(value,nametab)
                    count_tab += 1
        else:
            self.create_default()

    def create_import(self,keytab,nametab):
        """ When import """
        self.tab_value = QWidget()
        self.tab_value.setObjectName(keytab)
        self.tabwidget.addTab(self.tab_value, "")
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_value),
            QCoreApplication.translate("mainwindow", nametab, None))

    def create_default(self):
        """ First launch or not conf """
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridlayout_2 = QGridLayout(self.tab)
        self.gridlayout_2.setObjectName("gridlayout_2")
        self.textedit = QPlainTextEdit(self.tab)
        self.textedit.setObjectName("textedit")
        self.gridlayout_2.addWidget(self.textedit, 0, 0, 1, 1)
        self.tabwidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridlayout_3 = QGridLayout(self.tab_2)
        self.gridlayout_3.setObjectName("gridlayout_3")
        self.textedit2 = QPlainTextEdit(self.tab_2)
        self.textedit2.setObjectName("textedit2")
        self.gridlayout_3.addWidget(self.textedit2, 0, 0, 1, 1)
        self.tabwidget.addTab(self.tab_2, "")

        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab),
            QCoreApplication.translate("mainwindow", "Tab 1", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_2),
            QCoreApplication.translate("mainwindow", "Tab 2", None))

    def create_custom(self, value):
        """ Custom config """
        self.tab_value = QWidget()
        self.tab_value.setObjectName("tab_"+value)
        self.gridlayout_value = QGridLayout(self.tab_value)
        self.gridlayout_value.setObjectName("gridLayout_"+value)
        self.tabwidget.addTab(self.tab_value, "")
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_value),
         QCoreApplication.translate("mainwindow", value, None))

    def retranslate_ui(self, mainwindow):
        """ Retranslate """
        mainwindow.setWindowTitle(QCoreApplication.translate("mainwindow", "lxnotit",
            None))
        self.label.setText(QCoreApplication.translate("mainwindow",
            "take and save your notes",
            None))
        self.pushbuttonnewnote.setText(QCoreApplication.translate("mainwindow", "Add note",
            None))
        self.pushbuttondelete.setText(QCoreApplication.translate("mainwindow", "Delete note",
            None))
        self.pushbuttonsaveas.setText(QCoreApplication.translate("mainwindow", "Save as",
            None))
        self.pushbuttonrenametab.setText(QCoreApplication.translate("mainwindow", "Rename note",
            None))

    # retranslateUi
