import unittest

from htmlnode import HTMLNode, LeafNode



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "text", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(
        "p",
        "text",
        None,
        {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        )
        result = node.props_to_html()
        self.assertIn("href='https://www.google.com'", result)
        self.assertIn("target='_blank'", result)

    def test_repr(self):
        node = HTMLNode(
        "p",
        "text",
        None,
        {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
        "HTMLNode('p', 'text', None, {'href': 'https://www.google.com', 'target': '_blank'})",
        repr(node)
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_repr_leaf(self):
        node = LeafNode(
        "p",
        "text",
        {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
        "LeafNode('p', 'text', {'href': 'https://www.google.com', 'target': '_blank'})",
        repr(node)
        )
    def test_leaf_to_html(self):
        node = LeafNode("p", "text", {'href': 'https://www.google.com'})
        self.assertEqual(node.to_html(), "<p href='https://www.google.com'>text</p>")
    
        

if __name__ == "__main__":
    unittest.main()
