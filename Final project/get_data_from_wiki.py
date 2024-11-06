import requests
from bs4 import BeautifulSoup
import json
import re

# List of Wikipedia pages and sections you want to search for
page_titles = ["Angel Beats!","List of Angel Beats! episodes"]
desired_sections = ["Summary", "Plot", "Characters", "Music", "Episode list"]
anime_titles = ["Angel Beats!","Future Diary"]
undesired_sections = ["References", "External links"]

def prepare_query(names):
    new_list = []
    for name in names:
        new_list.append([name, f"List of {name} characters", f"List of {name} episodes"])
    return new_list

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

def clean_text(text):
    text = re.sub(r'\[\s*edit\s*\]', '', text)  
    text = re.sub(r'\[\s*\d+\s*\]', '', text)    
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_wikipedia_sections(page_title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "sections",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Return list of sections with their titles and IDs
        if 'parse' in data and 'sections' in data['parse']:
            return data['parse']['sections']
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sections for {page_title}: {e}")
        return []

def get_section_content(page_title, section_id):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "section": section_id,
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        raw_html = data['parse']['text']['*']
        soup = BeautifulSoup(raw_html, 'html.parser')
        text_content = soup.get_text(separator="\n")
        text_content = clean_text(text_content)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for section {section_id} in {page_title}: {e}")
        return None

def retrieve_content_for_desired_sections(page_titles, desired_sections):
    results = {}
    
    for title in page_titles:
        print(f"Processing page: {title}")
        sections = get_wikipedia_sections(title)
        print(sections)
        # Filter sections that match desired section titles
        matched_sections = {section['line']: section['index'] for section in sections if section['line'] in desired_sections}
        
        # Retrieve content for matched sections
        page_data = {}
        for section_title, section_id in matched_sections.items():
            content = get_section_content(title, section_id)
            preview = content[:800] + "..." if content else "No content available"
            print(f"\nSection: {section_title}\nContent Preview: {preview}\n")
            page_data[section_title] = content
        
        results[title] = page_data
    
    return results

def search_and_retrieve_episode_list(titles):
    results = {}

    for title in titles:
        query = f"List of {title} episodes"
        print(f"Processing page: {query}")
        sections = get_wikipedia_sections(query)
        new_sections = {section['line']: section['index'] for section in sections if section['line'] in desired_sections}
        page_data = {}
        for section, section_id in new_sections.items():
            content = get_section_content(query, section_id)
            preview = content[:1600] + "..." if content else "No content available"
            # print(f"\nSection: {section}\nContent Preview: {preview}\n")
            content = filter_text_and_remove_custom_stopwords(content)
            page_data[section] = content
        
        results[title] = page_data

    return results

a = search_and_retrieve_episode_list(anime_titles)
print(a['Future Diary']['Episode list'])


# results = retrieve_content_for_desired_sections(page_titles, desired_sections)


