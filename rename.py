import os

directory = './stories/rabibasariya/'

for filename in os.listdir(directory):
    print(filename)

    new_filename = filename.replace('Short-story:-', '')
    new_filename = filename.replace('short-story:-', '')
    new_filename = filename.replace('Short-Story:-', '') 
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    print("renaming...")
