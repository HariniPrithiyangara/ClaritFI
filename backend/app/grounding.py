import re

def clean_text(text: str) -> str:
    """
    Normalizes text for substring checking by:
    - Converting to lowercase
    - Collapsing multiple spaces and newlines into a single space
    - Stripping leading and trailing spaces
    - Removing non-alphanumeric characters (keeps letters, numbers, and basic spaces)
    """
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Replace newlines and carriage returns with spaces
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Remove non-alphanumeric except spaces
    text = re.sub(r'[^a-z0-9 ]', '', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def verify_clause_grounding(verbatim_text: str, original_document: str) -> bool:
    """
    Checks if the verbatim_text exists as a substring in the original_document.
    Uses normalized cleaning to ensure robustness against formatting differences.
    """
    cleaned_verbatim = clean_text(verbatim_text)
    cleaned_document = clean_text(original_document)
    
    # If the verbatim text is empty after cleaning, count it as not verified
    if not cleaned_verbatim:
        return False
        
    return cleaned_verbatim in cleaned_document
