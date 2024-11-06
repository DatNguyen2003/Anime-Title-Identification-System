import re

def filter_text_and_remove_custom_stopwords(text):
    # Remove all characters except letters and spaces
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', text)
    
    # Define stopwords as a regular expression pattern
    stopwords = r'\b(' + '|'.join([
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 
        'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
        'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
        'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 
        'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
        'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
        'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
        'don', 'should', 'now'
    ]) + r')\b'

    # Remove stopwords
    result = re.sub(stopwords, '', cleaned_text, flags=re.IGNORECASE)
    
    # Remove extra spaces from the result
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

# Example usage
text = "Hello World! This is a Test of filtering out stopwords like the and in."
filtered_text = filter_text_and_remove_custom_stopwords(text)
print("Filtered text:", filtered_text)
