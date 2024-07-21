from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
chrome_options.add_argument("--incognito")  # Open in incognito mode
chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

# Path to ChromeDriver
chrome_driver_path = "./chromedriver-linux64/chromedriver"

# Set up ChromeDriver service
service = ChromeService(executable_path="./chromedriver-linux64/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to simulate human-like interactions
def simulate_human_interaction(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)

# URL of the webpage to scrape
# url = "https://www.anandabazar.com//rabibashoriyo/"
url = "https://www.anandabazar.com/rabibashoriyo/bengali-short-story-by-binita-roychowdhury/cid/1463869"

def write_metadata(object):
    # Create a datetime object for the current date and time
    now = datetime.datetime.now()
    # Convert the datetime object to a string with the desired format
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%d-%m-%Y")

    metadata = {}
    metadata['url'] = object["url"]
    metadata['author'] = object["author"]
    metadata['crawl_date'] = date_time_str

    output_file_path = f'./metadata/rabibasariya/{object["name"]}-{object["author"]}.json'
    output_file_path = output_file_path.replace(' ', '-')
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile, ensure_ascii=False)  

def write_story(object):
    print(f'{object["name"]}: Writing story')
    # download image 
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    
    image_outfile = f"metadata/images/rabibasariya/{object['name']}-{object['author']}.jpg"
    image_outfile = image_outfile.replace(' ', '-')
    response = requests.get(object["image"])
    if response.status_code == 200:
        # Open a file in binary mode and write the response content to it
        with open(image_outfile, 'wb') as f:
            f.write(response.content)
            print(f'{object["name"]}: Image downloaded')
    else:
        print('Failed to download image')
        
    image_section = f'<div align=center> <img src="../../{image_outfile}" align="center"></div>'
    name_section = f'<h1 align=center>{object["name"]}</h1>'
    author_section = f'<h2 align=center>{object["author"]}</h2>'
    story_section = object["text"]
    # print(type(story_section))
    # story_section = "\n".join(story_section)
    # # print(story_section)

    markdown_content = f'{image_section}<br>{name_section}\n{author_section}<br>\n\n{story_section}'
    markdown_outfile = f'./stories/rabibasariya/{object["name"]}-{object["author"]}.md'
    markdown_outfile = markdown_outfile.replace(" ", '-')

    # if not already scraped
    if not os.path.exists(markdown_outfile):
        with open(markdown_outfile, 'w') as f:
            f.write(markdown_content)

        ## append to README
        with open('rabibasariya', "a") as f:
            f.write(f"\n[ {object['name']} - {object['author']} ]({markdown_outfile})")
        print(f'{object["name"]}: Wrinting story')



def fetch_a_story(driver,url):
    url = ""
    with open("url",'r') as f:
        url = f.read()
    
    try:
        # Open the webpage
        driver.get(url)

        # Wait for the page to load and the necessary element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Simulate human interactions
        simulate_human_interaction(driver)

        # Locate the div with the specific class
        leadimgbox_div = driver.find_element(By.XPATH, "//div[@class='leadimgbox mt-24']")

        # Locate the img element within the div
        img_element = leadimgbox_div.find_element(By.XPATH, ".//img[@fetchpriority='high']")

        # Get the src attribute of the img element
        img_src = img_element.get_attribute('src')

        print(img_src)

        # name
        content_div = driver.find_element(By.XPATH, "//div[@class='articletbox mt-32']")
        h1_element = content_div.find_element(By.XPATH, ".//h1[@class='mt-8']")
        print(f"name: {h1_element.text}")

        # editor
        editor_div = driver.find_element(By.XPATH, "//div[@class='editbox df']")
        h5_element = editor_div.find_element(By.XPATH, ".//h5[@class='betellips betvl-1']")
        print(f"author: {h5_element.text}")

        # story
        story_div = driver.find_element(By.XPATH, "//div[@class='contentbox' and @id='contentbox']")

        # Locate all p elements within the div
        p_elements = story_div.find_elements(By.XPATH, ".//p")

        # Get the text of each p element
        p_texts = ""
        for p in p_elements:
            p_texts += p.text + "\n\n"
        print(type(p_texts))


        # write metadata
        obj = {}
        obj["url"] = url.strip()
        obj["image"] = img_src.strip()
        obj["name"] = h1_element.text.strip()
        obj["author"] = h5_element.text.strip()
        obj["text"] = p_texts
        write_metadata(obj)
        write_story(obj)

    finally:
        # Quit the WebDriver
        driver.quit()

fetch_a_story(driver,url)
