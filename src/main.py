from textnode import TextNode, TextType
from htmlnode import HTMLNode
import os

def main():
    copy_content("test", "src")


def copy_content(source, des):
    if os.path.exists(f"./{des}"):
        print(os.listdir(f"./{des}"))
    else:
        print("not found")

main()