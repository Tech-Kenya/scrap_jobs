from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
import time

# Function to initialize WebDriver in headless mode
def initialize_driver():
    print("🚀 Initializing Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # New headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service()  # Update with your ChromeDriver path if needed
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ WebDriver initialized.")
    return driver

# Function to scrape job data
def scrape_jobs(driver):
    print("🌍 Navigating to job listings page...")
    url = "https://www.workatastartup.com/jobs"
    driver.get(url)

    try:
        # Wait until job listings load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "company-jobs"))
        )
        print("✅ Job listings page loaded successfully.")

        # Parse page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs_container = soup.find('div', class_='company-jobs')

        if not jobs_container:
            print("⚠️ No jobs container found. Exiting.")
            return []

        jobs_list = jobs_container.find('div', class_='jobs-list')
        if not jobs_list:
            print("⚠️ No jobs list found. Exiting.")
            return []

        jobs = jobs_list.find_all('div', class_='w-full')
        job_list = []

        print(f"🔎 Found {len(jobs)} job postings. Extracting details...")

        for index, job in enumerate(jobs, start=1):
            title_element = job.find('a', class_='font-bold')
            company_element = job.find('span', class_='font-bold')
            location_element = job.find('span', class_='capitalize')
            salary_element = job.find('span', class_='text-gray-500')
            job_link = title_element['href'] if title_element and title_element.has_attr('href') else None

            title = title_element.text.strip() if title_element else "No Title"
            company = company_element.text.strip() if company_element else "No Company"
            location = location_element.text.strip() if location_element else "No Location"
            salary = salary_element.text.strip() if salary_element else "Not Specified"

            # Ensure the correct application URL
            application_url = job_link if job_link.startswith("http") else f"https://www.workatastartup.com{job_link}"

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "application_url": application_url
            }

            job_list.append(job_data)

            # Print progress update
            print(f"✅ [{index}/{len(jobs)}] {title} at {company} - {location}")

        return job_list

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return []

    finally:
        driver.quit()
        print("🛑 WebDriver session closed.")

# Function to save data to a JSON file
def save_to_file(job_data):
    try:
        with open("jobs.json", "w") as file:
            json.dump(job_data, file, indent=4)
        print(f"📂 Data saved successfully! ({len(job_data)} jobs) → jobs.json")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# Main function
def main():
    print("🚀 Starting job scraping process...")
    driver = initialize_driver()
    job_data = scrape_jobs(driver)

    if job_data:
        save_to_file(job_data)
    else:
        print("⚠️ No job data found. Exiting.")

if __name__ == "__main__":
    main()
