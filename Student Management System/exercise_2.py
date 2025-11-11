import sys

from PyQt6.QtWidgets import QComboBox, QWidget, QApplication, QLabel, QLineEdit, QPushButton, QGridLayout


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # Create Widgets
        distance_label = QLabel("Distance (km):")
        self.distance_line_edit = QLineEdit()
        date_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Speed")
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("Output:")

        self.combo = QComboBox()

        # Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.combo.addItems(['Metric (km)', 'Imperial (m)'])

        self.setLayout(grid)

    def calculate_speed(self) -> None:
        # Decide whether to use Metric or Imperial
        multiplier: float = 1
        metric: str = "mph"
        if self.combo.currentText() == 'Metric (km)':
            # multiplier = 1
            metric = "km/h"
        if self.combo.currentText() == 'Imperial (m)':
            multiplier = 0.621371
            # metric = "mph"

        # Calculate (Distance * multiplier) / speed
        speed: float = (float(self.distance_line_edit.text()) * multiplier) / float(self.time_line_edit.text())
        speed = round(speed, 4)

        # Return to the output label
        self.output_label.setText(f"The average speed is: {speed} in {metric}")
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = SpeedCalculator()
    calc.show()
    sys.exit(app.exec())
