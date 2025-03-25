import streamlit as st
import json

# Configuration
JOB_DATA_FILE = "jobs.json"  # Same as the scrapper's output file
PAGE_TITLE = "Remote ICT Job Board"
PAGE_ICON = ":computer:"  # Emojis are supported

# --- Streamlit App ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(PAGE_TITLE)


@st.cache_data  # Cache the data to avoid reloading on every interaction
def load_job_data(filename):
    """Loads job data from the JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(
            f"Error: Job data file '{filename}' not found. Run the scrapper first."
        )
        return None  # or return []
    except json.JSONDecodeError:
        st.error(
            f"Error: Invalid JSON format in '{filename}'. Check the scrapper's output."
        )
        return None
    except Exception as e:
        st.error(f"Error loading job data: {e}")
        return None


def display_jobs(jobs):
    """Displays the job listings in a user-friendly format."""
    if not jobs:
        st.info("No jobs found.  Try running the scrapper to populate the data.")
        return

    for job in jobs:
        with st.container():  # Creates a distinct, visually separable job listing
            st.subheader(job["title"])
            st.write(f"**Company:** {job['company']}")
            st.write(f"**Source:** {job['source']}")  # Added source for clarity
            st.write(f"[Apply Now]({job['link']})")  # Creates a clickable link
            st.markdown("---")  # Adds a horizontal line between jobs


def filter_jobs(jobs, search_term):
    """Filters jobs based on a search term."""
    if not search_term:
        return jobs  # Return all jobs if no search term is provided

    filtered_jobs = [
        job
        for job in jobs
        if search_term.lower() in job["title"].lower()
        or search_term.lower() in job["company"].lower()
    ]
    return filtered_jobs


def main():
    """Main function to run the Streamlit app."""
    jobs = load_job_data(JOB_DATA_FILE)

    if jobs is None:  # Handle case where data loading failed.  Critically important.
        return  # Stop the app if there's no data

    # Sidebar for search
    with st.sidebar:
        st.header("Filter Jobs")
        search_term = st.text_input("Search by title or company:", "")
        st.markdown("---")
        st.info(
            "This app displays remote ICT jobs scraped from various websites.  Run the scrapper.py script to update the data."
        )

    # Filter and display jobs
    filtered_jobs = filter_jobs(jobs, search_term)
    display_jobs(filtered_jobs)


if __name__ == "__main__":
    main()
