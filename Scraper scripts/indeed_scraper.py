import time
import random
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

import requests

PAGES_TO_SCRAPE = 5
BASE_URL = "https://www.indeed.com/jobs?l=california&start="

def new_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(100)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    return driver

if __name__ == "__main__":
    print("Starting Indeed job URL retrieval...")

    print("Retrieving job URLs from Indeed...") 
    jobs = []
    previous_length = 0
    for page in range(PAGES_TO_SCRAPE):
        print(f"Scraping page {page + 1} of {PAGES_TO_SCRAPE}...")
        
        time.sleep(random.uniform(2, 5))  # Random delay between 2 to 5 seconds
        
        url = BASE_URL + str(page * 10) if page > 0 else BASE_URL
        driver = new_driver()
        driver.get(url) 
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        job_results = soup.find("div", id="mosaic-jobResults")
        job_cards = job_results.find_all("a", class_="jcs-JobTitle")
        for job_card in job_cards:
            job_url = "https://www.indeed.com" + job_card.get("href")
            
            job_driver = new_driver()
            job_driver.get(job_url)
            job_soup = BeautifulSoup(job_driver.page_source, "html.parser")
            
            if job_soup.find("h1", class_="jobsearch-JobInfoHeader-title") is None:
                print(f"Skipping job URL (no title found): {job_url}")
                continue

            title = job_soup.find("h1", class_="jobsearch-JobInfoHeader-title").get_text().strip()
            
            if job_soup.find("div", {"data-testid": "inlineHeader-companyName"}) is None:
                print(f"Skipping job URL (no company found): {job_url}")
                continue

            company_element = job_soup.find("div", {"data-testid": "inlineHeader-companyName"})
            company_name = company_element.get_text().strip()
            
            if company_element.find("a") is None:
                print(f"Skipping job URL (no company URL found): {job_url}")
                continue
            
            company_url = company_element.find("a")["href"]
            
            if job_soup.find("div", {"data-testid": "inlineHeader-companyLocation"}) is None:
                print(f"Skipping job URL (no location found): {job_url}")
                continue
            
            location = job_soup.find("div", {"data-testid": "inlineHeader-companyLocation"}).get_text().strip()
            
            salary_element = job_soup.find("div", id="salaryInfoAndJobType")
            salary = salary_element.find("span").get_text().strip() if salary_element and salary_element.find("span") else None
            
            description = job_soup.find("div", id="jobDescriptionText").get_text().strip() if job_soup.find("div", id="jobDescriptionText") else None
            
            criteria = {}
            job_details = job_soup.find("div", id="mosaic-vjJobDetails")
            if job_details:
                details = job_details.find_all("div", attrs={"aria-label": True})

                for detail in details:
                    label = detail.get("aria-label").strip()
                    content_text = detail.get_text(separator=" ", strip=True)
                    criteria[label] = content_text
            
            job = {
                "url": job_url,
                "title": title,
                "company": {
                    "name": company_name,
                    "url": company_url
                },
                "location": location,
            #     "applications": applicants,
                "salary": salary,
                "description": description,
                "criteria": criteria
            }
            
            jobs.append(job)
            
        print(f"Found {len(jobs) - previous_length} valid job URLs on page {page + 1}.")
        previous_length = len(jobs)

        driver.quit()
        
    with open("indeed_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
