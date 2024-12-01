from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
def main():
    textnode = TextNode("This is a bold text", TextType.BOLD)

    leafnode = HTMLNode.text_node_to_html_node(textnode)

    print(leafnode.to_html())    



if __name__ == "__main__":
    main()