import requests
from bs4 import BeautifulSoup
import json
import datetime
import time

DOMAIN = "https://www.anandabazar.com"

HEADERS =  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

class Story:
    def __init__(self,url):
        self.name = ""
        self.author = ""
        self.image  = ""
        self.text = ""
        self.url = url
        self.soup = ""
        
        self.fetch_story()
        self.get_name()
        self.get_author()
        self.get_image()
        self.get_text()

        self.write_metadata()
        self.write_story()
    
    def fetch_story(self):
        # Send the request with the user agent header
        response = requests.get(self.url, headers=HEADERS)
        # Parse the HTML with Beautiful Soup
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def get_name(self):
        name_div = self.soup.find('div',{'class': 'articletbox mt-32'})
        name_tag = name_div.find('h1')
        self.name = name_tag.text.strip()
    
    def get_author(self):
        author_div = self.soup.find('div',{'class': 'editorbox mt-24'})
        author_tag = author_div.find('h5')
        self.author = author_tag.text.strip()

    def get_image(self):
        image_div = self.soup.find('div',{'class': 'leadimgbox mt-24'})
        img_tag = image_div.find('img')
        self.image = img_tag['src']
        
    
    def get_text(self):
        story_text = ""
        content_div = self.soup.find('div', {'class': 'acontentbox'})

        # Find all the <p> tags under the <div> and print their contents
        for p_tag in content_div.find_all('p'):
            story_text += p_tag.text + '\n\n'
            
        self.text = story_text.strip()

    
    def write_metadata(self):
        # Create a datetime object for the current date and time
        now = datetime.datetime.now()
        # Convert the datetime object to a string with the desired format
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        date_str = now.strftime("%d-%m-%Y")

        metadata = {}
        metadata['url'] = self.url
        metadata['author'] = self.author
        metadata['crawl_date'] = date_time_str

        output_file_path = f'./metadata/rabibasariya/{self.name}-{self.author}.json'
        output_file_path = output_file_path.replace(' ', '-')
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(metadata, outfile, ensure_ascii=False)  


    def write_story(self):
        print(f'{self.name}: Writing story')
        # download image 
        now = datetime.datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        
        image_outfile = f"metadata/images/rabibasariya/{self.name}-{self.author}.jpg"
        image_outfile = image_outfile.replace(' ', '-')
        response = requests.get(self.image)
        if response.status_code == 200:
            # Open a file in binary mode and write the response content to it
            with open(image_outfile, 'wb') as f:
                f.write(response.content)
                print(f'{self.name}: Image downloaded')
        else:
            print('Failed to download image')
            
        image_section = f'<div align=center> <img src="../../{image_outfile}" align="center"></div>'
        name_section = f'<h1 align=center>{self.name}</h1>'
        author_section = f'<h2 align=center>{self.author}</h2>'
        story_section = self.text

        markdown_content = f'{image_section}<br>{name_section}\n{author_section}<br>{story_section}'
        markdown_outfile = f'./stories/rabibasariya/{self.name}-{self.author}.md'
        markdown_outfile = markdown_outfile.replace(" ", '-')

        with open(markdown_outfile, 'w') as f:
            f.write(markdown_content)

        ## append to README
        with open ('README.md', "a") as f:
            f.write(f"\n1. [ {self.name} - {self.author} ]({markdown_outfile})")
        print(f'{self.name}: Appending to README')


###########################################


class Homepage:
    def __init__(self,page):
        self.home = "https://www.anandabazar.com/rabibashoriyo/"
        self.page = page
        self.url = f'{self.home}page-{self.page}'
        self.stories = []

        self.fetch_entries()

    def fetch_entries(self):
        response = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a')

        for a_tag in a_tags:
            story_url = a_tag.get('href')
            # matching the keyword
            if "bengali-short-story" in story_url:
                if story_url not in self.stories:
                    self.stories.append(story_url)

######################################

# Set the URL and user agent
# url = "https://www.anandabazar.com/rabibashoriyo/bengali-short-story-written-by-amit-das/cid/1417309"

# story = Story(url)
# print(story.author)
# print(story.text)
# print(story.image)


#####################################

for i in range(10,20):
    rabibasariya = Homepage(str(i))
    stories_url = rabibasariya.stories

    for story_url in stories_url:
        url = f"{DOMAIN}/{story_url}"
        print(f"Fetching: {url}")
        story = Story(url)
        time.sleep(5)
    
