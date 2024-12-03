from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            split_node_list.append(old_node)
            continue

        split = old_node.text.split(delimiter)
        if len(split) == 1:
            split_node_list.append(old_node)

        elif len(split) == 2:
            raise Exception("invalid markdown syntax")

        else:
            split_node_list.append(TextNode(split[0], TextType.NORMAL))
            split_node_list.append(TextNode(split[1], text_type))
            split_node_list.append(TextNode(split[2], TextType.NORMAL))          


                
    return split_node_list
                

    