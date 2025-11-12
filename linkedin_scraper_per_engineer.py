import requests
from bs4 import BeautifulSoup
import json
import time
import random

# --------------------------------------------
# CONFIG
# --------------------------------------------
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
MAX_PAGES = 1
JOBS_PER_PAGE = 60
SCRAPING_LIMIT = 10
DELAY_RANGE = (3, 7)  # seconds between requests
OUTPUT_FILE = "EngineerJobs.json"

# List of engineering job positions to search for
positions = [
    "Software%20Engineer",
    "Data%20Engineer",
    "Machine%20Learning%20Engineer",
    "DevOps%20Engineer",
    "Backend%20Engineer",
    "Frontend%20Engineer",
    "Full%20Stack%20Engineer",
    "Cloud%20Engineer",
    "Network%20Engineer",
    "Security%20Engineer",
    "Systems%20Engineer",
    "Site%20Reliability%20Engineer",
    "Embedded%20Systems%20Engineer",
    "Automation%20Engineer",
    "QA%20Engineer",
    "Test%20Automation%20Engineer",
    "Data%20Science%20Engineer",
    "AI%20Engineer",
    "Blockchain%20Engineer",
    "Robotics%20Engineer",
    "Hardware%20Engineer",
    "Electrical%20Engineer",
    "Electronics%20Engineer",
    "Mechanical%20Engineer",
    "Civil%20Engineer",
    "Industrial%20Engineer",
    "Manufacturing%20Engineer",
    "Biomedical%20Engineer",
    "Chemical%20Engineer",
    "Environmental%20Engineer"
]


# --------------------------------------------
# CORE SCRAPING FUNCTIONS
# --------------------------------------------
def retrieve_job_urls(session, job_search_url):
    """Retrieve all job URLs from a LinkedIn job search results page."""
    try:
        response = session.get(job_search_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"⚠️ Failed to retrieve {job_search_url} (HTTP {response.status_code})")
            return []
    except requests.RequestException as e:
        print(f"⚠️ Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_urls = []

    for link in soup.select("a.base-card__full-link"):
        job_url = link.get("href", "").split("?")[0]
        if job_url and job_url not in job_urls:
            job_urls.append(job_url)

    return job_urls


def scrape_job(session, job_url):
    """Extract job details from a LinkedIn job page."""
    try:
        response = session.get(job_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"⚠️ Failed to load job {job_url} (HTTP {response.status_code})")
            return None
    except requests.RequestException as e:
        print(f"⚠️ Request failed for {job_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    def safe_select(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    title = safe_select("h1")
    company_element = soup.select_one("[data-tracking-control-name='public_jobs_topcard-org-name']")
    company_name = company_element.get_text(strip=True) if company_element else None
    company_url = company_element["href"] if company_element and company_element.has_attr("href") else None

    job = {
        "url": job_url,
        "title": title,
        "company": {"name": company_name, "url": company_url},
        "location": safe_select(".topcard__flavor--bullet"),
        "applications": safe_select(".num-applicants__caption"),
        "salary": safe_select(".salary"),
        "description": safe_select(".description__text .show-more-less-html"),
        "criteria": [],
    }

    for li in soup.select(".description__job-criteria-list li"):
        name = li.select_one(".description__job-criteria-subheader")
        value = li.select_one(".description__job-criteria-text")
        if name and value:
            job["criteria"].append({"name": name.get_text(strip=True), "value": value.get_text(strip=True)})

    return job


def scrape_jobs_for_position(session, position):
    """Scrape job listings for a given position title."""
    base_search_url = (
        f"https://www.linkedin.com/jobs/search/?keywords={position}"
        f"&geoId=103736294&trk=public_jobs_jobs-search-bar_search-submit"
    )

    all_jobs = []

    for page in range(MAX_PAGES):
        paginated_url = f"{base_search_url}&start={page * JOBS_PER_PAGE}"
        print(f"🌐 Searching {position.replace('%20', ' ')} — Page {page + 1}/{MAX_PAGES}")

        job_urls = retrieve_job_urls(session, paginated_url)
        if not job_urls:
            print("🚫 No more jobs found.")
            break

        for job_url in job_urls[:SCRAPING_LIMIT]:
            print(f"🔍 Scraping job: {job_url}")
            job_data = scrape_job(session, job_url)
            if job_data:
                job_data["searched_position"] = position.replace("%20", " ")
                all_jobs.append(job_data)

            delay = random.uniform(*DELAY_RANGE)
            print(f"⏱️ Sleeping {delay:.1f}s...")
            time.sleep(delay)

    return all_jobs


# --------------------------------------------
# MAIN EXECUTION
# --------------------------------------------
if __name__ == "__main__":
    session = requests.Session()
    all_jobs = []

    print("🚀 Starting LinkedIn Engineer Job Scraper...\n")

    for pos in positions:
        print(f"\n==============================")
        print(f"🔎 Searching for {pos.replace('%20', ' ')} jobs...")
        print(f"==============================")

        jobs = scrape_jobs_for_position(session, pos)
        all_jobs.extend(jobs)

        delay = random.uniform(*DELAY_RANGE)
        print(f"🌙 Cooling down for {delay:.1f}s before next position...\n")
        time.sleep(delay)

    print(f"\n💾 Exporting {len(all_jobs)} scraped jobs to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=4, ensure_ascii=False)
    print("✅ Done.")
