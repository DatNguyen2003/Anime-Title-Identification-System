import re
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import pos_tag


def filter_nouns_verbs_adjs(text):
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)

    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]
    verbs = [word for word, pos in tagged_tokens if pos.startswith('VB')]
    adjectives = [word for word, pos in tagged_tokens if pos.startswith('JJ')]

    return nouns, verbs, adjectives

def remove_custom_stopwords(text):
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
        'don', 'should', 'now','episode','Episode','episodes','Episodes','title','Title','list','List',
        'Directed','airdate','Animation','Original','Season','Japanese'
    ]) + r')\b'

    # Remove stopwords
    result = re.sub(stopwords, '', cleaned_text, flags=re.IGNORECASE)
    
    # Remove extra spaces from the result
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def clean_text(text):

    # Remove all content inside square brackets, including the brackets themselves
    text = re.sub(r'\[.*?\]', '', text)
    
    # Replace multiple spaces with a single space and trim leading/trailing whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def strip_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    text = soup.get_text(separator="\n")
    return text