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
import re  # For cleaning data

# ----- CONFIGURATION -----
OUTPUT_FILE = "remote_ict_jobs.json"  # File to save results
SEARCH_TERMS = ["ICT", "Information Technology", "Software", "Developer", "Engineer", "Programming", "Cybersecurity"] # Keywords for filtering
# ----- END CONFIGURATION -----

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

def clean_text(text):
    """Cleans the text to remove unwanted characters."""
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# Function to scrape job data
def scrape_jobs(driver, search_terms): # Added search_terms parameter
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

            title = clean_text(title_element.text.strip()) if title_element else "No Title"
            company = clean_text(company_element.text.strip()) if company_element else "No Company"
            location = clean_text(location_element.text.strip()) if location_element else "No Location"
            salary = clean_text(salary_element.text.strip()) if salary_element else "Not Specified"

            # Ensure the correct application URL
            application_url = job_link if job_link.startswith("http") else f"https://www.workatastartup.com{job_link}"

            # Filter by keywords *before* creating the job_data dictionary
            if any(term.lower() in title.lower() or term.lower() in company.lower() for term in search_terms):
                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "link": application_url, # Changed application_url to link for consistency
                    "source": "workatastartup.com" #Added the source
                }

                job_list.append(job_data)

                # Print progress update
                print(f"✅ [{index}/{len(jobs)}] {title} at {company} - {location}")
            else:
                 print(f"⏩ [{index}/{len(jobs)}] {title} at {company} - {location} (Skipped - Keyword Filter)")

        return job_list

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return []

    finally:
        driver.quit()
        print("🛑 WebDriver session closed.")

# Function to save data to a JSON file, appends to existing file
def save_to_file(job_data, filename): #Added filename parameter
    try:
        # Load existing data, if the file exists
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = [] #Start with an empty list if JSON is corrupted
        else:
            existing_data = []

        # Append new job data to existing data
        all_data = existing_data + job_data

        with open(filename, "w", encoding="utf-8") as file:  # Corrected encoding
            json.dump(all_data, file, indent=4, ensure_ascii=False) # Added ensure_ascii

        print(f"📂 Data saved successfully! ({len(job_data)} jobs) → {filename}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# Main function
def main():
    print("🚀 Starting job scraping process...")
    driver = initialize_driver()
    job_data = scrape_jobs(driver, SEARCH_TERMS) # Pass search terms to scrape_jobs

    if job_data:
        save_to_file(job_data, OUTPUT_FILE) #Pass filename to save_to_file
    else:
        print("⚠️ No job data found. Exiting.")

if __name__ == "__main__":
    main()