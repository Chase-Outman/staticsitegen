import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()
