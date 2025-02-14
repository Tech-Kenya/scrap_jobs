import pytest
from scrape_jobs import initialize_driver, extract_job_details
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Mock HTML for testing
MOCK_HTML = """
<div class="company-jobs">
    <div class="jobs-list">
        <div class="w-full">
            <a class="font-bold" href="/jobs/123">Software Engineer</a>
            <span class="font-bold">Example Startup</span>
            <span class="capitalize">San Francisco, CA</span>
            <span class="text-gray-500">$120,000 - $150,000</span>
        </div>
    </div>
</div>
"""

@pytest.fixture
def mock_driver():
    # Initialize a headless Chrome driver for testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_extract_job_details():
    # Test the job details extraction function
    soup = BeautifulSoup(MOCK_HTML, "html.parser")
    job = soup.find("div", class_="w-full")
    job_data = extract_job_details(job)

    assert job_data["title"] == "Software Engineer"
    assert job_data["company"] == "Example Startup"
    assert job_data["location"] == "San Francisco, CA"
    assert job_data["salary"] == "$120,000 - $150,000"
    assert job_data["application_url"] == "https://www.workatastartup.com/jobs/123"

def test_initialize_driver(mock_driver):
    # Test if the driver initializes correctly
    assert mock_driver is not None