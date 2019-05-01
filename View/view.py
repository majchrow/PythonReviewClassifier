#!/usr/bin/env python3

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QLineEdit, QListWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit, QDesktopWidget
from PyQt5.QtCore import QSize

IMAGES_LAYOUTS_PATH = 'images/layouts/'


class Window(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setMinimumSize(QSize(960, 500))
        self.setMaximumSize(QSize(960, 500))
        self.setWindowTitle("Review Classifier")
        self.controller = controller
        self._center()

    def add_layout(self, columns, rows, c_stretch, r_stretch):
        layout = QGridLayout(self)

        for i in range(rows):
            layout.setRowStretch(i, r_stretch)

        for i in range(columns):
            layout.setColumnStretch(i, c_stretch)

        return layout

    def add_pix_map(self, image):
        label = QLabel(self)
        pix_map = QPixmap(image)
        label.setPixmap(pix_map)
        label.resize(pix_map.width(), pix_map.height())
        return label

    def add_text_line(self, color, text):
        text_line = QLineEdit(self)
        text_line.setStyleSheet(color)
        text_line.insert(text)
        return text_line

    def add_text_area(self, color, text):
        text_area = QPlainTextEdit(self)
        text_area.setStyleSheet(color)
        text_area.insertPlainText(text)
        return text_area

    @staticmethod
    def add_button(label, style, connect_function):
        button = QPushButton(label)
        button.setStyleSheet(style)
        button.clicked.connect(connect_function)
        return button

    def _center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())


class StartWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: black")
        self.start_button = Window.add_button('Start', "background-color: white", controller.on_click_start)
        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout(self)
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)

        additional_layout = Window.add_layout(self, 5, 5, 5, 5)

        label = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'main.jpg')

        grid_layout.addWidget(label, 2, 2)

        additional_layout.addWidget(self.start_button, 2, 2)
        grid_layout.addLayout(additional_layout, 2, 2)

        self.setCentralWidget(central_widget)


class MenuWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: white")
        color = "background-color: rgb(141, 194, 210)"
        labels = ('Choose model', 'Classify your review', 'Generate text')
        connect_functions = (controller.on_click_choose, controller.on_click_classify, controller.on_click_generate)
        self.buttons = []
        for i in range(3):
            self.buttons.append(Window.add_button(labels[i], color, connect_functions[i]))
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 5, 5, 5, 5)

        images = ('network.jpeg', 'film.jpg', 'text.png')

        for i in range(3):
            label = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + images[i])
            grid_layout.addWidget(label, 1, i + 1)
            grid_layout.addWidget(self.buttons[i], 2, i+1)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)


class ChooseWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.list_widget_lm = QListWidget()
        self.list_widget_cm = QListWidget()
        self.list_widget_lm.itemClicked.connect(controller.on_click_item_lm)
        self.list_widget_cm.itemClicked.connect(controller.on_click_item_cm)
        self.back_button = Window.add_button("Get back", "background-color: white", controller.on_click_back)
        self.current_lm_model = Window.add_text_line(self, "background-color:white", "")
        self.current_cm_model = Window.add_text_line(self, "background-color:white", "")
        self.init_ui()

    def init_ui(self):
        lm_list = self.controller.get_lm()
        cm_list = self.controller.get_cm()
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 2, 2*len(lm_list)+2*len(cm_list), 10, 10)

        additional_layout_lm = Window.add_layout(self, 2, 4, 10, 10)
        additional_layout_cm = Window.add_layout(self, 2, 4, 10, 10)

        self.list_widget_lm.setStyleSheet("background-color: white")
        self.list_widget_cm.setStyleSheet("background-color: white")

        for i, model in enumerate(lm_list):
            self.list_widget_lm.insertItem(i, model)

        for i, model in enumerate(cm_list):
            self.list_widget_cm.insertItem(i, model)

        additional_layout_cm.addWidget(self.list_widget_cm)
        additional_layout_lm.addWidget(self.list_widget_lm)

        grid_layout.addLayout(additional_layout_lm, 0, 0, 4, 1)
        grid_layout.addLayout(additional_layout_cm, 2, 0, 4, 1)
        grid_layout.addWidget(self.back_button, 0, 1)
        grid_layout.addWidget(self.current_lm_model, 1, 1)
        grid_layout.addWidget(self.current_cm_model, 2, 1)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def lm_c(self):
        self.current_lm_model.setText("1")

    def cm_c(self):
        self.current_cm_model.setText("1")

class GenerateWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.init_ui()

    def init_ui(self):
        pass


class ClassifyWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")

        color = "background-color: white"
        labels = ("Classify", "Get back")
        connect_functions = (controller.on_click_classify, controller.on_click_back)

        self.buttons = []
        for i in range(2):
            self.buttons.append(Window.add_button(labels[i], color, connect_functions[i]))

        self.text_area = Window.add_text_area(self, "background-color: white", "Write your review here.\n")

        self.current_model = Window.add_text_line(self, "background-color:white", controller.get_current_model())

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 3, 1, 5, 5)

        grid_layout.addWidget(self.text_area, 0, 0, 2, 2)
        additional_layout = Window.add_layout(self, 3, 3, 3, 3)

        for i in range(2):
            additional_layout.addWidget(self.buttons[i], i, 1)

        additional_layout.addWidget(self.current_model, 2, 1)

        grid_layout.addLayout(additional_layout, 0, 2)

        central_widget.setLayout(grid_layout)


        self.setCentralWidget(central_widget)


class MessageWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setMinimumSize(QSize(600, 200))
        self.setMaximumSize(QSize(600, 200))
        self.setWindowTitle("Message")
        self.setStyleSheet("background-color: white")
        self.label = QLabel(self)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        grid_layout = Window.add_layout(self, 3, 3, 3, 3)
        central_widget.setLayout(grid_layout)

        self.label.setFont(QFont("Arial", 12, QFont.Black))
        grid_layout.addWidget(self.label, 1, 1)

        self.setCentralWidget(central_widget)