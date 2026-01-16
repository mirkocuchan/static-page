import os, shutil, pathlib, sys
from textnode import *
from markdown_blocks import eliminate_symbol, BlockType, markdown_to_html_node

def main():    
    copy_function("./static", "./docs")
    
    template_path = "template.html"
    
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_pages_recursive("./content", template_path, "./docs", basepath)
    
def copy_function(source_directory, destination_directory, first_call=True):
    if first_call and os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    list_of_dirs_and_files = os.listdir(source_directory)
    
    for item in list_of_dirs_and_files:
        if os.path.isfile(os.path.join(source_directory, item)):
            shutil.copy(os.path.join(source_directory, item), os.path.join(destination_directory, item))
        else:
             copy_function(os.path.join(source_directory, item), os.path.join(destination_directory, item), first_call=False)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip() 
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)
    
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    final_html = final_html.replace("{{ base_path }}", basepath)
    final_html = final_html.replace("{{ base_path }}", basepath)

    dest_dir = os.path.dirname(dest_path)
    
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    all_files_in_dir_path_content = os.listdir(dir_path_content)
    for file in all_files_in_dir_path_content:
        if not os.path.isfile(os.path.join(dir_path_content, file)): 
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)
        else:
            if pathlib.Path(os.path.join(dir_path_content, file)).suffix == ".md":
                dest_html_path = pathlib.Path(os.path.join(dest_dir_path, file)).with_suffix(".html")
                generate_page(os.path.join(dir_path_content, file), template_path, dest_html_path, basepath)
    
if __name__ == "__main__":
        main()