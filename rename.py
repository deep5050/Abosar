import os

directory = './metadata/rabibasariya/'

for filename in os.listdir(directory):
    print(filename)

    new_filename = filename.replace('A-short-story:-', '')
    new_filename = new_filename.replace('short-story:-', '')
    new_filename = new_filename.replace('Short-story:-', '') 
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename.strip()))
    print("renaming...")
