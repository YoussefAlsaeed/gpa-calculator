import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLabel, QWidget,
    QInputDialog, QMessageBox, QComboBox, QHBoxLayout, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup

# Define the GPA mapping
grade_to_gpa = {
    "A+": 4.0,
    "A": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "C+": 2.7,
    "C": 2.4,
    "D+": 2.2,
    "D": 2.0,
    "F": 0.0
}

# Load the table HTML content from the file
with open("courses_table.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")
table = soup.find("table", class_="table table-striped col-md-12")

# Extract data from table rows
courses = []
for row in table.find("tbody").find_all("tr"):
    columns = row.find_all("td")
    if len(columns) < 7:
        continue  # Skip rows that do not have enough columns
    try:
        code = columns[0].get_text(strip=True)
        name = columns[1].get_text(strip=True)
        credits = int(columns[3].get_text(strip=True))
        grade = columns[6].get_text(strip=True)
    except ValueError:
        continue  # Skip rows where credits are not valid
    if grade in ["Con", "0", ""] or grade not in grade_to_gpa:
        continue  # Skip invalid grades
    courses.append({
        'Name': name,
        'Credits': credits,
        'Grade': grade
    })


class GPACalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GPA Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Credits', 'Grade', ''])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget)

        self.populate_table()

        self.table_widget.cellDoubleClicked.connect(self.edit_cell)

        # Add course button
        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.add_course)
        self.layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update GPA")
        self.update_button.clicked.connect(self.calculate_gpa)
        self.layout.addWidget(self.update_button)

        self.gpa_label = QLabel("Total GPA: 0.00")
        self.gpa_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.gpa_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.gpa_label)

        self.toggle_button = QPushButton("Toggle Light/Dark Mode")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.dark_mode = False
        self.apply_light_mode()
        self.calculate_gpa()

    def populate_table(self):
        self.table_widget.setRowCount(len(courses))
        for row, course in enumerate(courses):
            self.table_widget.setItem(row, 0, QTableWidgetItem(course['Name']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(course['Credits'])))
            self.table_widget.setItem(row, 2, QTableWidgetItem(course['Grade']))

            remove_button = QPushButton("X")
            remove_button.clicked.connect(lambda _, r=row: self.remove_course(r))
            self.table_widget.setCellWidget(row, 3, remove_button)

    def edit_cell(self, row, column):
        if column == 1:  # Credits column
            current_value = self.table_widget.item(row, column).text()
            new_value, ok = QInputDialog.getItem(self, "Edit Credits", "Select new credits value:", ["0", "2", "3", "6"], current=0, editable=False)
            if ok and new_value:
                self.table_widget.setItem(row, column, QTableWidgetItem(new_value))
                self.update_courses()
                self.calculate_gpa()
        elif column == 2:  # Grade column
            current_value = self.table_widget.item(row, column).text()
            new_value, ok = QInputDialog.getItem(self, "Edit Grade", "Select new grade value:", list(grade_to_gpa.keys()), current=0, editable=False)
            if ok and new_value:
                self.table_widget.setItem(row, column, QTableWidgetItem(new_value))
                self.update_courses()
                self.calculate_gpa()
        else:  # Other columns
            old_value = self.table_widget.item(row, column).text()
            new_value, ok = QInputDialog.getText(self, "Edit Value", f"Edit value for {self.table_widget.horizontalHeaderItem(column).text()}:", text=old_value)
            if ok and new_value:
                self.table_widget.setItem(row, column, QTableWidgetItem(new_value))
                self.update_courses()
                self.calculate_gpa()

    def add_course(self):
        name, ok = QInputDialog.getText(self, "Add Course", "Enter course name:")
        if not ok or not name:
            return
        credits, ok = QInputDialog.getItem(self, "Add Course", "Select credits value:", ["0", "2", "3", "6"], current=0, editable=False)
        if not ok or not credits:
            return
        grade, ok = QInputDialog.getItem(self, "Add Course", "Select grade value:", list(grade_to_gpa.keys()), current=0, editable=False)
        if not ok or not grade:
            return

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(credits))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(grade))

        remove_button = QPushButton("X")
        remove_button.clicked.connect(lambda _, r=row_position: self.remove_course(r))
        self.table_widget.setCellWidget(row_position, 3, remove_button)

        self.update_courses()
        self.calculate_gpa()

    def remove_course(self, row):
        self.table_widget.removeRow(row)
        self.update_courses()
        self.calculate_gpa()

    def update_courses(self):
        global courses
        courses = []
        for row in range(self.table_widget.rowCount()):
            name = self.table_widget.item(row, 0).text()
            credits = self.table_widget.item(row, 1).text()
            grade = self.table_widget.item(row, 2).text()
            if grade in ["Con", "0", ""] or grade not in grade_to_gpa:
                continue  # Skip invalid grades
            courses.append({
                'Name': name,
                'Credits': int(credits),
                'Grade': grade
            })

    def calculate_gpa(self):
        total_credits = 0
        total_points = 0
        for course in courses:
            try:
                credits = int(course['Credits'])
                grade = course['Grade']
                if grade in ["Con", "0", ""] or grade not in grade_to_gpa:
                    continue  # Skip invalid grades
                gpa_points = grade_to_gpa.get(grade, 0.0)
                total_credits += credits
                total_points += credits * gpa_points
            except ValueError:
                continue  # Skip rows where credits are not valid
        if total_credits > 0:
            gpa = total_points / total_credits
        else:
            gpa = 0.0
        self.gpa_label.setText(f"Total GPA: {gpa:.2f}")

    def toggle_mode(self):
        if self.dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
        self.dark_mode = not self.dark_mode

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QTableWidget {
                background-color: #252526;
                color: #D4D4D4;
                gridline-color: #3C3C3C;
            }
            QTableWidget::item {
                border: 1px solid #3C3C3C;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3C3C3C;
                color: #D4D4D4;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color
                #005B9E;
            }
            QLabel {
                color: #D4D4D4;
            }
        """)

    def apply_light_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QTableWidget {
                background-color: #F0F0F0;
                color: black;
                gridline-color: lightgray;
            }
            QTableWidget::item {
                border: 1px solid lightgray;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: lightgray;
                color: black;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #005B9E;
            }
            QLabel {
                color: black;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPACalculator()
    window.show()
    sys.exit(app.exec_())