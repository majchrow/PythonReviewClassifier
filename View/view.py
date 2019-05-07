#!/usr/bin/env python3

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QLineEdit, QListWidget, QComboBox
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit, QDesktopWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

IMAGES_LAYOUTS_PATH = 'images/layouts/'
IMAGES_ICON_PATH = 'images/icons/'


class Window(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setMinimumSize(QSize(960, 500))
        self.setMaximumSize(QSize(960, 500))
        self.setWindowTitle("Review Classifier")
        self.controller = controller
        self._center()
        self.setWindowIcon(QIcon(IMAGES_ICON_PATH + 'window_icon.png'))

    def add_layout(self, columns, rows, c_stretch, r_stretch):
        layout = QGridLayout(self)

        for i in range(rows):
            layout.setRowStretch(i, r_stretch)

        for i in range(columns):
            layout.setColumnStretch(i, c_stretch)

        return layout

    def add_combo_box(self, items, style):
        box = QComboBox(self)
        for i in items:
            box.addItem(i)
        box.setStyleSheet(style)
        return box

    def add_label(self, color, text):
        label = QLabel(self)
        label.setText(text)
        label.setStyleSheet(color)
        label.setAlignment(Qt.AlignCenter)
        return label

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
        self.start_button = Window.add_button('START', "background-color: white", controller.on_click_start)
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
        self.lm_list = self.controller.get_lm()
        self.clf_list = self.controller.get_cm()
        self.combo_box_lm = Window.add_combo_box(self, self.lm_list, "background-color:white")
        self.combo_box_clf = Window.add_combo_box(self, self.clf_list, "background-color:white")
        self.back_button = Window.add_button("Get back", "background-color: white", controller.on_click_back)
        self.current_lm = Window.add_label(self, "background-color:white", "")
        self.current_clf = Window.add_label(self, "background-color:white", "")
        self.apply_clf_button = Window.add_button("Apply", "background-color: white", controller.on_click_apply_clf)
        self.apply_lm_button = Window.add_button("Apply", "background-color: white", controller.on_click_apply_lm)
        self.clf_title = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CURRENT CLASSIFIER")
        self.lm_title = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CURRENT LANGUAGE MODEL")
        self.classifiers = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CLASSIFIERS")
        self.lmodels = Window.add_label(self, "background-color:rgb(141, 194, 210)", "LANGUAGE MODELS")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 7, 10, 10, 10)

        grid_layout.addWidget(self.classifiers, 0, 2)
        grid_layout.addWidget(self.combo_box_clf, 1, 2)
        grid_layout.addWidget(self.apply_clf_button, 2, 2)
        grid_layout.addWidget(self.lmodels, 3, 2)
        grid_layout.addWidget(self.combo_box_lm, 4, 2)
        grid_layout.addWidget(self.apply_lm_button, 5, 2)
        grid_layout.addWidget(self.back_button, 7, 2)
        grid_layout.addWidget(self.clf_title, 1, 4)
        grid_layout.addWidget(self.current_clf, 2, 4)
        grid_layout.addWidget(self.lm_title, 4, 4)
        grid_layout.addWidget(self.current_lm, 5, 4)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)


class GenerateWindow(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.text_area = Window.add_text_area(self, "background-color: white", "Write your text here. \nRemember to specify number of words to gnenerate.\n")

        color = "background-color: white"
        labels = ("Cenerate", "Get back")
        connect_functions = (controller.on_click_generate, controller.on_click_back)

        self.buttons = []
        for i in range(2):
            self.buttons.append(Window.add_button(labels[i], color, connect_functions[i]))

        self.current_model = Window.add_label(self, "background-color:white", controller.get_current_model())
        self.words = Window.add_label(self, "background-color:rgb(141, 194, 210)", "NUMBER OF WORDS")
        self.n_words = Window.add_text_line(self, "background-color:white", "")
        self.model_title = Window.add_label(self, "background-color: rgb(141, 194, 210)", "CURRENT LANGUAGE MODEL")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 3, 1, 5, 5)

        grid_layout.addWidget(self.text_area, 0, 0, 2, 2)
        additional_layout = Window.add_layout(self, 3, 10, 3, 3)

        for i in range(2):
            additional_layout.addWidget(self.buttons[i], i, 1)

        additional_layout.addWidget(self.model_title, 3, 1)
        additional_layout.addWidget(self.current_model, 4, 1)
        additional_layout.addWidget(self.words, 5, 1)
        additional_layout.addWidget(self.n_words, 6, 1)

        grid_layout.addLayout(additional_layout, 0, 2)

        central_widget.setLayout(grid_layout)

        self.setCentralWidget(central_widget)


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

        self.current_model = Window.add_label(self, "background-color:white", controller.get_current_model())

        self.model_title = Window.add_label(self, "background-color: rgb(141, 194, 210)", "CURRENT CLASSIFIER")

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(self, 3, 1, 5, 5)

        grid_layout.addWidget(self.text_area, 0, 0, 2, 2)
        additional_layout = Window.add_layout(self, 3, 10, 3, 3)

        for i in range(2):
            additional_layout.addWidget(self.buttons[i], i, 1)

        additional_layout.addWidget(self.model_title, 3, 1)
        additional_layout.addWidget(self.current_model, 4, 1)

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
        self._center()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        grid_layout = Window.add_layout(self, 3, 3, 3, 3)
        central_widget.setLayout(grid_layout)

        self.label.setFont(QFont("Arial", 12, QFont.Black))
        grid_layout.addWidget(self.label, 1, 1)

        self.setCentralWidget(central_widget)
