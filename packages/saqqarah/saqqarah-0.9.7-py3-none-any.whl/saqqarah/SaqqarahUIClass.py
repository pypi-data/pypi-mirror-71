#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:34:32 2020

@author: yves


    This file is part of Saqqarah.

    Saqqarah is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Saqqarah is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Saqqarah.  If not, see <https://www.gnu.org/licenses/>
"""

from . import Pyramid, PyramidPrinterImage, PyramidPrinterTikz

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimeLine, QThread
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QFileDialog, QAction
from PySide2.QtCore import QStandardPaths as sp
from PIL.ImageQt import toqpixmap

from time import sleep

class LookingForPuzzleThread(QThread):
    def __init__(self, uicontrol):
        QThread.__init__(self)
        self.uicontrol = uicontrol

    def __del__(self):
        self.wait()

    def run(self):
        self.uicontrol.pyramid.get_puzzle(difficulty=self.uicontrol.difficulty,
                                          min = self.uicontrol.value_min,
                                          max = self.uicontrol.value_max,
                                          seed = self.uicontrol.seed,
                                          non_zero = self.uicontrol.exclude_zero)

class SaqqarahUI:
    def __init__(self, window):
        # defaut values
        self.size = 5
        self.size_min= 4 
        self.size_max= 12
        self.difficulty = 2
        self.difficulty_min = 1
        self.difficulty_max = 5
        self.seed = None
        self.value_min = 0
        self.value_max = 9
        self.exclude_zero = False
        self.seed = None
        self.images = {}
        self.generating = False
        self.output_directory = sp.writableLocation(sp.DocumentsLocation)
        #TODO: add some parameters
        self.resolution = 300
        self.latex_separator = ''

        self.init_ui(window)
        # 1000 seconds
        self.timeline = QTimeLine(2_000, self.window)
        self.init_timeline()
        self.combo_init()
        self.seed_init()
        self.zero_init()
        self.update_pyramid()
        
    def zero_init(self):
        zeroCheck = self.window.zeroCheckbox
        self.exlude_zero = zeroCheck.isChecked()
        zeroCheck.stateChanged.connect(self.zero_changed)

    def zero_changed(self):
        zeroCheck = self.window.zeroCheckbox
        self.exclude_zero = zeroCheck.isChecked()

    def seed_init(self):
        seed = self.window.seedEdit
        seed.setValidator(QRegExpValidator("[1-9][0-9]*"))
        seed.editingFinished.connect(self.seed_changed)

    def seed_changed(self):
        value = self.window.seedEdit.text()
        self.seed = int(value)

    def combo_init(self):
        outCombo = self.window.outputTypeCombo
        outCombo.addItem('Images', userData=PyramidPrinterImage)
        outCombo.addItem('Tikz code', userData=PyramidPrinterTikz)

    def update_pyramid(self):        
        self.pyramid = Pyramid(self.size, ui=self)
        self.imagePrinter = PyramidPrinterImage(self.pyramid)
        self.clean_images()
           
    def init_ui(self,window):
        self.window = window
        self.window.quitButton.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.spinbox_init(window.sizeBox, 
                          value=self.size, 
                          min=self.size_min, 
                          max=self.size_max, 
                          on_change=self.size_changed )
        self.check_size_difficulty()

        self.spinbox_init(window.difficultyBox, 
                          value=self.difficulty, 
                          min=self.difficulty_min, 
                          max=self.difficulty_max,
                          on_change=self.difficulty_changed )
        self.spinbox_init(window.minBox, 
                          value=self.value_min, 
                          min=-1000, 
                          max=self.value_max-1,
                          on_change=self.min_changed )
        self.spinbox_init(window.maxBox, 
                          value=self.value_max, 
                          min=self.value_min+1, 
                          max=1000,
                          on_change=self.max_changed )
        self.window.puzzleButton.clicked.connect(self.generate_puzzle)
        self.window.directoryButton.clicked.connect(self.choose_directory)
        self.window.saveButton.clicked.connect(self.save_puzzle)
        self.progressbar_init()
        self.menus_init()
        
    def menus_init(self):
        entryExit = self.window.actionExit
        entryExit.triggered.connect(QtWidgets.QApplication.instance().quit)
        self.window.actionAbout.setEnabled(False)
        self.window.actionPreferences.setEnabled(False)

    def init_timeline(self):
        # 0.1 sec frame
        self.timeline.setUpdateInterval(10)
        self.timeline.setFrameRange(0, 100)
        self.timeline.frameChanged[int].connect(self.update_progressbar)
        #2**12 * 10 seconds is 11 hours
        self.timeline.setLoopCount(2**15)
        self.timeline.setCurveShape(self.timeline.LinearCurve)

    def update_progressbar(self, frame):
        # animation to make sure ui is not locked
        X = frame*2 - 100
        self.window.progressBar.setInvertedAppearance(X >= 0)
        X = 100 - abs(X)
        self.window.progressBar.setValue(X)
     
    def progressbar_init(self):
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.setInvertedAppearance(False)
        self.window.progressBar.reset()

    def progressbar_stop(self):
        self.timeline.stop()
        self.window.progressBar.setInvertedAppearance(False)
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.setFormat('Click on "Create a puzzle"')
        self.window.progressBar.reset()
        
    def progressbar_run(self):
        self.window.progressBar.setRange(0,100)
        self.window.progressBar.setFormat("Looking…")
        self.window.progressBar.reset()
        self.timeline.start()
        sleep(0.04)
        
    def spinbox_init(self, spin, *, value = 0, min=0, max=1000, step=1, on_change = None):
        spin.setRange(min,max)
        spin.setValue(value)
        if on_change:
            spin.valueChanged.connect(on_change)
        
    def size_changed(self, value):
        self.size = value
        self.update_pyramid()
        self.check_size_difficulty()

    def check_size_difficulty(self):
        if self.size < 5:
            self.window.difficultyBox.setMaximum(3)
        else:
            self.window.difficultyBox.setMaximum(5)
            
    def difficulty_changed(self, value):
        self.difficulty = value
    def min_changed(self, value):
        self.value_min = value
        self.window.maxBox.setMinimum(value+1)
    def max_changed(self, value):
        self.value_max = value
        self.window.minBox.setMaximum(value-1)

    def update_images(self):
        if not self.images:
            return
        
        if 'puzzle' in self.images:
            self.puzzlePix = toqpixmap(self.images['puzzle'])
        if 'solution' in self.images:
            self.solutionPix = toqpixmap(self.images['solution'])
        if 'nopuzzle' in self.images:
            self.puzzlePix = toqpixmap(self.images['nopuzzle'])
            self.solutionPix = toqpixmap(self.images['nopuzzle'])

        self.window.puzzleImageLabel.setPixmap(self.puzzlePix)
        self.window.solutionImageLabel.setPixmap(self.solutionPix)
        
    def generate_puzzle(self):
        # in another thread. That can be long.
        if not self.generating:
            self.generating = True
            self.progressbar_run()  
            self.information("Looking for a puzzle.")
            self.clean_images()
            self.myThread = LookingForPuzzleThread(self)
            self.myThread.finished.connect(self.when_get_puzzle)
            self.myThread.start(QThread.LowPriority)
            self.puzzleButtonText = self.window.puzzleButton.text()
            self.window.puzzleButton.setText("&Cancel")
        else:
            # cancel the running puzzle generation
            self.generating = False
            self.pyramid.cancel = True

    def when_get_puzzle(self):
        if self.pyramid.cancel:
            self.information("Operation cancelled.")
        else:
            self.imagePrinter.print(memory_images=True)
            self.images = self.imagePrinter.get_images()
            self.update_images()

        self.generating = False
        self.window.puzzleButton.setText(self.puzzleButtonText)
        self.progressbar_stop()
        del self.myThread
        
    def information(self, text):
        self.window.informationLabel.setText(str(text))
        
    def clean_images(self):
        self.pyramid.puzzle = {}
        self.pyramid.solution = []
        self.imagePrinter.print(memory_images=True)
        self.images = self.imagePrinter.get_images()
        self.update_images()

    def choose_directory(self):
        dirDialog = QFileDialog()
        # default irectory to "Documents"
        dirDialog.setDirectory(self.output_directory)
        self.output_directory = dirDialog.getExistingDirectory(self.window, "Select Directory")

    def save_puzzle(self):
        combo = self.window.outputTypeCombo
        printerClass = combo.currentData()
        printer = printerClass(self.pyramid)
        param = { 'directory' : self.output_directory,
                 'resolution' : self.resolution,
                 'latex_separator' : self.latex_separator
                }
        printer.print(**param)
