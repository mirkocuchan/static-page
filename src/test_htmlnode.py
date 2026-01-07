import unittest

from htmlnode import HTMLNode



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
        node = HTMLNode.LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
if __name__ == "__main__":
    unittest.main()
