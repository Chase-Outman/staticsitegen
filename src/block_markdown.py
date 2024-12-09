import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import text_to_textnodes
from textnode import  text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unorderedlist = "unordered_list"
block_type_orderedlist = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if re.match(r"^#{1,6} ", lines[0]):
        return block_type_heading
    
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unorderedlist
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unorderedlist
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_orderedlist
         
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_of_block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_paragraph:
            list_of_block_nodes.append(block_to_html_paragraph_node(block))

        if block_type == block_type_heading:
            list_of_block_nodes.append(block_to_html_heading_node(block))

        if (block_type == block_type_quote):
            list_of_block_nodes.append(block_to_html_quote_node(block))

        if (block_type == block_type_code):
            list_of_block_nodes.append(block_to_html_code_node(block))

        if (block_type == block_type_unorderedlist):
            list_of_block_nodes.append(block_to_html_unorderedlist_node(block))

        if (block_type == block_type_orderedlist):
            list_of_block_nodes.append(block_to_html_orderedlist_node(block))

    html_node = ParentNode("div", list_of_block_nodes)
    return html_node

def block_to_html_orderedlist_node(block):
    children = get_list_nodes(block)
    ol_node = ParentNode("ol", children)
    return ol_node    

def block_to_html_unorderedlist_node(block):
    children = get_list_nodes(block)
    ul_node = ParentNode("ul", children)
    return ul_node

   

def block_to_html_code_node(block):
    trimmed_block = block.removesuffix("```").removeprefix("```")
    children = text_to_children(trimmed_block)
    code_node = ParentNode("code", children)
    final_node = ParentNode("pre", [code_node])
    return final_node

def block_to_html_quote_node(block):
    children = []
    if "\n" in block:
        lines = block.split("\n")
        l_lines= []
        for line in lines:    
            l_lines.append(line[2:])            
            
        line = " ".join(l_lines)
        child = text_to_children(line)
        children.extend(child)
    else:
        children = text_to_children(block[2:])   

    node = ParentNode("blockquote", children)
    return node

def block_to_html_paragraph_node(block):
    children = text_to_children(block.replace("\n", " "))

    node = ParentNode("p", children)
    return node


def block_to_html_heading_node(block):
    num_hashes = block[:7].count("#")
    block_no_hash = block[num_hashes+1:]
    children = text_to_children(block_no_hash)

    node = ParentNode(f"h{num_hashes}", children)

    return node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []

    for node in nodes:
        children.append(text_node_to_html_node(node))

    return children

def get_list_nodes(block):
    children = []
    if "\n" in block:
        lines = block.split("\n")
        for line in lines:            
            child = text_to_children(line[2:].strip())
            list_node = ParentNode("li", child)
            children.append(list_node)
    else:
        child = text_to_children(block[2:].strip())
        list_node = ParentNode("li", child)
        children.append(list_node)

    return children