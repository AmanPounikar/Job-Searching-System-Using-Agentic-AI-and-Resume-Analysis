import re

def preprocess_text(text):
    text = text.lower()
    
    # keep letters + numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()