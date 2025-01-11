from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Set up WebDriver
s = Service("D:/VS Code/web scraping/Selenium/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Open LinkedIn and log in
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
driver.maximize_window()
time.sleep(4)

# Log in credentials
username = driver.find_element(By.XPATH, '''//input[@id='username']''')
username.send_keys("Provide your Username here")
time.sleep(2)

password = driver.find_element(By.XPATH, '''//input[@id='password']''')
password.send_keys("Provide your Password here")
time.sleep(2)

sign_in = driver.find_element(By.XPATH, '''//button[@class='btn__primary--large from__button--floating' and @aria-label='Sign in']''')
sign_in.click()
time.sleep(3)

# Search for jobs
search = driver.find_element(By.XPATH, '''//input[@aria-label ='Search']''')
search.send_keys('', Keys.ENTER)
time.sleep(4)

jobs = driver.find_element(By.XPATH, '''//*[@id="search-reusables__filters-bar"]/ul/li[4]/button''')
jobs.click()
time.sleep(4)

# Enter job title and location
skill = driver.find_element(By.XPATH, '''/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div/input[1]''')
skill.send_keys("Marketing Data Analyst")
time.sleep(3)

location = driver.find_element(By.XPATH, '''/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]''')
location.clear()
location.send_keys("Berlin")
time.sleep(3)

search2 = driver.find_element(By.XPATH, '''/html/body/div[6]/header/div/div/div/div[2]/button[1]''')
search2.click()
time.sleep(3)

# Collect job data
ljob_title = []
ljob_location = []
ljob_type = []
ljob_description = []

# Iterate through the first 3 pages
for j in range(1, 5):
    # Navigate to the desired page
    try:
        page_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {j}']")
        page_button.click()
        time.sleep(5)
    except:
        print(f"Page {j} button not found.")
        continue

    # Fetch job elements again after navigating
    job_block = driver.find_elements(By.XPATH, '''//ul[@class="yuYSJSfXWBGNVCKRVlUYgsEAgaJlGqUCS"]/li''')
    print(f"Number of jobs on page {j}: {len(job_block)}")

    # Scroll through each job block
    for job in job_block:
        driver.execute_script("arguments[0].scrollIntoView();", job)
        time.sleep(2)

    # Click each job link and extract details
    job_links = driver.find_elements(By.XPATH, "//ul[@class='yuYSJSfXWBGNVCKRVlUYgsEAgaJlGqUCS']/li/div/div/div[1]/div/div[2]/div[1]/a")
    for link in job_links:
        try:
            link.click()
            time.sleep(3)
            
            # Extract job details
            job_title = driver.find_element(By.XPATH, "//h1[@class='t-24 t-bold inline']").text
            job_location = driver.find_element(By.XPATH, "//div[@class='t-black--light mt2']/span").text
            job_type = driver.find_element(By.XPATH, "//div[@class='job-details-preferences-and-skills__pill']/span").text
            job_description = driver.find_element(By.XPATH, "//div[@class='mt4']/p").text

            # Append data to respective lists
            ljob_title.append(job_title)
            ljob_location.append(job_location)
            ljob_type.append(job_type)
            ljob_description.append(job_description)
        
        except Exception as e:
            print(f"Error extracting job details: {e}")
            continue

# Create a DataFrame from the collected data
data = {
    'job_title': ljob_title,
    'job_location': ljob_location,
    'job_type': ljob_type,
    'job_description': ljob_description
}
df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv("linkedin_scrape.csv", index=False)

# Close the driver
driver.quit()