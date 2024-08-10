import os
import re
from pathlib import Path

def escape_mdx(text):
    # Escape special characters for MDX
    escape_chars = r'[<>@\[\]\\`*_{}&#]'
    return re.sub(escape_chars, lambda m: '\\' + m.group(0), text)

def extract_script_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    info = {
        'name': 'N/A',
        'description': 'N/A',
        'author': 'N/A',
        'downloadURL': 'N/A'
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

    return info

def generate_markdown(scripts_info):
    markdown = "## My Tampermonkey Userscripts\n\nThis is just my personal list of userscripts that I use. I will try to keep this list updated as I add or remove userscripts.\n\n"
    
    for script in scripts_info:
        markdown += f"### {script['name']}\n\n"
        markdown += f"{script['description']}\n\n"
        markdown += f"**Author:** {script['author']}\n\n"
        markdown += f"**Download:** [{script['downloadURL']}]({script['downloadURL']})\n\n"
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
        info = extract_script_info(file)
        scripts_info.append(info)

    markdown_content = generate_markdown(scripts_info)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Markdown file has been generated: {output_file}")

if __name__ == "__main__":
    main()