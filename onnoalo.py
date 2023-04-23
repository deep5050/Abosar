import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
from selenium import webdriver

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


f.read()

#################################
# url = "https://www.prothomalo.com/onnoalo/stories/%E0%A6%AC%E0%A7%81%E0%A6%99%E0%A7%8D%E0%A6%97%E0%A6%BE%E0%A6%B6%E0%A6%BF%E0%A6%95%E0%A6%BE%E0%A6%B0%E0%A6%BF"
#################################


def crawler(url):
    response = requests.get(url, headers=HEADERS)
    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    story_divs = soup.find_all(
        'div', {'class': 'story-element story-element-text'})
    # print(story_divs)
    # name_tag = story_div.find('h1')
    # self.name = name_tag.text.strip()
    # print(story_div)

    # story name
    name_div = soup.find('div', {'class': 'story-title-info'})
    story_name = name_div.find('h1').text
    print(story_name)

    # story author
    try:
        author_span = soup.find('span', {'class': 'contributor-name'})
        story_author = author_span.text
        if "লেখা" in story_author:
            author_span = soup.find('span', {'class': 'author-location'})
            story_author = author_span.text
    except:
        story_author = "unknown"
    print(story_author)

    # story image
    story_image = ""
    meta_images = soup.find_all('meta')
    for meta_image in meta_images:
        possible_img = meta_image.get('content')
        # print("-->" + str(possible_img))
        if "https://images.prothomalo.com/" in str(possible_img):
            story_image = possible_img

    print(story_image)

    # # print(meta_images)
    # story_image_div = soup.find('div',{'class': 'story-card-image'})
    # story_image = story_image_div.find('picture')

    # story text
    story_text = ""
    for story_div in story_divs:
        paras = story_div.find_all('p')
        for para in paras:
            story_text += para.text + "\n\n"

    story_path = "./stories/onnoalo/"
    image_path = "./metadata/images/onnoalo/"
    metadata_path = "./metadata/onnoalo/"

    markdown_content = f"<div align=center>\n<img src={story_image} />\n<br><br>\n<h1>{story_name}</h1> \n<h4>{story_author}</h4>\n<br><br>\n</div>\n\n{story_text}"

    outfile_pattern = f"{story_name}-{story_author}".strip().replace(" ",
                                                                     '-').replace(":", '')

    # download image
    response = requests.get(story_image)
    if response.status_code == 200:
        # Open a file in binary mode and write the response content to it
        with open(f"{image_path}{outfile_pattern}.jpg", 'wb') as f:
            f.write(response.content)
            print(f'{story_name}: Image downloaded')
    else:
        print('Failed to download image')

    data = {}
    data['name'] = story_name
    data['author'] = story_author
    data['image'] = story_image
    data['url'] = url
    now = datetime.datetime.now()
    # Convert the datetime object to a string with the desired format
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%d-%m-%Y")
    data['crawl_date'] = date_time_str

    with open(f"{metadata_path}{outfile_pattern}.json", 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    # if already exists skip

    markdown_file = f"{story_path}{outfile_pattern}.md"
    if not os.path.exists(markdown_file):
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
            # append to list
        with open('onnoalo', 'a') as f:
            f.write(
                f"[ {story_name} - {story_author} ]({story_path}{outfile_pattern}.md)\n")
            print("new story added !!")
    else:
        print("Skipping duplicate story")


def auto_crawl(homepage):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = './chromedriver'

    # Set up the Chrome webdriver with the options
    driver = webdriver.Chrome(chrome_options=chrome_options)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    driver.get(homepage)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

    links = soup.find_all('a', class_='card-with-image-zoom')

    # Print the href attribute of each link
    for link in links:
        print(link['href'])
    # story_links = soup.find('div',{'class':'left_image_right_news news_item wMFhj'})
    # print(len(story_links))
    # for story_link in story_links:
    #     print(story_link)


# homepage = "https://www.prothomalo.com/onnoalo/stories?"
# auto_crawl(homepage)

url = ""
with open('url') as f:
    url = f.read()

#############################################
crawler(url)
