import mysql.connector
import subprocess
import requests
import re

from run_sql import run_sql

def clean_description(description):
    if description is None:
        return "No description available"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', description)

def fetch_multiple_page(query, numPage):
    
    url = 'https://graphql.anilist.co'

    media_info = []

    for i in range(numPage):

        variables = {
            "page": i+1,
            "perPage": 50
        }
    
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()
        media_info += data['data']['Page']['media']

    return media_info

def insert_into_database(media_info):
    initial_config = {
        'user': 'root',  
        'password': '2003',  
        'host': 'localhost'
    }
    
    conn = mysql.connector.connect(**initial_config)
    cursor = conn.cursor()

    run_sql('create_db.sql' ,conn, cursor)

    conn.database = 'anime_db'

    for media in media_info:
        print(f"ID: {media['id']}")
        print(f"Title (Romaji): {media['title']['romaji']}")
        print(f"Description: {clean_description(media['description'])}")
        print(f"Genres: {', '.join(media['genres'])}")
        print('-' * 80)  
        cursor.execute('''
        INSERT IGNORE INTO anime (id, title_romaji, description)
        VALUES (%s, %s, %s)
        ''', (media['id'], media['title']['romaji'], clean_description(media.get('description'))))

        for genre in media.get('genres', []):  
            cursor.execute('''
            INSERT IGNORE INTO genres (anime_id, genre)
            VALUES (%s, %s)
            ''', (media['id'], genre))

    conn.commit()

    cursor.close()
    conn.close()
    return

def main():
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

    media_info = fetch_multiple_page(query,2)

    insert_into_database(media_info)

    subprocess.run([r'C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe'])

if __name__ == "__main__":
    main()