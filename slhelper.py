import sys
import random
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot
import json
from pywinauto import Application,mouse
import win32api
import re

# https://doc.qt.io/qt-6/widget-classes.html#the-widget-classes
# https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
#       "command":"kubectl get pods -A | grep {VK_LCONTROL down}v{VK_LCONTROL up}{ENTER}"
#       "command":"kubectl get pods -A | grep {grep_pod}{ENTER}"


data_file = "commandLab.json"
app = Application(backend="win32").connect(found_index=0, class_name="CASCADIA_HOSTING_WINDOW_CLASS", timeout=10)
cmd_window = app.window(found_index=0, class_name="CASCADIA_HOSTING_WINDOW_CLASS")

pages = []
buttons = []
layouts = []
groups = []
texts = []
splits = []
combos = []
lineedits = []
        
def split_string(input_string):
    # Regular expression pattern to match words inside {} and outside {}
    pattern = r'\s*\{.*?\}\s*|[^\{\}\s]+|\s+'
    # Find all matches of the pattern
    matches = re.findall(pattern, input_string)
    return matches

# def split_at_placeholder(s, placeholder="{ENTER}"):
#     # Find the index of the first occurrence of the placeholder
#     index = s.find(placeholder)
    
#     if index == -1:
#         # Placeholder not found, return the original string and an empty string
#         return s, ''
    
#     # Split the string into two parts
#     part1 = s[:index]
#     part2 = s[index:]  # Include the placeholder in the second part
    
#     return part1, part2

    
@Slot()
def buttonTermial(command):
    x, y = win32api.GetCursorPos()
    try:
        # print(command)
        # print(f"variables: {env} and {tenant}")
        new_command = ""
        parts = split_string(command)
        for part in parts:
            try:
                #replace with global variable
                new_command += part.format_map(globals())
            except:
                #keep special variable - for key codes
                new_command += part
        command = new_command
        # print(command)
    except NameError:
        print("Variables missing.. ",command)
    # cmd_window.type_keys(command, with_spaces=True)
    cmd_window.type_keys(command, with_spaces=True)
    mouse.move([x,y])
    
@Slot()
def comboBoxVariable(name,value):
    globals()[name] = value.currentText()

@Slot()
def lineEditVariable(name,value):
    globals()[name] = value.text()
    
@Slot()
def searchCommands(onPage,searchText): 
    searchText = searchText.text()
    
    for x in buttons:
        if onPage.isAncestorOf(x):
            if searchText in x.text():
                x.show()
            else:
                x.hide()

    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create a QTabWidget
        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Load JSON data from a file
        with open(data_file, 'r') as file:
            data_json = json.load(file)
        
        for page_key, page_value in data_json.items():
            # print(f"Key: {key}, Value: {value}")
            if "page" in page_key:
                pages.append(QtWidgets.QWidget())
                layouts.append( QtWidgets.QVBoxLayout(self,alignment=Qt.AlignTop))
                page_layout = layouts[-1]
                pages[-1].setLayout(page_layout)
                self.tab_widget.addTab(pages[-1], page_value["title"])    
                # adding the top search lineedit
                lineedits.append(QtWidgets.QLineEdit("Search"))
                lineedits[-1].textChanged.connect(lambda _, p=pages[-1],b=lineedits[-1]:searchCommands(p,b))
                page_layout.addWidget(lineedits[-1])                       

            for key, value in page_value["elements"].items():
                if "group" in key or "items" in key:
                    if "group" in key:
                        # Add only for groups
                        # print("Creating a group: ",key)
                        groups.append(QtWidgets.QGroupBox(title=value["title"]))  
                        layouts.append(QtWidgets.QVBoxLayout(alignment=Qt.AlignTop))
                        groups[-1].setLayout(layouts[-1])
                        ## Add the box to the layout       
                        page_layout.addWidget(groups[-1])
                        
                    ## Check each item from the group or items
                    for item in value["elements"]:
                        # print(item)
                        if item["type"] == "button":
                            buttons.append(QtWidgets.QPushButton(item["title"]))
                            buttons[-1].clicked.connect(lambda _, p=item["command"]: buttonTermial(p))
                            if "group" in key:
                                layouts[-1].addWidget(buttons[-1])
                            else: 
                                page_layout.addWidget(buttons[-1])
                        if item["type"] == "label":
                            texts.append(QtWidgets.QLabel(item["title"], alignment=Qt.AlignCenter))
                            if "group" in key:
                                layouts[-1].addWidget(texts[-1])
                            else: 
                                page_layout.addWidget(texts[-1])
                        if item["type"] == "split":       
                            splits.append(QtWidgets.QSplitter())
                            if "group" in key:
                                layouts[-1].addWidget(splits[-1])
                            else: 
                                page_layout.addWidget(splits[-1])
                        if item["type"] == "lineedit":       
                            lineedits.append(QtWidgets.QLineEdit(item["name"]))
                            lineEditVariable(item["name"],lineedits[-1])
                            lineedits[-1].textChanged.connect(lambda _, p=item["name"], c=lineedits[-1]: lineEditVariable(p,c ))                            
                            if "group" in key:
                                layouts[-1].addWidget(lineedits[-1])
                            else: 
                                page_layout.addWidget(lineedits[-1])                                
                        if item["type"] == "combobox":       
                            combos.append(QtWidgets.QComboBox())
                            for x in item["values"]:
                                combos[-1].addItem(x)
                            comboBoxVariable(item["name"],combos[-1]) # to initialize
                            combos[-1].currentIndexChanged.connect(lambda _, p=item["name"], c=combos[-1]: comboBoxVariable(p,c ))
                            if "group" in key:
                                layouts[-1].addWidget(combos[-1])
                            else: 
                                page_layout.addWidget(combos[-1])                                

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.setWindowTitle("S'Little Helper")
    window.resize(200, 800)
    window.show()

    # Execute the application
    sys.exit(app.exec())

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])

#     widget = MyWidget()
#     widget.resize(200, 600)
#     widget.show()
    
#     sys.exit(app.exec()) 