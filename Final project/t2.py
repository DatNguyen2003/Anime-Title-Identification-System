import requests

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
            return []

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
            return data['parse']['sections']
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sections for {query}: {e}")
        return []

get_wikipedia_sections("The Future Diary")