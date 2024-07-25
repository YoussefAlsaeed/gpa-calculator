# GPA Calculator

## Overview

This project is a GPA calculator for FCAI-CU with a modern GUI built using PyQt5. It allows you to add and remove courses, edit course details, and calculate your GPA. The calculator supports both dark and light themes and integrates with Selenium for web scraping to fetch course data.

## Setup

### Prerequisites

**1. Clone the Repository:**
   ```bash
   git clone https://github.com/YoussefAlsaeed/gpa-calculator
   ```
   
**2. Download WebDriver:**
- For Edge: Download the Edge WebDriver from [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
- For Chrome: Download the Chrome WebDriver from [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable).

**3. Configuration:**

- Edit the secrets.json file:

- Replace browser value with "edge" or "chrome" based on your WebDriver.
- Set "webdriver_path" to the path of the downloaded WebDriver executable.
- Update "username" and "password" with your login credentials.

### Running the Application
- For Windows:
 Open `run-calc.bat` by double-clicking it.

- For Linux or macOS:

Open a terminal and run:
```bash
./run-calc.sh
```
