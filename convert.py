import os
import sys
import threading

from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QFileDialog, QLineEdit, QHBoxLayout, QStyle, QCheckBox, QLabel
from PySide6 import QtGui, QtCore

def runNukeScript(args):
    # Set OCIO Config
    os.environ["OCIO"] = "/aces_1.0.1/RATZ_OCIO_config_v001.ocio"

    # Set Nuke startup script (Script sets OCIO as default color management)
    os.environ["NUKE_PATH"] = "/Nuke Startup"

    os.environ["RATZ_ImageInputPath"] = args[0]
    os.environ["RATZ_ImageOutputPath"] = args[1]
    os.environ["RATZ_IsSequence"] = str(args[2])
    os.environ["RATZ_IsSRGB"] = str(args[3])
    os.environ["RATZ_FrameRangeFrom"] = args[4]
    os.environ["RATZ_FrameRangeTo"] = args[5]

    print("Start Nuke init.py Script")

    os.system(' "C:/Program Files/Nuke13.2v1/Nuke13.2.exe" -t R:/00_pipeline/nuke_converter/src/init.py ')

    print("Ending Button callback")

class TestWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convert to ACES")
        self.resize(850,100)

        self.output_path = ""
        self.input_path = ""
        self.isSequence = True
        self.isSRGB = False

        self.create_widgets()
        self.create_layouts()

    def create_layouts(self):
        mainLayout = QVBoxLayout(self)
        # mainLayout.setContentsMargins(0,15,0,0)

        mainLayout.addLayout(self.hbox_input_path)
        mainLayout.addLayout(self.hbox_output_path)
        mainLayout.addLayout(self.isSequenceHBox)
        mainLayout.addLayout(self.isSRGBHBox)
        mainLayout.addLayout(self.rangeHBox)

        mainLayout.addWidget(self.runScriptButton)

        self.setLayout(mainLayout)

    def create_widgets(self):
        self.addInputFileSelect()
        self.addOutputFileSelect()
        self.addOptions()
        self.addRange()
        self.addRunScriptButton()

    def addInputFileSelect(self):
        inputPathLabel = QLabel("Input")
        inputPathLabel.setMinimumWidth(80)

        self.input_path_lineedit = QLineEdit("")
        self.input_path_lineedit.textChanged.connect(lambda: self.changeInputImagePath(self.input_path_lineedit.text()))

        select_file_button = QPushButton()
        select_file_button.setToolTip('Select path to Style Image')

        pixmapi = getattr(QStyle, "SP_DirIcon")
        icon = self.style().standardIcon(pixmapi)
        select_file_button.setIcon(icon)
        select_file_button.clicked.connect(lambda: self.selectInputImagePath())

        self.hbox_input_path = QHBoxLayout()
        self.hbox_input_path.addWidget(inputPathLabel)
        self.hbox_input_path.addWidget(self.input_path_lineedit)
        self.hbox_input_path.addWidget(select_file_button)

    
    def addOutputFileSelect(self):
        outputPathLabel = QLabel("Output")
        outputPathLabel.setMinimumWidth(80)

        self.output_path_lineedit = QLineEdit("")
        self.output_path_lineedit.editingFinished.connect(lambda: self.changeOutputImagePath(self.output_path_lineedit.text()))

        select_file_button = QPushButton()
        select_file_button.setToolTip('Select path to Style Image')

        pixmapi = getattr(QStyle, "SP_DirIcon")
        icon = self.style().standardIcon(pixmapi)
        select_file_button.setIcon(icon)
        select_file_button.clicked.connect(lambda: self.selectOutputImagePath())

        self.hbox_output_path = QHBoxLayout()
        self.hbox_output_path.addWidget(outputPathLabel)
        self.hbox_output_path.addWidget(self.output_path_lineedit)
        self.hbox_output_path.addWidget(select_file_button)
    
    def addOptions(self):
        # Is Sequence
        self.isSequenceCheckbox = QCheckBox()
        self.isSequenceCheckbox.setChecked(True)
        self.isSequenceCheckbox.toggled.connect(lambda: self.setIsSequence(self.isSequenceCheckbox.isChecked()))

        isSequenceLabel = QLabel("Is Sequence?")
        isSequenceLabel.setMaximumWidth(80)

        self.isSequenceHBox = QHBoxLayout()
        self.isSequenceHBox.addWidget(isSequenceLabel)
        self.isSequenceHBox.addWidget(self.isSequenceCheckbox)

        # Is SRGB
        self.isSRGBCheckbox = QCheckBox()
        self.isSRGBCheckbox.toggled.connect(lambda: self.setIsSRGB(self.isSRGBCheckbox.isChecked()))

        isSRGBLabel = QLabel("Is sRGB?")
        isSRGBLabel.setMaximumWidth(80)

        self.isSRGBHBox = QHBoxLayout()
        self.isSRGBHBox.addWidget(isSRGBLabel)
        self.isSRGBHBox.addWidget(self.isSRGBCheckbox)

    def addRange(self):
        fromRangeLabel = QLabel("Frame Range")
        fromRangeLabel.setMinimumWidth(80)
        fromRangeLabel.setMaximumWidth(80)

        # From
        self.from_range_lineedit = QLineEdit("1001")
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 99999)
        self.from_range_lineedit.setValidator(onlyInt)
        self.from_range_lineedit.setMaximumWidth(40)

        seperatorLabel = QLabel(" - ")
        seperatorLabel.setMinimumWidth(12)
        seperatorLabel.setMaximumWidth(12)

        # To
        self.to_range_lineedit = QLineEdit("")
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 99999)
        self.to_range_lineedit.setValidator(onlyInt)
        self.to_range_lineedit.setMaximumWidth(40)

        self.rangeHBox = QHBoxLayout()
        self.rangeHBox.addWidget(fromRangeLabel)
        self.rangeHBox.addWidget(self.from_range_lineedit)
        self.rangeHBox.addWidget(seperatorLabel)
        self.rangeHBox.addWidget(self.to_range_lineedit)
        self.rangeHBox.addStretch(1)


    def toggleRange(self,bool):
        for i in range(self.rangeHBox.count()):
            item = self.rangeHBox.itemAt(i).widget()
            if item:
                if bool:
                    item.show()
                else:
                    item.hide()

    def addRunScriptButton(self):
        self.runScriptButton = QPushButton("Run Nuke Script")
        self.runScriptButton.setToolTip('Run Nuke Script')
        self.runScriptButton.clicked.connect(lambda: self.runThread())

    def selectInputImagePath(self):
        input_path, selected_filter = QFileDialog.getOpenFileName(self, "Select File", "")
        if input_path:
            self.changeInputImagePath(input_path)

    def selectOutputImagePath(self):
        output_path, selected_filter = QFileDialog.getSaveFileName(self, "Select File", "")
        if output_path:
            self.changeOutputImagePath(output_path)

    def changeInputImagePath(self,imagePath):
        imagePath = imagePath.replace("\\", "/")
        self.input_path_lineedit.setText(imagePath)
        self.input_path = imagePath

        newOutputPath = ""
        if(self.isSequence):
            newOutputPath = os.path.splitext(imagePath)[0] + '.mov'
        else:
            newOutputPath = os.path.splitext(imagePath)[0] + '.jpg'

        self.changeOutputImagePath(newOutputPath)

    def changeOutputImagePath(self,imagePath):
        self.output_path_lineedit.setText(imagePath)
        self.output_path = imagePath

    def runThread(self):
        frameRangeFrom = self.from_range_lineedit.text()
        frameRangeTo = self.to_range_lineedit.text()
        
        thread = threading.Thread(target=runNukeScript, args=([self.input_path, self.output_path, self.isSequence, self.isSRGB, frameRangeFrom, frameRangeTo], ))
        thread.start()
        thread.join()
        print("Done")

    # Run Converter on Key pressed
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return: 
            self.runThread()
    
    def setIsSequence(self,value):
        self.isSequence = value
        self.changeInputImagePath(self.input_path)
        if(value):
            self.toggleRange(True)
        else:
            self.toggleRange(False)

    def setIsSRGB(self,value):
        self.isSRGB = value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec()
