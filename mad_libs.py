import sys
import os
from docx import Document
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget, QTextEdit, QButtonGroup
from PyQt6.QtGui import QFont, QTextCursor, QAction,QTextCharFormat, QKeySequence
from functools import partial
import inputs_file

#custom window subclass for custom prompts
class CustomWindow(QMainWindow):
    submitClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mad Libs")
        self.input_text = ""
        self.custom_text_input = QLineEdit()
        self.custom_label = QLabel("Enter your custom prompt: ")
        self.custom_button = QPushButton("Done")
        self.custom_button.clicked.connect(self.close_window)

        layout = QGridLayout()
        layout.addWidget(self.custom_label,0,1,1,1)
        layout.addWidget(self.custom_text_input,0,2,1,22)
        layout.addWidget(self.custom_button,1,0,10,22)
        
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
    
    def keyPressEvent(self, event):
        '''
        Function to look for the enter key press while filling in custom prompt
        arg: event enter key press - 16777220
        '''
        if event.key() == 16777220:
            if self.custom_text_input.text() != "":
                self.close_window()
            else:
                pass

    def close_window(self):
        '''
        Function to close opened window and send input text back to main window
        Text is the custom prompt entered by the user. If text is blank, nothing happens
        '''
        if self.custom_text_input.text() != "":
            self.submitClicked.emit(self.custom_text_input.text())
            self.close()
        else:
            pass

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prompt_counter = 0
        self.added_fill_ins = [] # holds list of prompts for cycling later
        self.setWindowTitle("Mad Libs")
        self.buttons = []

        # file menu options. Currently just save but want to include open
        mainMenu = self.menuBar()
        saveFile = QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        changeImage = QAction("Change &Background", self)
        changeImage.setShortcut("Ctrl+B")
        changeImage.setStatusTip('Change Background')
        changeImage.triggered.connect(self.change_image)
        # add menu options
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(saveFile)
        fileMenu.addAction(changeImage)

        # add all the buttons dynamically based on the dictionary list
        self.button_list = inputs_file.inputs
        prompt_group = QButtonGroup() # group buttons together for simplicity
        i = 0
        for key, value in self.button_list.items():
            self.buttons.append(QPushButton(value, self))
            self.buttons[i].clicked.connect(partial(self.add_a_prompt, prompt=value))
            self.buttons[i].setShortcut(QKeySequence('Ctrl+' + key))
            prompt_group.addButton(self.buttons[i])
            i = i + 1
        num_buttons_layout = int(len(prompt_group.buttons())/2)

        # Theme text and labels
        self.theme_text = QLineEdit()
        self.theme_label = QLabel("Theme:")
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.theme_label.setStyleSheet("color: white;background-color: black")
        self.theme_label.setFixedWidth(45)
        self.theme_label.setFixedHeight(20)

        # main text box and formatting for prompts
        self.full_text = QTextEdit()
        self.cursor = self.full_text.textCursor()
        self.bold_fmt = QTextCharFormat()
        self.bold_fmt.setFontWeight(700)

        # labels for showing prompt count and prompt to fill in
        self.fill_in_label = QLabel()
        self.fill_in_label.setStyleSheet("color: white;background-color: black")
        self.fill_in_label.hide()
        self.prompt_counter_label = QLabel("Number of Prompts: ")
        self.prompt_counter_label.setStyleSheet("color: white;background-color: black")

        # done button to begin the fill in the blank process
        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.start_fill_in_the_blank)

        # prompt editor buttons
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_fill_in_the_blank)
        self.next_button.setEnabled(False)
        self.next_button.hide()
        self.input_text = QLineEdit()
        self.input_text.setReadOnly(True)
        self.input_text.hide()

        # layout adds all items
        layout = QGridLayout()
        layout.addWidget(self.theme_label,0,1,1,1)
        layout.addWidget(self.theme_text,0,2,1,22)#, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.full_text,1,0,10,22)
        layout.addWidget(self.prompt_counter_label,11,0,alignment=Qt.AlignmentFlag.AlignLeft)
        # add buttons based on the list 
        for i in range(num_buttons_layout):
            layout.addWidget(prompt_group.buttons()[i],i+1,23, alignment=Qt.AlignmentFlag.AlignLeft)
        for i in range(num_buttons_layout):
            layout.addWidget(prompt_group.buttons()[i+num_buttons_layout],i+1,24, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.done_button,12,0,1,1)
        layout.addWidget(self.fill_in_label,14,0,alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.input_text,14,1,1,15)
        layout.addWidget(self.next_button,14,16,1,2,alignment=Qt.AlignmentFlag.AlignLeft)

        #self.button_noun.clicked.connect(lambda:self.editor.build_text(self.current_text))
        #self.input_text.textChanged.connect(self.text_holder)
        # .setFixedSize() you can also call .setMinimumSize() and .setMaximumSize()
        #self.label.setFont(myFont)

        # Set the central widget of the Window.
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    ###################################################
    # function definitions
    ###################################################
    
    def keyPressEvent(self, event):
        '''
        Function to look for the enter key press while filling in prompts to move to the next fill in the blank
        arg: event enter key press - 16777220
        '''
        if event.key() == 16777220:
            if self.next_button.isEnabled() and self.input_text.text() != "":
                self.next_fill_in_the_blank()
            else:
                pass
    
    def file_save(self):
        '''
        Function to save file. Currently saves as text file with no formatting. 
        Want to update to PDF or docx saving
        '''
        document = Document()
        document.add_heading(self.theme_text.text(), level=1)
        document.add_paragraph(self.full_text.toPlainText())
        name = QFileDialog.getSaveFileName(self, 'Save File')
        document.save(name[0] + '.docx')

    def change_image(self):
        '''
        Function to allow user to change the background image based on selecting a file
        '''
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            imageName = os.path.basename(imagePath)
            self.setStyleSheet("MainWindow { border-image: url(" + "backgrounds/" + imageName + "); background-repeat: no-repeat; background-position: center}")

    def custom_prompt_window(self):
        '''
        Function to open a new window when the custom prompt is selected. The window allows the user to fill in a custom prompt
        '''
        self.sub_window = CustomWindow()
        self.sub_window.submitClicked.connect(self.on_sub_window_confirm)
        self.sub_window.show()
    
    def on_sub_window_confirm(self, prompt):
        '''
        Function to fill in custom prompt received from custom_prompt_window
        arg: prompt - str - custom prompt
        '''
        self.add_a_prompt(prompt)

    def add_a_prompt(self, prompt):
        '''
        function to add a prompt which is based on the button clicked
        args: prompt - str -text of button pressed
        '''
        if prompt=="Custom":
            self.custom_prompt_window()
        else:
            self.cursor.insertText(prompt,self.bold_fmt)
            self.full_text.setFontWeight(QFont.Weight.Normal) # change font back to normal

            self.added_fill_ins.append(prompt)
            self.prompt_counter_label.setText("Number of Prompts: " + str(len(self.added_fill_ins)))
            self.full_text.setFocus()
    
    def update_text_with_prompt(self, prompt):
        '''
        function to update the overall text with the input text after clicking next
        args: prompt - str - text of next prompt in list of prompts
        '''
        self.new_prompt_text = self.input_text.text()
        self.current_text = self.full_text.toPlainText()
        prompt_loc = self.current_text.find(prompt) # find the first instance of the prompt
        if prompt_loc >= 0:
            # move cursor to prompt location, then select and replace the text
            self.cursor.setPosition(prompt_loc, QTextCursor.MoveMode.MoveAnchor)
            self.cursor.movePosition(QTextCursor.MoveOperation.Right,QTextCursor.MoveMode.KeepAnchor,len(prompt))
            self.cursor.insertText(self.new_prompt_text,self.bold_fmt)
        self.input_text.setText("")
        self.input_text.setFocus()

    def start_fill_in_the_blank(self):
        '''
        function to start filling in the blank prompt and then update the text after clicking next
        '''
        if len(self.added_fill_ins) == 0:
            # error label
            self.input_text.show()
            self.input_text.setText("Enter a Prompt first!")
            pass
        else:
            self.next_button.setEnabled(True)
            self.input_text.setReadOnly(False)
            self.fill_in_label.show()
            self.input_text.show()
            self.input_text.setText("")
            self.next_button.show()
            self.full_text.setReadOnly(True)
            self.fill_in_label.setText("Enter a " + self.added_fill_ins[self.prompt_counter] + ":")
            self.input_text.setFocus()
        
    def next_fill_in_the_blank(self):
        '''
        function to continue filling in prompts as user clicks next. Cycles through prompts added via clicks
        Button is disabled until user clicks Done and then is enabled. Button will disable again after end of prompts is reached
        '''
        self.update_text_with_prompt(self.added_fill_ins[self.prompt_counter])
        self.prompt_counter = self.prompt_counter + 1
        if self.prompt_counter >= len(self.added_fill_ins):
            self.next_button.setEnabled(False)
            self.fill_in_label.setText("ALL DONE!")
        else:
            self.fill_in_label.setText("Enter a " + self.added_fill_ins[self.prompt_counter] + ":")

stylesheet_main = """
        MainWindow {
        border-image: url("backgrounds/default.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

app = QApplication(sys.argv)
app.setStyleSheet(stylesheet_main) # background image
window = MainWindow()
window.show()

app.exec()
