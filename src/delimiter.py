from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        
        divided_text = node.text.split(delimiter)
        if len(divided_text) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: missing closing delimiter {delimiter}")
        
        for i in range(len(divided_text)):
            if divided_text[i] == "":
                continue

            if i % 2 == 0:
                new_nodes_list.append(TextNode(f"{divided_text[i]}", TextType.TEXT))
            else:
                new_nodes_list.append(TextNode(f"{divided_text[i]}", text_type))
    return new_nodes_list

def extract_markdown_images(text):
    matches_description = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_description

def extract_markdown_links(text):
    matches_description = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_description

def split_nodes_image(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes_list.append(node)
            continue

        for i in range(len(images)):
            one_image = images[i]
            target = f"![{one_image[0]}]({one_image[1]})"
            sections = node.text.split(target, 1)

            if sections[0] != "":
                new_nodes_list.append(TextNode(f"{sections[0]}", TextType.TEXT))
            new_nodes_list.append(TextNode(one_image[0], TextType.IMAGE, one_image[1]))
            node.text = sections[1]
            
        if node.text != "":
            new_nodes_list.append(TextNode(node.text, TextType.TEXT))
        
    return new_nodes_list

def split_nodes_link(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes_list.append(node)
            continue
        for i in range(len(links)):
            one_link = links[i]
            target = f"[{one_link[0]}]({one_link[1]})"
            sections = node.text.split(target, 1)

            if sections[0] != "":
                new_nodes_list.append(TextNode(f"{sections[0]}", TextType.TEXT))

            new_nodes_list.append(TextNode(one_link[0], TextType.LINK, one_link[1]))
            node.text = sections[1]
            
        if node.text != "":
            new_nodes_list.append(TextNode(node.text, TextType.TEXT))
        
    return new_nodes_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes