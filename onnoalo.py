import requests
from bs4 import BeautifulSoup
import json

HEADERS =  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

#################################
url = "https://www.prothomalo.com/onnoalo/stories/d2dh3a9wgm"
#################################

response = requests.get(url, headers=HEADERS)
# Parse the HTML with Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
story_divs = soup.find_all('div',{'class': 'story-element story-element-text'})
# print(story_divs)
# name_tag = story_div.find('h1')
# self.name = name_tag.text.strip()
# print(story_div)

# story name
name_div = soup.find('div',{'class': 'story-title-info'})
story_name = name_div.find('h1').text
print(story_name)

# story author
author_span = soup.find('span',{'class':'contributor-name'})
story_author = author_span.text
if "লেখা" in story_author:
    author_span = soup.find('span',{'class':'author-location'})
    story_author = author_span.text
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

outfile_pattern = f"{story_name}-{story_author}".strip().replace(" ", '-').replace(":", '')

# download image 
response = requests.get(story_image)
if response.status_code == 200:
    # Open a file in binary mode and write the response content to it
    with open(f"{image_path}{outfile_pattern}.jpg", 'wb') as f:
        f.write(response.content)
        print(f'{story_name}: Image downloaded')
else:
    print('Failed to download image')



with open(f"{story_path}{outfile_pattern}.md",'w') as f:
    f.write(markdown_content)

# append to list
with open('onnoalo','a') as f:
    f.write(f"[ {story_name} - {story_author} ]({story_path}{outfile_pattern}.md)\n")