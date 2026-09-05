"""Validation functions for automation tool inputs and configurations."""

import os
import re
from typing import Any, Dict, List
from urllib.parse import urlparse


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """Validate whether a given string is a valid file path format."""
    if not isinstance(path, str) or not path.strip():
        return False
    if must_exist:
        return os.path.isfile(path)
    try:
        os.path.abspath(path)
        return True
    except (TypeError, ValueError):
        return False


def validate_url(url: str) -> bool:
    """Check if the provided string is a valid HTTP/HTTPS URL."""
    if not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def validate_payload_schema(data: Dict[str, Any], required_keys: List[str]) -> List[str]:
    """Validate payload dictionary against required keys.

    Returns a list of missing key names.
    """
    if not isinstance(data, dict):
        return required_keys.copy()

    missing_keys = [key for key in required_keys if key not in data or data[key] is None]
    return missing_keys


def validate_cron_expression(cron_str: str) -> bool:
    """Validate standard 5-part cron schedule expression."""
    if not isinstance(cron_str, str):
        return False
    parts = cron_str.strip().split()
    if len(parts) != 5:
        return False

    pattern = r"^(\*|([0-9]|[1-4][0-9]|5[0-9])|\*/[0-9]+)$"
    return all(re.match(pattern, part) for part in parts)
