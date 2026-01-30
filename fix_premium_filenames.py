import os
import re
import json

def sanitize_filename(text):
    text = text.replace(' ', '-')
    # Allow alphanumeric, underscore, hyphen, and Bengali characters (U+0980 to U+09FF)
    return "".join([c for c in text if c.isalnum() or c in ('-', '_') or ('\u0980' <= c <= '\u09ff')])

def fix_filenames():
    base_story_path = "./stories/rabibasariya/premium"
    base_metadata_path = "./metadata/rabibasariya/premium"
    base_image_path = "./metadata/images/rabibasariya/premium"
    
    if not os.path.exists(base_story_path):
        print("Premium story directory not found.")
        return

    files = [f for f in os.listdir(base_story_path) if f.endswith(".md")]
    
    for filename in files:
        old_path = os.path.join(base_story_path, filename)
        
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Title and Author
        # Pattern: <h1 align=center>(.*?)</h1>\n<h2 align=center>(.*?)</h2>
        match = re.search(r'<h1 align=center>(.*?)</h1>\n<h2 align=center>(.*?)</h2>', content)
        
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            
            safe_name = sanitize_filename(title)
            safe_author = sanitize_filename(author)
            
            new_filename = f"{safe_name}-{safe_author}"
            
            print(f"Processing: {filename} -> {new_filename}")
            
            # 1. Rename Story MD
            new_story_path = os.path.join(base_story_path, new_filename + ".md")
            if old_path != new_story_path:
                os.rename(old_path, new_story_path)
                print(f"Renamed MD: {filename} -> {new_filename}.md")
            
            # 2. Rename JSON and update content
            old_json_name = filename.replace(".md", ".json")
            old_json_path = os.path.join(base_metadata_path, old_json_name)
            
            if os.path.exists(old_json_path):
                with open(old_json_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                
                # Update metadata
                data['name'] = title
                # Ensure author matches what we extracted or keep original? 
                # Scraper might have had slightly different whitespace, let's keep original data['author'] unless missing
                if 'author' not in data:
                    data['author'] = author
                
                new_json_path = os.path.join(base_metadata_path, new_filename + ".json")
                
                with open(new_json_path, 'w', encoding='utf-8') as jf:
                    json.dump(data, jf, ensure_ascii=False, indent=4)
                
                if old_json_path != new_json_path:
                    os.remove(old_json_path) # Remove old after writing new
                    print(f"Renamed JSON: {old_json_name} -> {new_filename}.json")
            else:
                print(f"Warning: JSON not found for {filename}")

            # 3. Rename Image and update MD reference
            old_image_name = filename.replace(".md", ".jpg")
            old_image_path = os.path.join(base_image_path, old_image_name)
            new_image_name = new_filename + ".jpg"
            new_image_path = os.path.join(base_image_path, new_image_name)
            
            if os.path.exists(old_image_path):
                if old_image_path != new_image_path:
                    os.rename(old_image_path, new_image_path)
                    print(f"Renamed Image: {old_image_name} -> {new_image_name}")
                
                    # Update MD content to point to new image
                    # Path in MD is relative: ../../../metadata/images/rabibasariya/premium/OLD_FILENAME
                    # We need to replace it with NEW_FILENAME
                    
                    new_content = content.replace(old_image_name, new_image_name)
                    with open(new_story_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated image link in {new_filename}.md")
            else:
                print(f"Warning: Image not found for {filename}")

        else:
            print(f"Could not parse title/author from {filename}")

if __name__ == "__main__":
    fix_filenames()
