from textnode import TextNode, TextType
def main():
    test = TextNode("This is text node", TextType.BOLD, "www.mywebpage.com")

    print(test)



if __name__ == "__main__":
    main()