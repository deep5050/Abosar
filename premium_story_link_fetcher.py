from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def fetch_links():
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Enable complete loading
        driver.set_page_load_timeout(30)
        
        all_story_links = set()
        base_url = "https://www.anandabazar.com"

        for page_num in range(1, 8):
            url = f"https://www.anandabazar.com/rabibashoriyo/page-{page_num}"
            print(f"Scraping page: {url}")
            
            try:
                driver.get(url)
                time.sleep(3) # Wait for content to load
                
                # Find all links
                a_tags = driver.find_elements(By.TAG_NAME, "a")
                
                page_links = 0
                for a in a_tags:
                    href = a.get_attribute('href')
                    if href and "short-story" in href:
                        # Ensure full URL
                        if href.startswith("/"):
                            href = base_url + href
                        
                        all_story_links.add(href)
                        page_links += 1
                
                print(f"Found {page_links} stories on page {page_num}")
                
            except Exception as e:
                print(f"Error scraping page {page_num}: {e}")

        # Write to file
        output_file = "premium_stories_url"
        with open(output_file, 'w', encoding='utf-8') as f:
            for link in sorted(all_story_links):
                f.write(link + "\n")
                
        print(f"Successfully wrote {len(all_story_links)} unique story links to {output_file}")

    except Exception as e:
        print(f"Fatal error: {e}")
        if 'driver' in locals():
            driver.quit()
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    fetch_links()
