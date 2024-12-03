from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_node_list.append(old_node)
            continue
        split_nodes = []
        split = old_node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(split[i], text_type))

        new_node_list.extend(split_nodes)     


                
    return new_node_list
                

    