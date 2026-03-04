import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()

    raise Exception("No Header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdownText = f.read()

    with open(template_path, 'r') as f_template:
        template = f_template.read()

    html_string = markdown_to_html_node(markdownText).to_html()

    #print(f"HTML: {html_string}")

    title = extract_title(markdownText)

    #print(f"Title: {title}")

    title_template = template.replace("{{ Title }}", title)
    full_template = title_template.replace("{{ Content }}", html_string)
    href_template = full_template.replace('href="/', f'href="{basepath}')
    src_template = href_template.replace('src="/', f'src="{basepath}')
    #print(f"Template: {full_template}, Template Type: {type(template)}")
    #print(f"os path dirname: {os.path.dirname(dest_path)}")
    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(full_template)
        

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generating all pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            print(f"Generating page {from_path} -> {dest_path}")
            generate_page(from_path, template_path, str(Path(dest_path).with_suffix(".html")), basepath)
        else:
            generate_page_recursive(from_path, template_path, dest_path, basepath)
