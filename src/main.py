from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utility import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
def main():
    node = TextNode(
        "This is text with a image ![to boot dev](https://www.boot.dev) and ![to boot dev](https://www.boot.dev)",
        TextType.NORMAL,
        )

    image_nodes = split_nodes_image([node])
  
    print(f"The size of list is {len(image_nodes)}")
    print(image_nodes) 
 
    

# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]


if __name__ == "__main__":
    main()