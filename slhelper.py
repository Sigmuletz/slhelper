import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import json
from pywinauto import Application,mouse
import win32api

# https://doc.qt.io/qt-6/widget-classes.html#the-widget-classes

data_file = "commandLab.json"
app = Application(backend="win32").connect(found_index=0, class_name="CASCADIA_HOSTING_WINDOW_CLASS", timeout=10)
cmd_window = app.window(found_index=0, class_name="CASCADIA_HOSTING_WINDOW_CLASS")

@QtCore.Slot()
def buttonTermial(command):
    x, y = win32api.GetCursorPos()
    cmd_window.type_keys(command, with_spaces=True)
    mouse.move([x,y])

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        buttons = []
        layouts = []
        groups = []
        texts = []
        splits = []
        
        # Load JSON data from a file
        with open(data_file, 'r') as file:
            data_json = json.load(file)
            
        layouts.append( QtWidgets.QVBoxLayout(self,alignment=QtCore.Qt.AlignTop))
        aaa = QtWidgets.QLabel("Hello World3", alignment=QtCore.Qt.AlignCenter)
        # layouts[0].addWidget(aaa)
        
        for key, value in data_json.items():
            # print(f"Key: {key}, Value: {value}")
            if "group" in key or "items" in key:
                if "group" in key:
                    # Add only for groups
                    print("Creating a group: ",key)
                    groups.append( QtWidgets.QGroupBox(title=value["title"]))  
                    layouts.append(QtWidgets.QVBoxLayout(alignment=QtCore.Qt.AlignTop))
                    groups[-1].setLayout(layouts[-1])
                    ## Add the box to the layout       
                    layouts[0].addWidget(groups[-1])
                    
                ## Check each item from the group or items
                for item in value["elements"]:
                    print(item)
                    if item["type"] == "button":
                        buttons.append(QtWidgets.QPushButton(item["title"]))
                        buttons[-1].clicked.connect(lambda _, p=item["command"]: buttonTermial(p))
                        if "group" in key:
                            layouts[-1].addWidget(buttons[-1])
                        else: 
                            layouts[0].addWidget(buttons[-1])
                    if item["type"] == "label":
                        texts.append(QtWidgets.QLabel(item["title"], alignment=QtCore.Qt.AlignCenter))
                        if "group" in key:
                            layouts[-1].addWidget(texts[-1])
                        else: 
                            layouts[0].addWidget(texts[-1])
                    if item["type"] == "split":       
                        splits.append(QtWidgets.QSplitter())
                        if "group" in key:
                            layouts[-1].addWidget(splits[-1])
                        else: 
                            layouts[0].addWidget(splits[-1])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(200, 600)
    widget.show()
    
    sys.exit(app.exec()) 