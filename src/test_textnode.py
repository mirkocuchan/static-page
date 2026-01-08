import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_ineq2(self):
        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_init_with_url(self):
        node = TextNode("Sample text", TextType.BOLD, "https://example.com")
        self.assertEqual(node.text, "Sample text")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, "https://example.com")

    def test_init_without_url(self):
        node = TextNode("Sample text", TextType.ITALIC)
        self.assertEqual(node.text, "Sample text")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode('This is a text node', 'text', 'https://www.boot.dev')", repr(node)
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_bold(self):
        node = TextNode("Negrita", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Negrita")

    def test_text_node_to_html_italic(self):
        node = TextNode("Cursiva", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Cursiva")

    def test_text_node_to_html_code(self):
        node = TextNode("print('hola')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hola')")

    def test_text_node_to_html_link(self):
        node = TextNode("Haz click", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Haz click")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_text_node_to_html_image(self):
        node = TextNode("Un paisaje", TextType.IMAGE, "paisaje.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "paisaje.jpg", "alt": "Un paisaje"}
        )
if __name__ == "__main__":
    unittest.main()
