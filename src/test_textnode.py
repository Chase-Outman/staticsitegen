import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from utility import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_withurl(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "www.test.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.test.com")
        self.assertEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1.__repr__(), "TextNode(This is a text node, bold, None)")

    def test_eq_text(self):
        node1 = TextNode("This is a text node1", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_texttype(self):
        node1 = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "www.test.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

class TestTestNodeToHTMLNode(unittest.TestCase):

    def test_textnode_to_leafnode_normal_texttype(self):
        tnode = TextNode("this is plain text", TextType.NORMAL)
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "this is plain text")

    def test_textnode_to_leafnode_bold_texttype(self):
        tnode = TextNode("this is bold text", TextType.BOLD)
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "<b>this is bold text</b>")

    def test_textnode_to_leafnode_italic_texttype(self):
        tnode = TextNode("this is italic text", TextType.ITALIC)
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "<i>this is italic text</i>")    

    def test_textnode_to_leafnode_code_texttype(self):
        tnode = TextNode("this is code text", TextType.CODE)
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "<code>this is code text</code>")

    def test_textnode_to_leafnode_link_texttype(self):
        tnode = TextNode("this is link text", TextType.LINK, "www.thisurl.com")
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "<a href=\"www.thisurl.com\">this is link text</a>")

    def test_textnode_to_leafnode_image_texttype(self):
        tnode = TextNode("this is image text", TextType.IMAGE, "this/location/img")
        lnode = text_node_to_html_node(tnode)
        self.assertEqual(lnode.to_html(), "<img src=\"this/location/img\" alt=\"this is image text\"></img>")

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

    
if __name__ == "__main__":
    unittest.main()
