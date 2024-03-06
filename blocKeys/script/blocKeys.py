"""
****************************************** Blockeys v2.0 ***************************************************************
                                 ________________________________________
                                |                                        |
                                |  Script done by: Pierre-Marie Bavay    |
                                |  Contact email : pierrem.bvy@gmail.com |
                                |________________________________________|

************************************************************************************************************************

"""




from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
import maya.mel as mel
import json
import os


def write_frame_numbers():
    project_data_dir = cmds.workspace(query=True, rd=True)
    file_name = "frame_numbers.json"
    file_path = os.path.join(project_data_dir, file_name)

    current_time = int(cmds.currentTime(query=True))
    frame_numbers = [current_time]

    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json_file.read()
            if data:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    return
            else:
                data = {}
    else:
        data = {}

    if not isinstance(data, dict):
        data = {}

    if not isinstance(data.get("frame_numbers"), list):
        data["frame_numbers"] = []

    print("Data before appending frame numbers:", data)
    data["frame_numbers"].append(frame_numbers)

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

    print("Frame numbers written to:", file_path)


def remove_frame_number(frame_number):
    project_data_dir = cmds.workspace(query=True, rd=True)
    file_name = "frame_numbers.json"
    file_path = os.path.join(project_data_dir, file_name)

    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File not found:", file_path)
        return
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return

    print("Data before removal:", data)

    if "frame_numbers" not in data:
        print("Key 'frame_numbers' not found in JSON data.")
        return

    frame_numbers = data["frame_numbers"]
    if isinstance(frame_numbers, list):
        occurrences = frame_numbers.count([frame_number])
        if occurrences > 0:
            frame_numbers = [fn for fn in frame_numbers if fn != [frame_number]]
            data["frame_numbers"] = frame_numbers
            with open(file_path, "w") as json_file:
                json.dump(data, json_file)
            print(f"Frame number {frame_number} removed {occurrences} time(s) from {file_path}")
        else:
            print(f"Frame number {frame_number} not found in {file_path}")
    else:
        print("Invalid data format for 'frame_numbers'.")

    print("Data after removal:", data)
    return data



class blocKeysWindow(QtWidgets.QWidget):
    def __init__(self):
        super(blocKeysWindow, self).__init__()
        self.setWindowTitle("BlocKeys")
        self.setGeometry(950, 400, 250, 85)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #464646;")

        main_layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        blockingKeys_button = QtWidgets.QPushButton("Blocking Keys")
        blockingKeys_button.clicked.connect(self.blockingKeys)
        blockingKeys_button.setStyleSheet(
            "QPushButton {"
            "   color: #00080a;"
            "   background-color: #e9e0d0;"
            "   min-width: 10em;"
            "   min-height: 2em;"
            "   border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #fff8e3;"
            "}")
        button_layout.addWidget(blockingKeys_button)

        resetKeys_button = QtWidgets.QPushButton("Reset Keys")
        resetKeys_button.clicked.connect(self.resetKeys)
        resetKeys_button.setStyleSheet(
            "QPushButton {"
            "   color: #00080a;"
            "   background-color: #d85d56;"
            "   min-width: 10em;"
            "   min-height: 2em;"
            "   border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #fe6d65;"
            "}")
        button_layout.addWidget(resetKeys_button)
        main_layout.addLayout(button_layout)

        separator_line = QtWidgets.QFrame()
        separator_line.setFrameShape(QtWidgets.QFrame.HLine)
        separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator_line)

        self.custom_frame = QtWidgets.QFrame()
        self.custom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.custom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.custom_frame.setStyleSheet("background-color: transparent;")

        custom_layout = QtWidgets.QHBoxLayout()
        custom_label = QtWidgets.QLabel("Custom Color")
        custom_layout.addWidget(custom_label)

        self.color_square = QtWidgets.QFrame()
        self.color_square.setFixedSize(20, 20)
        self.color_square.setStyleSheet("background-color: red;")
        custom_layout.addWidget(self.color_square)

        self.custom_frame.setLayout(custom_layout)
        self.custom_frame.hide()

        self.option_button = QtWidgets.QPushButton("Options +")
        self.option_button.setStyleSheet(
            "QPushButton {"
            "   color: #00080a;"
            "   background-color: transparent;"
            "   border: none;"
            "   text-align: left;"
            "   padding-left: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: transparent;"
            "}")
        self.option_button.clicked.connect(self.toggleCustomFrame)
        main_layout.addWidget(self.option_button)
        main_layout.addWidget(self.custom_frame)
        self.setLayout(main_layout)
        self.color_square.mousePressEvent = self.chooseCustomColor
        self.initial_height = self.height()


    def blockingKeys(self):

        current_time = int(cmds.currentTime(query=True))
        mel.eval(f"keyframe -time {current_time} -tds 1;")
        write_frame_numbers()


    def resetKeys(self):
        mel.eval("keyframe -tds 0;")

        project_data_dir = cmds.workspace(query=True, rd=True)
        file_name = "frame_numbers.json"
        file_path = os.path.join(project_data_dir, file_name)

        current_time = int(cmds.currentTime(query=True))
        remove_frame_number(current_time)

        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print("File not found:", file_path)
            return
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return

        if "frame_numbers" in data:
            frames = data["frame_numbers"]
            for frame_list in frames:
                for frame in frame_list:
                    mel_command = f"keyframe -time {frame} -tds 1;"
                    cmds.evalDeferred(f"mel.eval(\"{mel_command}\")")
                    print(f"Executed command: {mel_command}")
        else:
            print("No frame numbers found in the data.")


    def toggleCustomFrame(self):
        if self.custom_frame.isVisible():
            self.custom_frame.hide()
            self.setFixedHeight(self.initial_height)
            self.option_button.setText("Options +")
        else:
            self.custom_frame.show()
            self.setFixedHeight(self.height() * 1.5)
            self.option_button.setText("Options -")

    def chooseCustomColor(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                r, g, b = [val * 255 for val in color.getRgbF()[:3]]
                self.color_square.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")

                mel.eval(f"displayRGBColor \"timeSliderTickDrawSpecial\" {r / 255.0} {g / 255.0} {b / 255.0};")


maya_window = blocKeysWindow()
maya_window.show()
