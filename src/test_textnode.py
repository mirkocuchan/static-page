import unittest

from textnode import TextNode, TextType


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
if __name__ == "__main__":
    unittest.main()
