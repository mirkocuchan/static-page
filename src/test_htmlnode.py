import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )        
    
    def test_to_html_many_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "second_child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>second_child</span></div>")

    def test_mixed_children(self):
        node = ParentNode("p", [LeafNode(None, "Texto normal "),ParentNode("b", [LeafNode(None, "Texto en negrita")])])
        self.assertEqual(node.to_html(), "<p>Texto normal <b>Texto en negrita</b></p>")

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("b", "bold")], {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), "<div class='container' id='main'><b>bold</b></div>")

    def test_headings_recursion(self):
        node = ParentNode("h1", [ParentNode("h2", [ParentNode("h3", [LeafNode(None, "Final")])])])
        self.assertEqual(node.to_html(), "<h1><h2><h3>Final</h3></h2></h1>")

if __name__ == "__main__":
    unittest.main()
