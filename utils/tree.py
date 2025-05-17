from typing import Dict, List

def tree(directory) -> str:
    """
    Recursively builds a tree structure from a list of files.
    each file have a name key and a children key.
    The function returns a string representation of the tree using ascii art.
    """

    def build_tree(node: Dict, prefix: str = "") -> str:
        result = []
        children = node.get("children", [])
        name = node.get("name", "")
        
        if not children:
            return f"{prefix}└── {name}\n"
        
        result.append(f"{prefix}├── {name}\n")
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            result.append(build_tree(child, new_prefix))
        
        return "".join(result)

    return build_tree({"name": "root", "children": directory})