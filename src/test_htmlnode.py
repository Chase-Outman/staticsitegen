import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_only_tag(self):
        node = HTMLNode("p")
        self.assertEqual(repr(node), "HTMLNode(p, None, None, None)")
    
    def test_only_value(self):
        node = HTMLNode(None, "this is the value")
        self.assertEqual(repr(node), "HTMLNode(None, this is the value, None, None)")

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )    

    def test_props_to_html(self):
        props = {
                    "href": "https://www.google.com", 
                    "target": "_blank",
                }
        
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_parentnode_all_leafnodes(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold Text"),
            LeafNode(None, "Normal Text"),
            LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold Text</b>Normal Text<i>italic text</i></p>")

    def test_parentnode_one_nested_parentnode(self):
        node = ParentNode("p", [
            ParentNode("a", [LeafNode("b", "Bold Text")]),
            LeafNode("i", "italic text")
            ]
        )

        self.assertEqual(node.to_html(), "<p><a><b>Bold Text</b></a><i>italic text</i></p>") 

    def test_parentnode_multiplenested_parentnodes(self):
        node = ParentNode("p", [
            ParentNode("a", [LeafNode("b", "Bold Text")]),
            LeafNode("i", "italic text"),
            ParentNode("g", [ParentNode("j", [LeafNode("b", "Bold Text")])])
            ]
        )
        self.assertEqual(node.to_html(), "<p><a><b>Bold Text</b></a><i>italic text</i><g><j><b>Bold Text</b></j></g></p>")

    def test_leafnode(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_with_props(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leafnode_no_tag(self):
        leaf = LeafNode(None, "I should be just plain text")
        self.assertEqual(leaf.to_html(), "I should be just plain text")




if __name__ == "__main__":
    unittest.main()