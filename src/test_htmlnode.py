import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props = {"a": 1, "b": "b", "c": True}).props_to_html()
        ans = ' a="1" b="b" c="True"'
        self.assertEqual(ans, node) 

    def test_props_to_html2(self):
        node = HTMLNode().props_to_html()
        ans = ""
        self.assertEqual(ans, node) 


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), '<p>Hello, World!</p>')

    def test_leaf_to_html_a_without_href(self):
        node = LeafNode("a", "Click me!")
        self.assertEqual(node.to_html(), '<a>Click me!</a>')
    
    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", props = {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

    def test_leaf_without_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_with_none_children(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_with_empty_children(self):
        parent_node = ParentNode("span", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_without_tag(self):
        child_node = LeafNode("p", "test")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2")
        child_node3 = LeafNode("p", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>child2</p><p>child3</p></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_multiple_grandchildren(self):
        bold_grandchild_node = LeafNode("b", "bold grandchild 1")
        bold_child_node = ParentNode("span", [bold_grandchild_node])
        bold_parent_node = ParentNode("div", [bold_child_node])

        italic_grandchild_node = LeafNode("i", "italic grandchild 1")
        italic_child_node = ParentNode("span", [italic_grandchild_node])
        italic_parent_node = ParentNode("div", [italic_child_node])

        grandparent_node = ParentNode("div", [bold_parent_node, italic_parent_node])
        self.assertEqual(
            grandparent_node.to_html(),
            "<div><div><span><b>bold grandchild 1</b></span></div><div><span><i>italic grandchild 1</i></span></div></div>"
        )