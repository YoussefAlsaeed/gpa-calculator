import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the table HTML content from the file
with open("courses_table.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")
table = soup.find("table", class_="table table-striped col-md-12")

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

# Initialize variables for GPA calculation
total_credits = 0
total_points = 0

# Extract data from table rows
for row in table.find("tbody").find_all("tr"):
    columns = row.find_all("td")
    
    if len(columns) < 7:
        continue  # Skip rows that do not have enough columns

    # Extract course name, credits, and grade
    course_name = columns[1].get_text(strip=True)
    try:
        credits = int(columns[3].get_text(strip=True))
        grade = columns[6].get_text(strip=True)
    except ValueError:
        continue  # Skip rows where credits are not valid

    # Check if grade is valid (i.e., not "Con", 0, or empty)
    if grade in ["Con", "0", ""] or grade not in grade_to_gpa:
        logging.info(f"Skipping course: {course_name} with invalid grade: {grade}")
        continue  # Skip invalid grades
    
    # Convert grade to GPA points
    gpa_points = grade_to_gpa.get(grade, 0.0)
    
    # Log course name and grade
    logging.info(f"Course: {course_name}, Grade: {grade}, Credits: {credits}, GPA Points: {gpa_points}")

    # Update total credits and points
    total_credits += credits
    total_points += credits * gpa_points

# Calculate GPA
if total_credits > 0:
    gpa = total_points / total_credits
else:
    gpa = 0.0

logging.info(f"Total Credits: {total_credits}")
logging.info(f"Total GPA: {gpa:.2f}")
