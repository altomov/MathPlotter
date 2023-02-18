from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton


class AddLineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Line")
        self.setFixedSize(300, 150)

        start_point_label = QLabel("Start Point:")
        self.start_point_edit = QLineEdit()

        end_point_label = QLabel("Start Point:")
        self.end_point_edit = QLineEdit()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout = QGridLayout(self)

        layout.addWidget(start_point_label, 0, 0)
        layout.addWidget(self.start_point_edit, 0, 1)

        layout.addWidget(end_point_label, 1, 0)
        layout.addWidget(self.end_point_edit, 1, 1)

        layout.addWidget(ok_button, 2, 0)
        layout.addWidget(cancel_button, 2, 1)

        self.setLayout(layout)

    def get_values(self):
        return self.start_point_edit.text(), self.end_point_edit.text()
