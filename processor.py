from typing import Any, Callable, Dict, List

class DataProcessor:
    """A utility class to clean, filter, and transform raw data dictionaries.

    This processor handles basic automation tasks like cleaning keys,
    filtering out invalid entries, and applying mapping functions to data.
    """

    def __init__(self, raw_data: List[Dict[str, Any]]) -> None:
        """Initializes the DataProcessor with raw input data."""
        self.data: List[Dict[str, Any]] = raw_data

    def clean_keys(self) -> "DataProcessor":
        """Strips leading and trailing whitespaces from string keys and values.

        Returns:
            DataProcessor: The current instance with cleaned data for chaining.
        """
        cleaned: List[Dict[str, Any]] = []
        for item in self.data:
            new_item: Dict[str, Any] = {}
            for k, v in item.items():
                new_key = k.strip() if isinstance(k, str) else k
                new_val = v.strip() if isinstance(v, str) else v
                new_item[new_key] = new_val
            cleaned.append(new_item)
        self.data = cleaned
        return self

    def filter_by_key(self, key: str, value: Any) -> "DataProcessor":
        """Filters out items that do not match the specified key-value pair.

        Args:
            key: The dictionary key to check.
            value: The target value to match against.

        Returns:
            DataProcessor: The current instance with filtered data.
        """
        self.data = [item for item in self.data if item.get(key) == value]
        return self

    def transform(self, func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "DataProcessor":
        """Applies a custom transformation function to each item in the dataset.

        Args:
            func: A callback function that modifies and returns a dictionary.

        Returns:
            DataProcessor: The current instance with transformed data.
        """
        self.data = [func(item) for item in self.data]
        return self

    def execute(self) -> List[Dict[str, Any]]:
        """Retrieves the processed dataset.

        Returns:
            List[Dict[str, Any]]: The final processed list of dictionaries.
        """
        return self.data