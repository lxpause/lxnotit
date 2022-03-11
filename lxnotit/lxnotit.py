""" Main Application """

# -*- coding: utf-8 -*-
# pylint: disable=E0602,E1101

import sys
import os
import ast
import json

from shutil import copy,Error
from pathlib import Path
from PySide2.QtCore import ( QCoreApplication )
from PySide2.QtWidgets import ( QApplication, QMainWindow, QFileDialog,
QAction, QMessageBox, QInputDialog, QWidget )
from lxnotit.lxnotitui import UiMainWindow

HOMEDIR = os.path.expanduser('~')
DATADIR = HOMEDIR+'/.lxnotit/data/'
CUSTOM_FILE = DATADIR + "custom_setup.cfg"
CHECKINSTALL = os.path.isfile(CUSTOM_FILE)
LIBDIRPARENT = Path(__file__).resolve().parents[1]


class MainWindow(QMainWindow, UiMainWindow):
    """ Main Class """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tab_value = None
        self.returnvalue = None

        self.setup_ui(self)

        # Check if signal on changed tab
        self.tabwidget.currentChanged.connect(self.displaynote)

        # Begin Bar menu
        topmenu = self.menuBar()
        filemenu = topmenu.addMenu('File')
        exitmenu = QAction('Quit', self)
        exitmenu.setShortcut('Ctrl+Q')
        exitmenu.triggered.connect(qApp.quit)
        importmenu = QAction('Import file', self)
        importmenu.setShortcut('Ctrl+I')
        importmenu.triggered.connect(self.importfile)
        exportmenu = QAction('Export file', self)
        exportmenu.setShortcut('Ctrl+P')
        exportmenu.triggered.connect(self.exportfile)
        filemenu.addAction(importmenu)
        filemenu.addAction(exportmenu)
        filemenu.addAction(exitmenu)

        helpmenu = topmenu.addMenu('Help')
        aboutmenu = QAction('About', self)
        helpmenu.addAction(aboutmenu)
        helpmenu.triggered.connect(self.aboutapp)
        # End Bar menu

        # autosave data when changed char on the textedit
        texteditdocument = self.textedit.document()
        texteditdocument.contentsChanged.connect(self.savefile)

        self.tabwidget.tabCloseRequested.connect(self.closenote)

        self.pushbuttonrenametab.clicked.connect(self.renamenote)
        self.pushbuttonsaveas.clicked.connect(self.saveasnote)
        self.pushbuttonnewnote.clicked.connect(self.addnote)
        self.pushbuttondelete.clicked.connect(self.deletenote)

        self.displaynote(None)

    def addnote(self):
        """ Add new note and associate tab """
        i = 0
        with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
            mydict = ast.literal_eval(fdict.read())
        for i in range(1,99):
            notename = "note" + str(i)
            if notename in mydict['tabname'].keys():
                i+=1
            else:
                self.tab_value = QWidget()
                self.tabwidget.insertTab(0,self.tab_value, notename)
                # switch to new tab after create
                self.tabwidget.setCurrentIndex(0)
                self.tab_value.setObjectName(notename)
                self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_value),
                 QCoreApplication.translate("MainWindow", notename, None))
                try:
                    mydict['tabname'][notename] = {}
                    mydict['tabname'][notename]['name'] = notename
                    mydict['tabname'][notename]['data'] = DATADIR+notename+'.out'
                    with open(CUSTOM_FILE,"w",encoding="utf-8") as fdict:
                        try:
                            fdict.write(json.dumps(mydict))
                            with open(DATADIR+notename+'.out','a',encoding="utf-8"):
                                pass
                        except IOError as error:
                            print(error)
                    with open(DATADIR+notename+'.out','r',encoding="utf-8") as newfile:
                        self.textedit.setText(newfile.read())
                except TypeError:
                    self.textedit_console.setText('Error on rename note')
                break


    def renamenote(self):
        """ Rename actual note """
        currenttab = self.tabwidget.currentWidget().objectName()
        newname, answer = QInputDialog.getText(self, 'input dialog',
            'Insert new name of note '+currenttab)
        if answer:
            with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
                mydict = json.loads(fdict.read())
                olddir = mydict['tabname'][currenttab]['data']
            with open(CUSTOM_FILE,"w",encoding="utf-8") as fdict:
                mydict['tabname'][newname] = mydict['tabname'].pop(currenttab)
                mydict['tabname'][newname]['name'] = newname
                mydict['tabname'][newname]['data'] = DATADIR+newname+'.out'
                try:
                    fdict.write(json.dumps(mydict))
                    os.rename(olddir,DATADIR+newname+'.out')
                except IOError:
                    self.textedit_console.setText('Error on rename note')
        self.textedit_console.setText('Change title: '+currenttab + 'to: '+newname)
        currentindextab = self.tabwidget.currentIndex()
        self.textedit_console.setText('you are close the index:'+str(currentindextab))
        self.tabwidget.removeTab(currentindextab)
        self.tab_value = QWidget()
        self.tab_value.setObjectName(newname)
        self.tabwidget.addTab(self.tab_value, "")
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_value),
            QCoreApplication.translate("MainWindow", newname, None))

    # def detecttab(self):
    #     """ Detect current tab """
    #     currenttab = self.tabWidget.currentWidget().objectName()

    def displaynote(self,args):
        """ Display data of note """
        if args is True:
            # reload app after create new config
            python = sys.executable
            os.execl(python, python, * sys.argv)
        else:
            currenttab = self.tabwidget.currentWidget().objectName()
            try:
                with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
                    mydict = json.loads(fdict.read())
                    datadict = mydict['tabname'][currenttab]['data']
                with open(datadict,'r',encoding="utf-8") as datafile:
                    self.textedit.setText(datafile.read())
            except IOError as error:
                #print("debug",mydict,datadict)
                print(error)
            self.textedit_console.setText('You are on note: '+currenttab)

    def importfile(self):
        """ Import config file """
        options = QFileDialog.Options()
        # With underscore , ignore a value after return tuple of fileName
        # to retrieve only filename selected
        filename, _ = QFileDialog.getOpenFileName(parent=self,
            caption='Open file', dir='.',
            filter='(custom_setup_export.cfg) ;; All files (*)',
            options=options)
        if filename:
            if CHECKINSTALL:
                self.textedit_console.setStyleSheet("QTextEdit {color:red}")
                self.textedit_console.setText("File already exist")
            else:
                try:
                    copy(filename,CUSTOM_FILE)
                    self.textedit_console.setStyleSheet("QTextEdit {color:blue}")
                    self.textedit_console.setText("Import successfully. \
                        Restarting application.")
                    self.displaynote(True)
                except Error as err:
                    self.textedit_console.setText(err.args[0])

    def exportfile(self):
        """ Export config to file """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(parent=self,
            caption='Save file',
            dir='.',
            filter='(custom_setup_export.cfg) ;; All files (*)',
            options=options)
        if filename:
            try:
                copy(CUSTOM_FILE,filename)
                self.textedit_console.setStyleSheet("QTextEdit {color:blue}")
                self.textedit_console.setText("Export successfully")
            except Error as err:
                self.textedit_console.setStyleSheet("QTextEdit {color:red}")
                self.textedit_console.setText(err.args[0])

    def saveasnote(self):
        """ Save data of note to another file """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(parent=self,
            caption='Save note', dir='.',
            filter='All files (*)', options=options)
        if filename:
            currenttab = self.tabwidget.currentWidget().objectName()
            with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
                mydict = ast.literal_eval(fdict.read())
                datadict = mydict['tabname'][currenttab]['data']
                try:
                    copy(datadict,filename)
                    self.textedit_console.setStyleSheet("QTextEdit {color:blue}")
                    self.textedit_console.setText("Export note successfully")
                except Error as err:
                    self.textedit_console.setStyleSheet("QTextEdit {color:red}")
                    self.textedit_console.setText(err.args[0])

    @classmethod
    def fileabout(cls):
        """ Read about file - install also with setup on python lib"""
        aboutfile = str(LIBDIRPARENT) + '/static/about.cfg'
        existfile = os.path.isfile(aboutfile)
        if existfile:
            aboutdir = str(LIBDIRPARENT) + '/static/about.cfg'
        else:
            aboutdir = 'static/about.cfg'
        with open(aboutdir,'r',encoding="utf-8") as file:
            return file.read()

    def aboutapp(self):
        """ About popup """
        aboutmsg = QMessageBox()
        aboutmsg.setWindowTitle("About")
        aboutmsg.setInformativeText(self.fileabout())
        aboutmsg.setStandardButtons(QMessageBox.Close)
        aboutmsg.exec_()

    def savefile(self):
        """ Autosave note to data """
        currenttab = self.tabwidget.currentWidget().objectName()
        with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
            mydict = ast.literal_eval(fdict.read())
            datadict = mydict['tabname'][currenttab]['data']
        with open(datadict,'w',encoding="utf-8") as datafile:
            try:
                datafile.write(self.textedit.toPlainText())
                self.textedit_console.setText('save file successfully for note: '+ currenttab)
            except IOError as error:
                self.textedit_console.setText('error on save to file...' + error)

    def closenote(self):
        """ Close note after click on tab """
        currentindextab = self.tabwidget.currentIndex()
        self.textedit_console.setText('You are close the index:'+str(currentindextab))
        self.tabwidget.removeTab(currentindextab)

    def diagbox(self,args):
        """ Dailog box """
        dgbox = QMessageBox()
        dgbox.setIcon(QMessageBox.Warning)
        dgbox.setText("Do you really want delete " + args.upper() + " and all data ?")
        dgbox.setWindowTitle("Delete note")
        dgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.returnvalue = dgbox.exec()

    def deletenote(self):
        """ Delete note and data files """
        currenttab = self.tabwidget.currentWidget().objectName()
        self.diagbox(str(currenttab))
        if self.returnvalue == QMessageBox.Ok:
            with open(CUSTOM_FILE,"r",encoding="utf-8") as fdict:
                mydict = json.loads(fdict.read())
                olddir = mydict['tabname'][currenttab]['data']
            with open(CUSTOM_FILE,"w",encoding="utf-8") as fdict:
                mydict['tabname'].pop(currenttab)
                try:
                    fdict.write(json.dumps(mydict))
                    os.remove(olddir)
                except IOError:
                    self.textedit_console.setText('Error on delete note')
        self.textedit_console.setText('Delete note successfully')
        currentindextab = self.tabwidget.currentIndex()
        self.tabwidget.removeTab(currentindextab)

    def createconfig(self):
        """ Create custom config """
        customdict = {}
        customdict['tabname'] = {}
        i=1
        for i in range(1,3):
            customnote = "note"+str(i)
            customdict['tabname'][customnote] = {}
            customdict['tabname'][customnote]["name"] = customnote
            customdict['tabname'][customnote]["data"] = DATADIR+customnote+'.out'
        with open(CUSTOM_FILE,"w",encoding="utf-8") as cfile:
            cfile.write(json.dumps(customdict))
        self.displaynote(True)

    def checkinstall(self):
        """ Check if existing install """
        if CHECKINSTALL:
            pass
        else:
            dgbox = QMessageBox()
            dgbox.setIcon(QMessageBox.Warning)
            dgbox.setText('''
                No config detected. Proceed to create new install ? 
                \n If no install proceed, you can't save your notes.''')
            dgbox.setWindowTitle("Install config")
            dgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnbox = dgbox.exec()
            if returnbox == QMessageBox.Ok:
                configfile = str(LIBDIRPARENT)+'/static/custom_setup.cfg'
                listfiles = [configfile]
                for i in range(1,3):
                    notefileadd = str(LIBDIRPARENT)+'/static/note'+str(i)+'.out'
                    listfiles.append(notefileadd)
                if not os.path.isdir(DATADIR):
                    try:
                        os.makedirs(DATADIR)
                    except IOError as error:
                        print(error)
                try:
                    for files in listfiles:
                        copy(str(files), str(DATADIR))
                    print("end copy files")
                except IOError as error:
                    print(error)
                self.createconfig()

    @classmethod
    def main(cls):
        """ Main application """
        app = QApplication(sys.argv)
        mainpynv = MainWindow()
        mainpynv.checkinstall()
        mainpynv.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    MainWindow.main()
