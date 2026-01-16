from enum import Enum
from htmlnode import HTMLNode, ParentNode
from delimiter import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if block.startswith("- "):
        all_ul = True
        for line in lines:
            if not line.startswith("- "):
                all_ul = False
                break
        if all_ul == True:
            return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        is_ordered = True
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                is_ordered = False
                break
        if is_ordered == True:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_type_to_tag(block_type, block_text):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    if block_type == BlockType.HEADING:
        num_of_hashtag = 0
        for char in block_text:
            if char == "#":
                num_of_hashtag += 1
        return (f"h{num_of_hashtag}")
    
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.CODE:
        return "pre"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"
    
def eliminate_symbol(block, block_type): 
    if block_type == BlockType.HEADING:
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        return block[count + 1:]
    
    if block_type == BlockType.PARAGRAPH:
        return block
    
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line.lstrip().lstrip(">").strip())
        return " ".join(cleaned_lines)
    
    if block_type == BlockType.CODE:
        return block.strip("`").strip()
    
    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n") 
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line[2:])
        return "\n".join(cleaned_lines)
    
    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n") 
        cleaned_lines = []
        for line in lines:
            parts = line.split(". ", 1)[1]
            cleaned_lines.append(parts) 
        return "\n".join(cleaned_lines)

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    block_parent_nodes = []
    for block in blocks:
        
        block_type = block_to_block_type(block)
        tag = block_type_to_tag(block_type, block)

        if block_type == BlockType.UNORDERED_LIST:
            block = eliminate_symbol(block, block_type)
            lines = block.split("\n")
            array_of_parent_nodes = []

            for line in lines:
                text_nodes = text_to_textnodes(line)
                html_nodes = []
                for text_node in text_nodes:
                    html_nodes.append(text_node_to_html_node(text_node))
                array_of_parent_nodes.append(ParentNode("li", html_nodes, None))
                      
            block_parent_node = ParentNode(tag, array_of_parent_nodes, None)
            block_parent_nodes.append(block_parent_node)

        elif block_type == BlockType.ORDERED_LIST:
            block = eliminate_symbol(block, block_type)
            lines = block.split("\n")
            array_of_parent_nodes = []

            for line in lines:
                text_nodes = text_to_textnodes(line)
                html_nodes = []
                for text_node in text_nodes:
                    html_nodes.append(text_node_to_html_node(text_node))
                array_of_parent_nodes.append(ParentNode("li", html_nodes, None))
                      
            block_parent_node = ParentNode(tag, array_of_parent_nodes, None)
            block_parent_nodes.append(block_parent_node)
        
        elif block_type == BlockType.CODE:
            block = eliminate_symbol(block, block_type)
            block = block + "\n" 

            text_node = TextNode(block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)

            parent_code = ParentNode("code", [html_node], None)
            parent_pre = ParentNode("pre", [parent_code], None)

            block_parent_nodes.append(parent_pre)

        else:
            block = eliminate_symbol(block, block_type)
            if block_type != BlockType.QUOTE:
                block = " ".join(block.split())
            text_nodes = text_to_textnodes(block)
            array_of_html_nodes = []
            for text_node in text_nodes:
                array_of_html_nodes.append(text_node_to_html_node(text_node))

            block_parent_node = ParentNode(tag, array_of_html_nodes, None)
            block_parent_nodes.append(block_parent_node)

    parent_of_html_parents = ParentNode("div", block_parent_nodes, None)
    return parent_of_html_parents

