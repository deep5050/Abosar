import os
import json

def generate_premium_readme():
    premium_metadata_dir = "./metadata/rabibasariya/premium"
    premium_story_rel_path = "./stories/rabibasariya/premium"
    readme_file = "rabibasariya"

    if not os.path.exists(premium_metadata_dir):
        print(f"Directory {premium_metadata_dir} does not exist.")
        return

    # Read existing readme to avoid duplicates
    existing_links = set()
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            for line in f:
                if "stories/rabibasariya/premium" in line:
                    # Extract the filename part of the link to identify uniqueness
                    # Link format: [ ... ](./stories/rabibasariya/premium/filename.md)
                    parts = line.strip().split('(')
                    if len(parts) > 1:
                        link = parts[-1].rstrip(')')
                        existing_links.add(link)

    new_entries = []
    
    files = sorted(os.listdir(premium_metadata_dir))
    for file in files:
        if file.endswith(".json"):
            json_path = os.path.join(premium_metadata_dir, file)
            base_name = os.path.splitext(file)[0]
            md_filename = base_name + ".md"
            md_rel_link = f"{premium_story_rel_path}/{md_filename}"
            
            # Skip if already in readme
            if md_rel_link in existing_links:
                continue

            try:
                with open(json_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                    name = data.get('name', base_name.replace('-', ' '))
                    author = data.get('author', 'Unknown')
                    
                    entry = f"\n[ :crown: {name} - {author} ]({md_rel_link})"
                    new_entries.append(entry)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    if new_entries:
        with open(readme_file, "a", encoding="utf-8") as rf:
            for entry in new_entries:
                rf.write(entry)
        print(f"Appended {len(new_entries)} premium stories to {readme_file}")
    else:
        print("No new premium stories to append.")

if __name__ == "__main__":
    generate_premium_readme()
