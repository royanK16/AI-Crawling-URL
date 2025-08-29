import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_website(website):
    driver = None
    try:
        # Configure Chrome options for headless mode
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        # Use webdriver-manager to automatically handle the ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Launching headless Chrome browser...")
        driver.get(website)
        print("Page Loaded...")
        
        time.sleep(5)
        
        html = driver.page_source
        return html
        
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
    
    finally:
        if driver:
            driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.find("body")
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script in soup(["script", "style", "header"]):
        script.extract()
    
    # Get text and clean it
    text = soup.get_text(separator=",")
    text = ",".join(line.strip() for line in text.splitlines() if line.strip())
    
    return text

def split_dom_content(dom_content, max_length=7000):
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]


