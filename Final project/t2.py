import requests
import json
import re

# Function to clean HTML tags from the description
def clean_description(description):
    if description is None:
        return "No description available"  # Handle NoneType description
    clean = re.compile('<.*?>')
    return re.sub(clean, '', description)


# GraphQL query to get all media information (ID, title, description, genres)
query = '''
query ($page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media(sort: POPULARITY_DESC) {
            id
            title {
                romaji
            }
            description
            genres
        }
    }
}
'''
variables = {
    "page": 1,
    "perPage": 100
}


# API URL
url = 'https://graphql.anilist.co'

# Fetch the first page to get the total number of items
response = requests.post(url, json={'query': query, 'variables': variables})
data = response.json()

# Get the total number of items
total_items = data['data']['Page']['pageInfo']['total']
print(f"Total items found: {total_items}")

# Update 'perPage' to total number of items to fetch all results in one go
variables['perPage'] = total_items

# Fetch all data in one request
response = requests.post(url, json={'query': query, 'variables': variables})
data = response.json()

# Pretty print the entire response for debugging
# print(json.dumps(data, indent=2))

# Access and print media details including description and genres
media_info = data['data']['Page']['media']
for media in media_info:
    print(f"ID: {media['id']}")
    print(f"Title (Romaji): {media['title']['romaji']}")
    print(f"Description: {clean_description(media['description'])}")
    print(f"Genres: {', '.join(media['genres'])}")
    print('-' * 80)  # Separator between entries
