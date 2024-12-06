from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
def main():
    text = "This is **bold text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    print(text_to_textnodes(text))


if __name__ == "__main__":
    main()