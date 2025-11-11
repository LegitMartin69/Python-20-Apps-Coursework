import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # Create Widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()
        date_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.date_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("Output:")

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3,0,1,2)

        self.setLayout(grid)
        pass

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.date_line_edit.text()
        print(date_of_birth)

        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = AgeCalculator()
    calc.show()
    sys.exit(app.exec())
