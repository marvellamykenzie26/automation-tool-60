import re

def validate_input_data(data: dict) -> bool:
    """Validates dictionary structure for processing tasks."""
    required_keys = ['id', 'payload', 'timestamp']
    
    # Check for presence of all required fields
    if not all(key in data for key in required_keys):
        return False
    
    # Validate ID format (expecting alphanumeric)
    if not isinstance(data['id'], str) or not re.match(r'^[a-zA-Z0-9_-]+$', data['id']):
        return False
    
    # Ensure payload is a non-empty dictionary
    if not isinstance(data['payload'], dict) or not data['payload']:
        return False
        
    return True

def sanitize_input(data: str) -> str:
    """Basic sanitization to strip control characters."""
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', data).strip()

def process_main_loop(input_stream: list):
    """Main loop with integrated validation logic."""
    processed_items = []
    for entry in input_stream:
        if validate_input_data(entry):
            # Sanitization of payload keys to ensure clean processing
            clean_entry = {k: sanitize_input(str(v)) if isinstance(v, str) else v 
                           for k, v in entry.items()}
            processed_items.append(clean_entry)
        else:
            print(f"Skipping invalid entry: {entry.get('id', 'unknown')}")
    return processed_items