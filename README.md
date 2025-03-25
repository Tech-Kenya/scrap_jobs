# Job Scraper

This Python script scrapes job listings from [Work at a Startup](https://www.workatastartup.com/jobs) and saves the data to a JSON file. It uses Selenium for web scraping and BeautifulSoup for parsing HTML.

## Prerequisites

Before running the script, ensure you have the following installed:

1. **Python 3.8+**: Download and install Python from [python.org](https://www.python.org/).
2. **ChromeDriver**: Download the version of ChromeDriver that matches your Chrome browser version from [here](https://sites.google.com/chromium.org/driver/).
3. **Environment Variables**: Create a `.env` file to store your ChromeDriver path (optional).

## Installation

1. Clone this repository or download the script:

   ```bash
   git clone https://github.com/Tech-Kenya/scrap_jobs.git
   cd python_scrap_jobs
   ```

2. Create a virtual environment and install all dependecies:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

   ##### pip might be slow, checkout uv (<https://docs.astral.sh/uv/getting-started/installation/>)
<!-- 3. Create a `.env` file in the root directory and add the following:
    ```env
    CHROMEDRIVER_PATH=/path/to/chromedriver
    ``` -->
4. Run the script:

    ```bash
    python main.py
    ```

5. Run streamlit app:

    ```bash
    streamlit run jobs.py
    ```

5. The script will scrape the job listings and save the data to a JSON file in the `remote_ict_jobs.json` file.

## TODO

- [ ] Add support for other job listing websites.
- [ ] Improve the data extraction process.
- [ ] Add support for sending the data to an API/database.
