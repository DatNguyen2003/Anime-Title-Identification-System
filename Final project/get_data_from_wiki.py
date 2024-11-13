import requests
from text_processing import filter_nouns_verbs_adjs, remove_custom_stopwords, clean_text, strip_html
from helper_sql import close_databse, connect_database, pack_str

desired_sections = ["Summary", "Plot", "Characters", "Music", "Episode list", "Episodes"]

def fetch_anime_title(conn, cursor):
    cursor.execute('''
    SELECT Title
    FROM animes 
    ''')

    anime_data = cursor.fetchall()
    anime_titles = [anime[0] for anime in anime_data] 
    return anime_titles

def get_wikipedia_sections(query):
    # Step 1: Search for the most relevant page
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }

    try:
        # Perform the search query to get the most relevant page
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        # Check if there are search results
        if 'query' in search_data and 'search' in search_data['query'] and len(search_data['query']['search']) > 0:
            # Get the title of the most relevant page
            page_title = search_data['query']['search'][0]['title']
            print(f"Most relevant page found: {page_title}")
        else:
            print("No relevant pages found.")
            return [], "Nothing"

        # Step 2: Retrieve sections from the most relevant page
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "page": page_title,
            "prop": "sections",
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Return list of sections with their titles and IDs
        if 'parse' in data and 'sections' in data['parse']:
            return data['parse']['sections'], page_title
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sections for {query}: {e}")
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
        
        if 'parse' in data and 'text' in data['parse'] and '*' in data['parse']['text']:
            raw_html = data['parse']['text']['*']
            text = strip_html(raw_html)
            text = clean_text(text)
            return text
        else:
            print(f"No content found for section {section_id} in page '{page_title}'.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for section {section_id} in {page_title}: {e}")
        return None

def search_and_retrieve_episode_list(titles, conn, cursor):
    results = {}
    desired_sections = ["Episode list", "Episodes"]
    for title in titles:
        query = f"List of {title} episodes"
        print('-' * 80)
        print(f"Processing page: {query}")
        sections, new_query = get_wikipedia_sections(query)
        if(new_query == "Nothing"):
            continue
        new_sections = {section['line']: section['index'] for section in sections if section['line'] in desired_sections}
        data = {}
        for section, section_id in new_sections.items():
            content = get_section_content(new_query, section_id)
            preview = content[:400] + "..." if content else "No content available"
            content = remove_custom_stopwords(content)
            nouns, verbs, adjectives = filter_nouns_verbs_adjs(content)
            data[section] = content

            cursor.execute('''
            UPDATE animes
            SET 
                Noun = %s,
                Verb = %s,
                Adj = %s
            WHERE Title = %s;
            ''', (pack_str(nouns), pack_str(verbs), pack_str(adjectives), title))

            conn.commit()
            print("Data inserted to database!")
        results[title] = data

    return results

conn, cursor = connect_database()
anime_titles = fetch_anime_title(conn, cursor)
data = search_and_retrieve_episode_list(anime_titles, conn, cursor)
close_databse(conn, cursor)
