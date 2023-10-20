from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
from datetime import datetime, timezone, timedelta

# Create a new Chrome WebDriver instance
browser = webdriver.Chrome()

# Ask the user for the time input
start_time_input = input("Enter the start time (XX hours): ")
end_time_input = input("Enter the end time (YY hours): ")

# Convert the user input to integers
try:
    start_time = int(start_time_input)
    end_time = int(end_time_input)
except ValueError:
    print("Invalid time input. Please use numeric values for XX and YY.")
    browser.quit()
    exit()

# Create a time zone object for GMT+6 (Central Asia Standard Time)
tz = timezone(timedelta(hours=6))

# Get the current time in the desired time zone
current_time = datetime.now(tz)

# Handle the special case when start time is 23 and end time is 00
if start_time == 23 and end_time == 0:
    start_datetime = current_time.replace(hour=start_time, minute=0, second=0, microsecond=0)
    end_datetime = current_time.replace(hour=end_time, minute=0, second=0, microsecond=0) + timedelta(days=1)
else:
    # Construct the start and end times based on the user input and current date
    start_datetime = current_time.replace(hour=start_time, minute=0, second=0, microsecond=0)
    end_datetime = current_time.replace(hour=end_time, minute=0, second=0, microsecond=0)

# Subtract 6 hours from the start and end times
start_datetime -= timedelta(hours=6)
end_datetime -= timedelta(hours=6)

# Construct the URL with the user-specified time range
url = f"https://loganalyzerdc.mnpspbd.com/app/discover#/view/8111c940-d68e-11ed-b5e6-4555e8b66a47?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'{start_datetime.year}-{start_datetime.month:02d}-{start_datetime.day:02d}T{start_datetime.hour:02d}:00:00.000Z',to:'{end_datetime.year}-{end_datetime.month:02d}-{end_datetime.day:02d}T{end_datetime.hour:02d}:00:00.000Z'))&_a=(columns:!(message),filters:!(),grid:(),hideChart:!f,index:'6d047592-02c4-48ba-bbff-2c6a0a45e9e1',interval:auto,query:(language:kuery,query:'log.file.path%20:%20%22%2Fusr%2Flocal%2Ftomcat%2Flogs%2Fa2p_engine_transactional_iptsp%2FtransactionalCdr.csv%22%20and%20not%20%229000%22'),sort:!(!('@timestamp',desc)))"

browser.get(url)

# Wait briefly for the authentication prompt to appear
time.sleep(5)

# Use pyautogui to type in the username and password
username = "<enter-username>"
password = "<enter-password>"

pyautogui.write(username)
pyautogui.press('tab')
pyautogui.write(password)

# Press Enter to submit the login credentials
pyautogui.press('enter')

# Wait for the Share button to appear and click it
try:
    share_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='euiButtonEmpty__text' and text()='Share']")))
    share_button.click()
except:
    print("Failed to find or click the Share button.")

# Wait for the "CSV Reports" button to appear and click it
try:
    csv_reports_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='euiContextMenuItem__text' and text()='CSV Reports']")))
    csv_reports_button.click()
except:
    print("Failed to find or click the CSV Reports button.")

# Wait for the "Generate CSV" button to appear and click it
try:
    generate_csv_button = WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, "//span[@class='css-1km4ln8-euiButtonDisplayContent' and text()='Generate CSV']")))
    generate_csv_button.click()
except:
    print("Failed to find or click the Generate CSV button.")

# Wait for 15 seconds
time.sleep(15)

# Navigate to the new URL
new_url = "https://loganalyzerdc.mnpspbd.com/app/management/insightsAndAlerting/reporting"
browser.get(new_url)

# Wait for the "Download" button to appear and click it
try:
    download_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test-subj='reportDownloadLink']")))
    download_button.click()
except:
    print("Failed to find or click the Download button.")

# Wait for 5 seconds before closing the browser
time.sleep(5)

# Close the browser
browser.quit()
