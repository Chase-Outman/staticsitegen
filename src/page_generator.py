import os, pathlib

from block_markdown import markdown_to_html_node
from utility import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file = open(from_path, "r") 
    md = file.read()
    file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    generated_page = template.replace("{{ Title }}", title)
    generated_page = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(generated_page)
    to_file.close
    
def generate_pages_recursive(dir_path_content, template_path, des_dir_path):



    for filename in os.listdir(dir_path_content):
        
        filepath = os.path.join(dir_path_content, filename)
        destpath = os.path.join(des_dir_path, filename)   
        if os.path.isfile(filepath) and filepath.endswith(".md"):
            destpath = f"{destpath[:-3]}.html"
            generate_page(filepath, template_path, destpath)
        else:
            generate_pages_recursive(filepath, template_path, destpath)


