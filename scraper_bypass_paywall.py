from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time, datetime
import json
import requests
import os

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

# Set up ChromeDriver service
try:
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Enable Network domain
    driver.execute_cdp_cmd('Network.enable', {})
    
    # Block the paywall script
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        'urls': ['*paywall-v2.js*', '*paywall*'] 
    })
    
    # Set headers
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Referer': 'https://www.google.com/'}})
except Exception as e:
    print(f"Failed to initialize ChromeDriver: {e}")
    exit(1)

def simulate_human_interaction(driver):
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
    except Exception as e:
        print(f"Interaction error: {e}")

def write_metadata(object, base_path="./metadata/rabibasariya"):
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    metadata = {}
    metadata['url'] = object["url"]
    metadata['author'] = object["author"]
    metadata['crawl_date'] = date_time_str

    safe_name = object["name"].replace(' ', '-')
    safe_author = object["author"].replace(' ', '-')
    
    # Sanitize naming
    safe_name = "".join([c for c in safe_name if c.isalnum() or c in ('-','_')])
    safe_author = "".join([c for c in safe_author if c.isalnum() or c in ('-','_')])

    output_file_path = f'{base_path}/{safe_name}-{safe_author}.json'
    
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile, ensure_ascii=False, indent=4)
        print(f"Metadata written to {output_file_path}")

def write_story(object, base_image_path="./metadata/images/rabibasariya", base_story_path="./stories/rabibasariya"):
    if not os.path.exists(base_image_path):
        os.makedirs(base_image_path, exist_ok=True)
    if not os.path.exists(base_story_path):
        os.makedirs(base_story_path, exist_ok=True)

    print(f'{object["name"]}: Writing story')
    
    safe_name = object["name"].replace(' ', '-')
    safe_author = object["author"].replace(' ', '-')
    # Sanitize naming
    safe_name = "".join([c for c in safe_name if c.isalnum() or c in ('-','_')])
    safe_author = "".join([c for c in safe_author if c.isalnum() or c in ('-','_')])
    
    image_filename = f"{safe_name}-{safe_author}.jpg"
    image_outfile = os.path.join(base_image_path, image_filename)
    
    if object["image"]:
        try:
            response = requests.get(object["image"])
            if response.status_code == 200:
                with open(image_outfile, 'wb') as f:
                    f.write(response.content)
                print(f'{object["name"]}: Image downloaded to {image_outfile}')
            else:
                print('Failed to download image (status code check)')
        except Exception as e:
            print(f"Failed to download image: {e}")
    else:
        print("No image URL found")

    # Relative path for markdown
    # Assuming the markdown file is in ./stories/rabibasariya/
    # and image is in ./metadata/images/rabibasariya/
    # Relative path should be ../../metadata/images/rabibasariya/filename
    
    image_rel_path = f"../../{base_image_path}/{image_filename}"
    
    image_section = f'<div align=center> <img src="{image_rel_path}" align="center"></div>'
    name_section = f'<h1 align=center>{object["name"]}</h1>'
    author_section = f'<h2 align=center>{object["author"]}</h2>'
    story_section = object["text"]

    markdown_content = f'{image_section}<br>{name_section}\n{author_section}<br>\n\n{story_section}'
    
    markdown_outfile = os.path.join(base_story_path, f"{safe_name}-{safe_author}.md")

    with open(markdown_outfile, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Story written to {markdown_outfile}")

def fetch_story(driver, url):
    try:
        print(f"Navigating to {url}")
        driver.get(url)

        # Wait for body
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("Dumping page source for debugging...")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            
        simulate_human_interaction(driver)
        
        # Try to find the content
        # Using existing selectors from previous codebase
        
        img_src = ""
        try:
            leadimgbox_div = driver.find_element(By.XPATH, "//div[contains(@class, 'leadimgbox')]")
            img_element = leadimgbox_div.find_element(By.TAG_NAME, "img")
            img_src = img_element.get_attribute('src')
        except Exception as e:
            print(f"Could not find image: {e}")

        title = "Unknown Title"
        try:
            # Try multiple selectors for title
            h1_elements = driver.find_elements(By.TAG_NAME, "h1")
            for h1 in h1_elements:
                if h1.text.strip():
                    title = h1.text.strip()
                    break
        except Exception as e:
            print(f"Could not find title: {e}")

        author = "Unknown Author"
        try:
            # Try finding author
            # selector: //h4[@class='bynowtxt']
            author_element = driver.find_element(By.XPATH, "//h4[contains(@class, 'bynowtxt')]")
            if author_element.text.strip():
                author = author_element.text.strip()
        except Exception as e:
            print(f"Could not find author with primary selector: {e}")
            try:
                # Fallback
                 editor_div = driver.find_element(By.CLASS_NAME, "autherndntbox")
                 author = editor_div.find_element(By.TAG_NAME, "h4").text.strip()
            except Exception as e2:
                 print(f"Could not find author with fallback: {e2}")

        p_texts = ""
        try:
             # story content
             # selector: #articlebox p
            content_div = driver.find_element(By.ID, "articlebox")
            p_elements = content_div.find_elements(By.TAG_NAME, "p")
            
            print(f"Found {len(p_elements)} paragraphs.")
            
            for p in p_elements:
                text = p.text.strip()
                if text:
                    p_texts += text + "\n\n"
                    
            if not p_texts:
                print("Warning: No text found in articlebox.")

        except Exception as e:
            print(f"Could not find content: {e}")
            try:
                # Fallback to outerbox
                content_div = driver.find_element(By.ID, "outerboxarticlebox")
                p_elements = content_div.find_elements(By.TAG_NAME, "p")
                for p in p_elements:
                    text = p.text.strip()
                    if text:
                        p_texts += text + "\n\n"
            except Exception as e2:
                print(f"Could not find content in outerbox: {e2}")

        print(f"Extracted: {title} by {author}")
        
        obj = {
            "url": url,
            "image": img_src,
            "name": title,
            "author": author,
            "text": p_texts
        }
        
        write_metadata(obj)
        write_story(obj)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = "https://www.anandabazar.com/rabibashoriyo/bengali-short-story-authored-by-somja-das-prnt/cid/1654192"
    # cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{target_url}"
    # print(f"Attempting source: {cache_url}")
    fetch_story(driver, target_url)
