from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_nodes import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for i, block in enumerate(blocks):
        new_block = block.strip()
        if new_block == "":
            continue
        else:
            final_blocks.append(new_block)

    return final_blocks

def block_to_block_type(block):
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    elif block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        lines = block.split("\n")
        for line in lines:
            if line[0] != '>':
                return BlockType.PARAGRAPH

        return BlockType.QUOTE
    elif block[0] == "-":
        lines = block.split("\n")
        for line in lines:
            if line[0] != '-':
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    elif block[:3] == "1. ":
        lines = block.split("\n")
        for i, line in enumerate(lines):
            if line[:3] != f"{i + 1}. ":
                return BlockType.PARAGRAPH

        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def create_htmlnode_from_block(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            paragraphs = block.split("\n")
            stripped_paragraphs = []
            for paragraph in paragraphs:
                stripped_paragraphs.append(paragraph.strip())
            string_paragraph = ' '.join(stripped_paragraphs)
            
            nodes = text_to_children(string_paragraph)
            parent = ParentNode(tag = 'p', children = nodes)
            return parent
        
        case BlockType.HEADING:
            for i in range(6, 0, -1):
                if block[:i] == "#" * i:
                    paragraph = block[i:]
                    nodes = text_to_children(paragraph.strip())
                    parent = ParentNode(tag = f'h{i}', children = nodes)
                    return parent
                
            raise Exception("Heading does not contain #")

        
        case BlockType.CODE:
            paragraph = block.strip()[4:-3]


            return code_to_leaf_node(paragraph.lstrip())
        
        case BlockType.QUOTE:
            lines = block.split("\n")
            quote = []
            children = []
            for line in lines:
                if line[:2] == "> ":
                    quote.append(line[2:])
                else:
                    quote.append(line[1:])
            #print("BlockQuote quote:", quote)
            quote_string = ' '.join(quote)
            #print("BlockQUote string: ", quote_string)
            children = text_to_children(quote_string)
            #print("Children: ", children)
            parent = ParentNode(tag = "blockquote", children = children)
            return parent

        case BlockType.ULIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                nodes = text_to_children(line[2:])
                children.append(ParentNode(tag = "li", children = nodes))

            parent = ParentNode(tag = "ul", children = children)
            return parent
        
        case BlockType.OLIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                nodes = text_to_children(line[3:])
                children.append(ParentNode(tag="li", children = nodes))
            
            parent = ParentNode(tag = "ol", children = children)
            return parent


def text_to_children(text):
    textNodes = text_to_textnodes(text)
    children = []
    for textNode in textNodes:
        children.append(text_node_to_html_node(textNode))

    return children


def code_to_leaf_node(text):
    return ParentNode(tag = "pre", children = [
        ParentNode(tag = "code", children= [
            LeafNode(tag = None, value = text)
        ])
    ])






def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_children = create_htmlnode_from_block(block, block_type)
        children.append(block_children)

    return ParentNode(tag = "div", children = children )