#!/usr/bin/env python3

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtWidgets import QWidget, QPushButton,  QPlainTextEdit, QDesktopWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
import logging

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

    @staticmethod
    def add_layout(columns, rows, c_stretch, r_stretch):
        layout = QGridLayout()

        for i in range(rows):
            layout.setRowStretch(i, r_stretch)

        for i in range(columns):
            layout.setColumnStretch(i, c_stretch)

        return layout

    def add_combo_box(self, items, style):
        box = QComboBox(self)
        box.setEditable(True)
        box.lineEdit().setReadOnly(True)
        box.lineEdit().setAlignment(Qt.AlignCenter)
        for i in items:
            box.addItem(i)
        box.setStyleSheet(style)
        return box

    def add_label(self, color, text, **kwargs):
        label = QLabel(self)
        label.setText(text)
        label.setStyleSheet(color)
        if "font_size" in kwargs.keys():
            font = QFont()
            font.setPointSize(kwargs["font_size"])
            label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        return label

    def add_pix_map(self, image):
        label = QLabel(self)
        pix_map = QPixmap(image)
        label.setPixmap(pix_map)
        label.resize(pix_map.width(), pix_map.height())
        label.setAlignment(Qt.AlignCenter)
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
    """Staring window"""
    def __init__(self, controller):
        logging.info("Initializing starting window")
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: black")
        self.start_button = Window.add_button('START', "background-color: white", controller.on_click_start)
        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)

        additional_layout = Window.add_layout(5, 5, 5, 5)

        label = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'main.jpg')

        grid_layout.addWidget(label, 2, 2)

        additional_layout.addWidget(self.start_button, 2, 2)
        grid_layout.addLayout(additional_layout, 2, 2)

        self.setCentralWidget(central_widget)


class MenuWindow(Window):
    """Menu window"""
    def __init__(self, controller):
        logging.info("Initializing menu window")
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: white")
        color = "background-color: rgb(141, 194, 210)"
        labels = ('Choose models', 'Classify your review', 'Generate text')
        connect_functions = (controller.on_click_choose, controller.on_click_classify, controller.on_click_generate)
        self.buttons = [Window.add_button(labels[i], color, connect_functions[i]) for i in range(3)]
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(5, 5, 5, 5)

        images = ('network.jpeg', 'film.jpg', 'text.png')

        for i in range(3):
            label = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + images[i])
            grid_layout.addWidget(label, 1, i + 1)
            grid_layout.addWidget(self.buttons[i], 2, i+1)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)


class ChooseWindow(Window):
    """Model selector window"""
    def __init__(self, controller):
        logging.info("Initializing model selector window")
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")

        self.lm_list = self.controller.get_all_lm()
        self.clf_list = self.controller.get_all_clf()

        self.combo_box_lm = Window.add_combo_box(self, self.lm_list, "background-color:white")
        self.combo_box_clf = Window.add_combo_box(self, self.clf_list, "background-color:white")

        self.current_lm = Window.add_label(self, "background-color:white", controller.get_current_lm())
        self.current_clf = Window.add_label(self, "background-color:white", controller.get_current_clf())

        self.back_button = Window.add_button("Get back", "background-color: rgb(163, 226, 229)", controller.on_click_back)
        self.apply_clf_button = Window.add_button("Apply", "background-color: rgb(163, 226, 229)",
                                                  controller.on_click_apply_clf)
        self.apply_lm_button = Window.add_button("Apply", "background-color: rgb(163, 226, 229)",
                                                 controller.on_click_apply_lm)

        self.clf_title = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CURRENT MODEL")
        self.lm_title = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CURRENT MODEL")

        self.classifiers = Window.add_label(self, "background-color:rgb(141, 194, 210)", "CLASSIFIERS", font_size=12)
        self.lmodels = Window.add_label(self, "background-color:rgb(141, 194, 210)", "LANGUAGE MODELS", font_size=12)

        self.clf_image = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'decision-making.png')
        self.lm_image = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'discussion.png')

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(5, 10, 10, 10)

        clf_elements = (self.classifiers, self.combo_box_clf, self.apply_clf_button, self.clf_title, self.current_clf)
        lm_elements = (self.lmodels, self.combo_box_lm, self.apply_lm_button, self.lm_title, self.current_lm)

        for i, el in enumerate(clf_elements):
            grid_layout.addWidget(el, i, 1)

        for i, el in enumerate(lm_elements):
            grid_layout.addWidget(el, i, 3)

        grid_layout.addWidget(self.clf_image, 6, 1)
        grid_layout.addWidget(self.lm_image, 6, 3)

        grid_layout.addWidget(self.back_button, 9, 3)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)


class GenerateWindow(Window):
    """Text generator window"""
    def __init__(self, controller):
        logging.info("Initializing text generator window")
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.text_area = Window.add_text_area(self, "background-color: white",
                                              "Write your text here, specify number of words and click \'Generate\'.")

        color = "background-color: rgb(163, 226, 229)"
        labels = ("Cenerate", "Get back")
        connect_functions = (controller.on_click_generate, controller.on_click_back)

        self.buttons = [Window.add_button(labels[i], color, connect_functions[i]) for i in range(2)]

        self.current_model = Window.add_label(self, "background-color:white", controller.get_current_model())
        self.words = Window.add_label(self, "background-color:rgb(141, 194, 210)", "NUMBER OF WORDS")
        self.n_words = Window.add_text_line(self, "background-color:white", "")
        self.model_title = Window.add_label(self, "background-color: rgb(141, 194, 210)", "CURRENT LANGUAGE MODEL")
        self.lm_image = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'discussion.png')

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(3, 1, 5, 5)

        grid_layout.addWidget(self.text_area, 0, 0, 2, 2)
        additional_layout = Window.add_layout(3, 10, 3, 3)

        additional_layout.addWidget(self.lm_image, 0, 1)

        additional_layout.addWidget(self.words, 1, 1)
        additional_layout.addWidget(self.n_words, 2, 1)
        additional_layout.addWidget(self.model_title, 5, 1)
        additional_layout.addWidget(self.current_model, 6, 1)
        additional_layout.addWidget(self.buttons[0], 3, 1)
        additional_layout.addWidget(self.buttons[1], 8, 1)

        grid_layout.addLayout(additional_layout, 0, 2)

        central_widget.setLayout(grid_layout)

        self.setCentralWidget(central_widget)


class ClassifyWindow(Window):
    """Review classifier window"""
    def __init__(self, controller):
        logging.info("Initializing review classifier window")
        Window.__init__(self, controller)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")

        color = "background-color: rgb(163, 226, 229)"
        labels = ("Classify", "Get back")
        connect_functions = (controller.on_click_classify, controller.on_click_back)

        self.buttons = [Window.add_button(labels[i], color, connect_functions[i]) for i in range(2)]

        self.text_area = Window.add_text_area(self, "background-color: white",
                                              "Write your review here and click \'Classify\'.")

        self.current_model = Window.add_label(self, "background-color:white", controller.get_current_model())

        self.model_title = Window.add_label(self, "background-color: rgb(141, 194, 210)", "CURRENT CLASSIFIER")

        self.clf_image = Window.add_pix_map(self, IMAGES_LAYOUTS_PATH + 'decision-making.png')

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid_layout = Window.add_layout(3, 1, 5, 5)

        grid_layout.addWidget(self.text_area, 0, 0, 2, 2)
        additional_layout = Window.add_layout(3, 10, 3, 3)

        additional_layout.addWidget(self.clf_image, 0, 1)
        additional_layout.addWidget(self.buttons[0], 2, 1)

        additional_layout.addWidget(self.model_title, 4, 1)
        additional_layout.addWidget(self.current_model, 5, 1)

        additional_layout.addWidget(self.buttons[1], 9, 1)

        grid_layout.addLayout(additional_layout, 0, 2)

        central_widget.setLayout(grid_layout)

        self.setCentralWidget(central_widget)


class MessageWindow(Window):
    """Message window"""
    def __init__(self, controller):
        logging.info("Initializing message window")
        Window.__init__(self, controller)
        self.setMinimumSize(QSize(600, 200))
        self.setMaximumSize(QSize(600, 200))
        self.setWindowTitle("Message")
        self.setStyleSheet("background-color: white")
        self.label = QLabel(self)
        self.smile = Window.add_pix_map(self, IMAGES_ICON_PATH + 'smile.png')
        self.sad = Window.add_pix_map(self, IMAGES_ICON_PATH + 'sad.png')
        self.grid_layout = Window.add_layout(3, 3, 3, 3)

        self._center()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        central_widget.setLayout(self.grid_layout)

        self.grid_layout.addWidget(self.label, 1, 1)

        self.setCentralWidget(central_widget)
