from typing import Dict, Any, List, Union

def flatten_dict(
    data: Dict[str, Any],
    parent_key: str = '',
    separator: str = '_',
    flatten_lists: bool = False
) -> Dict[str, Any]:
    """
    Recursively flattens a nested dictionary into a single-level dictionary.
    """
    items: List[tuple] = []
    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator, flatten_lists).items())
        elif isinstance(value, list) and flatten_lists:
            for index, item in enumerate(value):
                list_key = f"{new_key}{separator}{index}"
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, list_key, separator, flatten_lists).items())
                else:
                    items.append((list_key, item))
        else:
            items.append((new_key, value))
    return dict(items)

def get_nested_value(data: Dict[str, Any], path: str, separator: str = '.', default: Any = None) -> Any:
    """
    Safely retrieves a value from a nested dictionary using a separator-joined path.
    """
    keys = path.split(separator)
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current