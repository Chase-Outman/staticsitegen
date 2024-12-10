import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from utility import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title

class TestUtility(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
            ]   
        )
    
    def test_split_nodes_delimiter_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL)
        
        self.assertRaises(Exception, lambda : split_nodes_delimiter([node], "`", TextType.CODE))

    def test_split_nodes_delimiter_non_normal_type(self):
        node = TextNode("This is already a bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is already a bold text", TextType.BOLD)])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        self.assertEqual(res, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images_no_match(self):
        text = "there are not image links here"
        res = extract_markdown_images(text)
        self.assertEqual(res, [])

    def test_extract_markdown_images_with_missing_exclamtion(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        self.assertEqual(res, [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        self.assertEqual(res, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_no_match(self):
        text = "there are no links here"
        res = extract_markdown_links(text)
        self.assertEqual(res, [])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        image_nodes = split_nodes_image([node])
        self.assertEqual(image_nodes, [
            TextNode("This is text with a image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
        ])

    def test_split_nodes_image_with_multiple_of_same_image(self):
        node = TextNode(
            "This is text with a image ![to boot dev](https://www.boot.dev) and ![to boot dev](https://www.boot.dev)",
            TextType.NORMAL,
        )
        image_nodes = split_nodes_image([node])
        self.assertEqual(image_nodes, [
            TextNode("This is text with a image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")
        ])

    def test_split_nodes_image_no_images(self):
        node = TextNode("There is no image here", TextType.NORMAL)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        image_nodes = split_nodes_link([node])
        self.assertEqual(image_nodes, [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ])

    def test_split_nodes_link_no_links(self):
        node = TextNode("There is no links here", TextType.NORMAL)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_text_textnodes(self):
        text = "This is **bold text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])

    def test_text_textnodes_just_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is just plain text", TextType.NORMAL)])

    def test_text_textnodes_just_bold(self):
        text = "This text only has a **bold** text type"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This text only has a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text type", TextType.NORMAL)
        ])

    def test_text_textnodes_just_italic(self):
        text = "This text only has a *italic* text type"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This text only has a ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text type", TextType.NORMAL)
        ])

    def test_text_textnodes_just_code(self):
        text = "This text only has a `code block` text type"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This text only has a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" text type", TextType.NORMAL)
        ])

    def test_text_textnodes_just_image(self):
        text = "This text only has a ![image](src/of/image) text type"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This text only has a ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "src/of/image"),
            TextNode(" text type", TextType.NORMAL)
        ])

    def test_text_textnodes_just_link(self):
        text = "This text only has a [link](http://www.somewhere.com) text type"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This text only has a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://www.somewhere.com"),
            TextNode(" text type", TextType.NORMAL)
        ])        

    
    def test_extract_title(self):
        md ="""
# This is the title
"""

        title = extract_title(md)

        self.assertEqual(title, "This is the title")

    def test_extract_title_with_h2(self):
        md ="""
## This is the title
"""
        self.assertRaises(Exception, lambda : extract_title(md))