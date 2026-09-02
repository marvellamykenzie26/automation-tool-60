import os
import time
import shutil
import json
from typing import List, Dict, Optional, Any, Callable

def ensure_directory_exists(path: str) -> None:
    """Create the directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def copy_files_with_filter(source_dir: str, target_dir: str, file_extensions: Optional[List[str]] = None) -> int:
    """Copy files from source to target, filtering by extensions if provided."""
    ensure_directory_exists(target_dir)
    copied_count = 0
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            if file_extensions is None or any(filename.lower().endswith(ext.lower()) for ext in file_extensions):
                target_path = os.path.join(target_dir, filename)
                shutil.copy2(file_path, target_path)
                copied_count += 1
    return copied_count

def wait_until_file_exists(file_path: str, timeout_seconds: int = 60) -> bool:
    """Wait for a file to exist within the timeout period."""
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        if os.path.exists(file_path):
            return True
        time.sleep(1)
    return False

def delete_old_files(directory: str, max_age_seconds: int = 86400) -> int:
    """Delete files older than the specified age in seconds."""
    if not os.path.exists(directory):
        return 0
    deleted_count = 0
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                deleted_count += 1
    return deleted_count

def load_config_from_json(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config_to_json(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration dictionary to a JSON file."""
    ensure_directory_exists(os.path.dirname(config_path))
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def batch_process_files(directory: str, process_func: Callable[[str], None], file_extensions: Optional[List[str]] = None) -> int:
    """Apply a processing function to files in a directory."""
    processed_count = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if file_extensions is None or any(filename.lower().endswith(ext.lower()) for ext in file_extensions):
                try:
                    process_func(file_path)
                    processed_count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return processed_count