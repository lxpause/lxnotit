from PySide2.QtWidgets  import (
QApplication, QMainWindow, QTabWidget, QFileDialog, QMenu, 
QAction, QMessageBox, QPlainTextEdit, QGridLayout, QInputDialog, QWidget
)

from PySide2.QtGui import *
from PySide2.QtCore import *

from lxnotitUI  import Ui_MainWindow
import sys, os, ast, json
from shutil import copy,Error

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)

        # Check if signal on changed tab
        self.tabWidget.currentChanged.connect(self._display_note)

        # Begin Bar menu
        TopMenu = self.menuBar()
        FileMenu = TopMenu.addMenu('File')
        ExitMenu = QAction('Quit', self)
        ExitMenu.setShortcut('Ctrl+Q')
        ExitMenu.triggered.connect(qApp.quit)
        ImportMenu = QAction('Import file', self)
        ImportMenu.setShortcut('Ctrl+I')
        ImportMenu.triggered.connect(self._import_file)
        ExportMenu = QAction('Export file', self)
        ExportMenu.setShortcut('Ctrl+P')
        ExportMenu.triggered.connect(self._export_file)
        FileMenu.addAction(ImportMenu)
        FileMenu.addAction(ExportMenu)
        FileMenu.addAction(ExitMenu)

        HelpMenu = TopMenu.addMenu('Help')
        AboutMenu = QAction('About', self)  
        HelpMenu.addAction(AboutMenu)
        HelpMenu.triggered.connect(self._about)
        # End Bar menu

        # autosave data when changed char on the textedit
        textEditdocument = self.textEdit.document()
        textEditdocument.contentsChanged.connect(self._save_File)

        self.tabWidget.tabCloseRequested.connect(self._close_note)
        self.pushButtonRenameTab.clicked.connect(self._rename_note)
        self.pushButtonSaveas.clicked.connect(self._saveas_note)

        self.pushButtonNewnote.clicked.connect(self._add_note)

    def _add_note(self):
        i = 0
        custom_file = 'custom_setup.cfg'
        exists = os.path.isfile(custom_file)
        with open(custom_file,"r") as fdict:
            mydict = ast.literal_eval(fdict.read())
        for i in range(1,99):
            notename = "note" + str(i)
            if notename in mydict['tabname'].keys():
                i+=1
            else:
                self.tab_value = QWidget()
                self.tabWidget.insertTab(0,self.tab_value, notename)
                # switch to new tab after create
                self.tabWidget.setCurrentIndex(0)
                self.tab_value.setObjectName(notename)
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_value), QCoreApplication.translate("MainWindow", notename, None))
                try:
                    currentTab = self.tabWidget.currentWidget().objectName()
                    mydict['tabname'][notename] = {}
                    mydict['tabname'][notename]['name'] = notename
                    mydict['tabname'][notename]['data'] = 'data/'+notename+'.out'
                    with open(custom_file,"w") as fdict:
                        try:
                            fdict.write(json.dumps(mydict))
                            with open('data/'+notename+'.out','a'):
                                pass
                        except Exception as e:
                            print(e)
                    with open('data/'+notename+'.out','r') as newfile:
                        self.textEdit.setText(newfile.read())                    
                except TypeError:
                    self.textEdit_console.setText('Error on rename note')
                break


    def _rename_note(self):
        currentTab = self.tabWidget.currentWidget().objectName()
        newname, answer = QInputDialog.getText(self, 'input dialog', 'Insert new name of note '+currentTab)
        if answer:
            custom_file = 'custom_setup.cfg'
            with open(custom_file,"r") as fdict:
                mydict = json.loads(fdict.read())
                olddir = mydict['tabname'][currentTab]['data']
            with open(custom_file,"w") as fdict:
                mydict['tabname'][newname] = mydict['tabname'].pop(currentTab)
                mydict['tabname'][newname]['name'] = newname
                mydict['tabname'][newname]['data'] = 'data/'+newname+'.out'
                try:
                    fdict.write(json.dumps(mydict))
                    os.rename(olddir,'data/'+newname+'.out')
                except:
                    self.textEdit_console.setText('Error on rename note')
        self.textEdit_console.setText('Change title: '+currentTab + 'to: '+newname)
        currentIndexTab = self.tabWidget.currentIndex()
        self.textEdit_console.setText('You are close the index:'+str(currentIndexTab))
        self.tabWidget.removeTab(currentIndexTab)
        self.tab_value = QWidget()
        self.tab_value.setObjectName(newname)
        self.tabWidget.addTab(self.tab_value, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_value), QCoreApplication.translate("MainWindow", newname, None))

    def _detect_Tab(self):
        currentTab = self.tabWidget.currentWidget().objectName()

    def _display_note(self):
        currentTab = self.tabWidget.currentWidget().objectName()
        #self.textEdit.setText("You are on: " + str(currentTab))
        custom_file = 'custom_setup.cfg'
        exists = os.path.isfile(custom_file)
        try:
            with open(custom_file,"r") as fdict:
                mydict = json.loads(fdict.read())
                #print(mydict, currentTab)
                #print(mydict['tabname'][currentTab]['data'])
                datadict = mydict['tabname'][currentTab]['data']
            with open(datadict,'r') as dataFile:
                # self.loadText()
                self.textEdit.setText(dataFile.read())
        except Exception as e:
            print(e)
        self.textEdit_console.setText('You are on note: '+currentTab)

    def _import_file(self):
        options = QFileDialog.Options()
        # With underscore , ignore a value after return tuple of fileName to retrieve only filename selected
        fileName, _ = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='(custom_setup_export.cfg) ;; All files (*)', options=options)
        if fileName:
            custom_file = 'custom_setup.cfg'
            exist_file = os.path.isfile(custom_file)
            if exist_file:
                self.textEdit_console.setStyleSheet("QTextEdit {color:red}")
                self.textEdit_console.setText("File already exist")
            else:
                try:
                    copy(fileName,'./custom_setup.cfg')
                    self.textEdit_console.setStyleSheet("QTextEdit {color:blue}")
                    self.textEdit_console.setText("Import successfully. You must restart application.")
                except Error as err:
                    self.textEdit_console.setText(err.args[0])

    def _export_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(parent=self, caption='Save file', dir='.', filter='(custom_setup_export.cfg) ;; All files (*)', options=options)
        if fileName:
            custom_file = 'custom_setup.cfg'
            try:
                copy(custom_file,fileName)
                self.textEdit_console.setStyleSheet("QTextEdit {color:blue}")
                self.textEdit_console.setText("Export successfully")
            except Error as err:
                self.textEdit_console.setStyleSheet("QTextEdit {color:red}")
                self.textEdit_console.setText(err.args[0])

    def _saveas_note(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(parent=self, caption='Save note', dir='.', filter='All files (*)', options=options)
        if fileName:
            currentTab = self.tabWidget.currentWidget().objectName()
            custom_file = 'custom_setup.cfg'
            exists = os.path.isfile(custom_file)
            with open(custom_file,"r") as fdict:
                mydict = ast.literal_eval(fdict.read())
                datadict = mydict['tabname'][currentTab]['data']
                try:
                    copy(datadict,fileName)
                    self.textEdit_console.setStyleSheet("QTextEdit {color:blue}")
                    self.textEdit_console.setText("Export note successfully")
                except Error as err:
                    self.textEdit_console.setStyleSheet("QTextEdit {color:red}")
                    self.textEdit_console.setText(err.args[0])

    def _affich(self):
        self.textEdit_console.setText(str("Vous êtes sur la note. Sauvegarde en cours de toutes modifications."))

    def _about(self):
        aboutmsg = QMessageBox()
        with open('about.cfg') as file:
            fileabout = file.read()
            aboutmsg.setWindowTitle("About")
            aboutmsg.setInformativeText(fileabout)
            aboutmsg.setStandardButtons(QMessageBox.Close)
            ret = aboutmsg.exec_()

    def _save_File(self):
        currentTab = self.tabWidget.currentWidget().objectName()
        custom_file = 'custom_setup.cfg'
        exists = os.path.isfile(custom_file)
        with open(custom_file,"r") as fdict:
            mydict = ast.literal_eval(fdict.read())
            datadict = mydict['tabname'][currentTab]['data']
        with open(datadict,'w') as dataFile:
            try:
                dataFile.write(self.textEdit.toPlainText())
                self.textEdit_console.setText('save file successfully for note: '+ currentTab)
            except:
                self.textEdit_console.setText('error on save to file...',IOError)

    def _close_note(self):
        currentIndexTab = self.tabWidget.currentIndex()
        self.textEdit_console.setText('You are close the index:'+str(currentIndexTab))
        self.tabWidget.removeTab(currentIndexTab)

    def setHyperlinkOnSelection(self, url):
        # Grab the text's format
        fmt = self.textEdit.currentCharFormat()

        # Set the format to an anchor with the specified url
        fmt.setAnchor(True)
        fmt.setAnchorHref(url)

        # And set the next char format
        self.textEdit.setCurrentCharFormat(fmt)
            

if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    mainpynv = MainWindow()
    mainpynv.show()
    # Load Initial data
    mainpynv._display_note()
    sys.exit(app.exec_())