from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QDialog, QGridLayout


class AddPointDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(300, 150)
        self.setWindowTitle("Add new point")

        x_label = QLabel("X:")
        self.x_input = QLineEdit()

        y_label = QLabel("Y:")
        self.y_input = QLineEdit()

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_input, 0, 1)

        layout.addWidget(x_label, 1, 0)
        layout.addWidget(self.x_input, 1, 1)

        layout.addWidget(y_label, 2, 0)
        layout.addWidget(self.y_input, 2, 1)

        layout.addWidget(ok_button, 3, 0)
        layout.addWidget(cancel_button, 3, 1)

        self.setLayout(layout)

    def get_values(self):
        x = self.x_input.text()
        y = self.y_input.text()
        name = self.name_input.text()
        return x, y, name
