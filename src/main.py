import shutil, os

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node

def copy_dir_to_new_dir(source, dest):    
        #if the destination path exsist, then delete it to ensure a fresh copy of files    
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    if os.path.isfile(source):
        shutil.copy(source, dest)
        return

    dir_list = os.listdir(source)
    
    for e in dir_list:
        spath = os.path.join(source, e)
        dpath = os.path.join(dest, e)
        if os.path.isfile(spath):
            copy_dir_to_new_dir(spath, dest)    
        else:
            copy_dir_to_new_dir(spath, dpath)
    
    

def main():
    copy_dir_to_new_dir("./static", "./public")

if __name__ == "__main__":
    main()