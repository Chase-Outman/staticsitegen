import re
import os
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_node_list.append(old_node)
            continue
        split_nodes = []
        split = old_node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(split[i], text_type))

        new_node_list.extend(split_nodes)    
                
    return new_node_list

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:        
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue        
        #extract image data from text from an old_node
        #return the old node if list of tuples is empty
        text_tuples = extract_markdown_images(old_node.text)
        if len(text_tuples) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        splits = old_node.text.split(f"![{text_tuples[0][0]}]({text_tuples[0][1]})", maxsplit=1)

        if len(splits)== 1:
            split_nodes.append(TextNode(splits[0],TextType.NORMAL))
        else:
            split_nodes.append(TextNode(splits[0], TextType.NORMAL))
            split_nodes.append(TextNode(text_tuples[0][0], TextType.IMAGE, text_tuples[0][1]))
            split_nodes.extend(split_nodes_image([TextNode(splits[1], TextType.NORMAL)]))
        
        for s in split_nodes:
            if s.text == "":
                split_nodes.remove(s)   

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:        
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue        
        #extract image data from text from an old_node
        #return the old node if list of tuples is empty
        text_tuples = extract_markdown_links(old_node.text)
        if len(text_tuples) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        splits = old_node.text.split(f"[{text_tuples[0][0]}]({text_tuples[0][1]})", maxsplit=1)

        if len(splits)== 1:
            split_nodes.append(TextNode(splits[0],TextType.NORMAL))
        else:
            split_nodes.append(TextNode(splits[0], TextType.NORMAL))
            split_nodes.append(TextNode(text_tuples[0][0], TextType.LINK, text_tuples[0][1]))
            split_nodes.extend(split_nodes_link([TextNode(splits[1], TextType.NORMAL)]))
        
        for s in split_nodes:
            if s.text == "":
                split_nodes.remove(s)   

        new_nodes.extend(split_nodes)

    return new_nodes    

def extract_markdown_images(text):    
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches            

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches 

def text_to_textnodes(text):
    orginal_node = TextNode(text, TextType.NORMAL)
    nodes = [orginal_node]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)   
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if re.match(r"^#{1} ", line):
            return line.replace("#", "").strip()
        
    raise Exception("No title in markdown file")


