from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton

class AddFunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add function")
        self.resize(300, 150)

        define_function_label = QLabel("y = ")
        self.function_label_input = QLineEdit()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout = QGridLayout(self)

        layout.addWidget(define_function_label, 0, 0)
        layout.addWidget(self.function_label_input, 0, 1)

        layout.addWidget(ok_button, 1, 0)
        layout.addWidget(cancel_button, 1, 1)

        self.setLayout(layout)

    def get_values(self):
        return self.function_label_input.text()