import os
import re
import json
from pathlib import Path

def escape_mdx(text):
    escape_chars = r'[<>@\[\]\\`*_{}&#]'
    return re.sub(escape_chars, lambda m: '\\' + m.group(0), text)

def extract_script_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    info = {
        'name': 'N/A',
        'description': 'N/A',
        'author': 'N/A',
        'downloadURL': None
    }

    patterns = {
        'name': r'@name\s+(.+)',
        'description': r'@description\s+(.+)',
        'author': r'@author\s+(.+)',
        'downloadURL': r'@downloadURL\s+(.+)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            info[key] = escape_mdx(match.group(1).strip())

    # If downloadURL is not found, check the associated options.json file
    if info['downloadURL'] is None:
        options_file = file_path.with_name(file_path.stem.replace('.user', '') + '.options.json')
        print(f"Checking for options file: {options_file}")
        if options_file.exists():
            print(f"Options file found: {options_file}")
            with open(options_file, 'r', encoding='utf-8') as f:
                options_data = json.load(f)
                print(f"Options data: {json.dumps(options_data, indent=2)}")
                file_url = options_data.get('meta', {}).get('file_url')
                if file_url:
                    info['downloadURL'] = escape_mdx(file_url)
                    print(f"File URL found: {file_url}")
                else:
                    print("No file_url found in options.json")
        else:
            print("Options file not found")

    return info

def generate_markdown(scripts_info):
    markdown = "## My Tampermonkey Userscripts\n\nThis is just my personal list of userscripts that I use. I will try to keep this list updated as I add or remove userscripts.\n\n"
    
    for script in scripts_info:
        markdown += f"### {script['name']}\n\n"
        markdown += f"{script['description']}\n\n"
        markdown += f"**Author:** {script['author']}\n\n"
        if script['downloadURL']:
            markdown += f"**Download:** [{script['downloadURL']}]({script['downloadURL']})\n\n"
        else:
            markdown += "**Download:** N/A\n\n"
        markdown += "---\n\n"
    
    return markdown

def main():
    script_dir = Path('./scripts')
    output_file = Path('./userscripts.mdx')

    if not script_dir.exists():
        print(f"Error: The directory {script_dir} does not exist.")
        return

    scripts_info = []

    for file in script_dir.glob('*.user.js'):
        print(f"\nProcessing file: {file}")
        info = extract_script_info(file)
        scripts_info.append(info)
        print(f"Extracted info: {info}")

    markdown_content = generate_markdown(scripts_info)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\nMarkdown file has been generated: {output_file}")

if __name__ == "__main__":
    main()