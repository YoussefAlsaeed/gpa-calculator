import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load secrets from secrets.json
with open('secrets.json', 'r') as f:
    secrets = json.load(f)

browser = secrets['browser']
webdriver_path = secrets['webdriver_path']
username = secrets['username']
password = secrets['password']
login_url = secrets['login_url']
courses_url = secrets['courses_url']

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the WebDriver based on the browser type
if browser == 'chrome':
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
elif browser == 'edge':
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")

    service = EdgeService(webdriver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
else:
    raise ValueError("Unsupported browser specified in secrets.json. Use 'chrome' or 'edge'.")

try:
    # Navigate to the main page
    logging.info("Navigating to the login page.")
    driver.get(login_url)

    # Wait for the "Account" menu and click on it
    logging.info("Clicking on 'Account' menu.")
    account_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jhitranslate='global.menu.account.main']/span[text()='Account']"))
    )
    account_menu.click()

    # Click on "Sign In" under the Account menu
    logging.info("Clicking on 'Sign in'.")
    sign_in = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jhitranslate='global.menu.account.login']/span[text()='Sign in']"))
    )
    sign_in.click()

    # Wait for the login form to appear and enter username and password
    logging.info("Entering login credentials.")
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    # Submit the login form
    password_input.send_keys(Keys.RETURN)

    # Wait for the login to complete by checking for the presence of the table
    logging.info("Waiting for login to complete and checking for the table.")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-bordered.table-sm"))
    )
    logging.info("Login successful and table found.")

    # Navigate to the protected page
    logging.info("Navigating to the courses page.")
    driver.get(courses_url)

    # Wait for the table with the class "table table-striped col-md-12" on the courses page
    logging.info("Waiting for the courses page to load and checking for the table.")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-striped.col-md-12"))
    )
    logging.info("Courses page loaded and table found.")
    
    page_source = driver.page_source

    # Save the HTML content to a file
    with open("full_courses_page.html", "w", encoding="utf-8") as file:
        file.write(page_source)
    logging.info("Page saved as full_courses_page.html.")

finally:
    # Clean up
    driver.quit()
    logging.info("WebDriver quit.")
