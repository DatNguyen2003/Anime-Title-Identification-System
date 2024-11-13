import mysql.connector
import subprocess
import requests
import re

from helper_sql import close_databse, connect_init_database, run_sql

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

def insert_into_database(media_info, conn, cursor):
    for media in media_info:
        print(f"ID: {media['id']}")
        print(f"Title (English): {media['title']['english']}")
        print(f"Description: {clean_description(media['description'])}")
        print(f"Genres: {', '.join(media['genres'])}")
        print('-' * 80)  
        cursor.execute('''
        INSERT IGNORE INTO animes (ID, Title, Recap, Genres)
        VALUES (%s, %s, %s, %s)
        ''', (media['id'], media['title']['english'], clean_description(media.get('description')), ', '.join(media['genres'])))

    conn.commit()
    return

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
                english
            }
            description
            genres
        }
    }
}
'''

media_info = fetch_multiple_page(query,2)
conn, cursor = connect_init_database()
insert_into_database(media_info, conn, cursor)
close_databse(conn, cursor)

subprocess.run([r'C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe'])