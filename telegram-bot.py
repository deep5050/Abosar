import asyncio
from telegram import Bot, constants
import os
from telegram import InputFile
import re
from time import sleep
# import urllib.request
import requests


##################### test ######################
# from dotenv import load_dotenv

# load_dotenv()

##################################################


TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("TELEGRAM_CHANNEL_USERNAME")


async def send_message_to_channel(message,markdown=True):
    bot = Bot(token=TOKEN)
    if markdown:
        await bot.send_message(chat_id=CHANNEL_USERNAME, text=message,parse_mode=constants.ParseMode.MARKDOWN_V2)
    else:
         await bot.send_message(chat_id=CHANNEL_USERNAME, text=message)


async def upload_file_to_channel(file_path, caption=None):
    bot = Bot(token=TOKEN)
    with open(file_path, "rb") as f:
        input_file = InputFile(f)
        await bot.send_document(chat_id=CHANNEL_USERNAME, file=input_file, caption=caption)

async def upload_photo_to_channel(file_path):
    bot = Bot(token=TOKEN)
    with open(file_path, "rb") as f:
        input_file = InputFile(f)
        await bot.send_photo(chat_id=CHANNEL_USERNAME,photo="https://imgur.com/XJpcu1U",caption="*hello everyone*",parse_mode=constants.ParseMode.MARKDOWN_V2)


#####################################################
async def post_a_story(image_url,story_url,story_title,extra_msg):
    print(f"Posting message for: {story_title}\n    {image_url}\n   {story_url}")
    
    bot = Bot(token=TOKEN)
    story_url = story_url.replace(".","\.")
    story_url = story_url.replace("-","\-")
    story_url = story_url.replace("_","\_")

    story_title = story_title.replace("-","\-")
    story_title = story_title.replace("_","\_")
    story_title = story_title.replace(".","\.")

    extra_msg = """\nJoin @rabibasariya for new stories on every sunday\. \U00002764\U00002764\n\n\[DISCLAIMER\]\nThe stories and images posted on this platform are not my own creations\. All copyright and intellectual property rights are attributed to their original authors and creators\. The contents are shared here for educational purposes only\. No copyright infringement or strike is intended\. If you are the original author or copyright holder of any content posted here and have concerns, please reach out to me at d\.pal5050@gmail\.com for appropriate credit or removal\. Your rights and ownership will be respected and acknowledged\.\nSource & Copyright\: www\.anandabazar\.com/rabibashoriyo/"""
    markdown_caption = f"\n*{story_title}*\U00002728\U00002728\n\U00002935\U00002935\U00002935\U00002935\n{story_url}\n{extra_msg}"

    await bot.send_photo(chat_id=CHANNEL_USERNAME,photo=image_url,
                        caption=markdown_caption,
                        parse_mode=constants.ParseMode.MARKDOWN_V2
                        )

async def main():
    with open("./rabibasariya","r") as f:
        lines = f.readlines()
        for link in lines[-2:]:
            # Regular expression pattern to match Markdown link
            pattern = r'\[([^\]]+)\]\(([^)]+)\)'

            # Find matches using the pattern
            matches = re.findall(pattern, link)

            if matches:
                link_text, url = matches[0]
                remote_story_file_url = f"https://github.com/deep5050/Abosar/blob/master/{url.replace('./','')}"
                remote_story_title = link_text
                raw_remote_story_file_url = remote_story_file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


                response = requests.get(raw_remote_story_file_url)
                if response.status_code == 200:
                    raw_content = response.content
                    raw_markdown = raw_content.decode("utf-8")
                    # Regular expression pattern to match image src URLs
                    pattern = r'<img\s+src="([^"]+)"'

                    # Find matches using the pattern
                    matches = re.findall(pattern, raw_markdown)

                    # Print the extracted image src URLs
                    for src_url in matches:
                        remote_image_url = src_url.replace("./", "")
                        remote_image_url = src_url.replace("../", "")
                        remote_image_url = f"https://github.com/deep5050/Abosar/blob/master/{remote_image_url}"
                        raw_remote_image_url = remote_image_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

                        sleep(2)

                        await post_a_story(raw_remote_image_url,
                                     remote_story_file_url,remote_story_title,"")
                else:
                    print("Failed to fetch content.")

            else:
                print("No match found.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

