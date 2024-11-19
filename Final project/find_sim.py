import csv

from helper_sql import *
from text_processing import *
from tf_idf_method import *

def read_csv_to_list(filename):
    data_list = []
    
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        header = next(csvreader, None)
        
        for row in csvreader:
            data_list.append(row)
    
    return data_list

def fetch_anime_nltk():
    conn, cursor = connect_database()

    # Execute a SQL query to select anime data, including titles, descriptions, and genres
    cursor.execute('''
    SELECT Title, Noun, Verb, Adj, NA 
    FROM animes_nltk
    WHERE Noun IS NOT NULL; 
    ''')

    # Fetch all results from the executed query
    data = cursor.fetchall()

    close_databse(conn, cursor)

    nouns = [anime[1] for anime in data]
    nouns = [unpack_str(noun) for noun in nouns]
    verbs = [anime[2] for anime in data]
    verbs = [unpack_str(verb) for verb in verbs]
    adjs = [anime[3] for anime in data]
    adjs = [unpack_str(adj) for adj in adjs]
    names = [anime[4] for anime in data]
    names = [unpack_str(name) for name in names]

    titles = [anime[0] for anime in data]
    return titles, nouns, verbs, adjs, names

def fetch_animes_spacy():
    conn, cursor = connect_database()

    # Execute a SQL query to select anime data, including titles, descriptions, and genres
    cursor.execute('''
    SELECT Title, Noun, Verb, Adj, NA 
    FROM animes_spacy
    WHERE Noun IS NOT NULL; 
    ''')

    # Fetch all results from the executed query
    data = cursor.fetchall()

    close_databse(conn, cursor)
    
    nouns = [anime[1] for anime in data]
    nouns = [unpack_str(noun) for noun in nouns]
    verbs = [anime[2] for anime in data]
    verbs = [unpack_str(verb) for verb in verbs]
    adjs = [anime[3] for anime in data]
    adjs = [unpack_str(adj) for adj in adjs]
    names = [anime[4] for anime in data]
    names = [unpack_str(name) for name in names]

    return nouns, verbs, adjs, names

def eval(noun, verb, adj, name):
    return 10 *noun + 1*verb + 1*adj + 30*name


filename = './tesing2.csv'   
samples = read_csv_to_list(filename)

samples_titles = [sample[0] for sample in samples]
samples = [sample[1] for sample in samples]

titles, nltk_nouns, nltk_verbs, nltk_adjs, nltk_names = fetch_anime_nltk()
spacy_nouns, spacy_verbs, spacy_adjs, spacy_names = fetch_animes_spacy()

titles = titles + samples_titles 

for sample in samples:
    text = remove_custom_stopwords(sample)
    
    nltk_noun, nltk_verb, nltk_adj, nltk_name = process_text_nltk(text)
    nltk_nouns.append(nltk_noun)
    nltk_verbs.append(nltk_verb)
    nltk_adjs.append(nltk_adj)
    nltk_names.append(nltk_name)

    spacy_noun, spacy_verb, spacy_adj, spacy_name = process_text_spacy(text)
    spacy_nouns.append(spacy_noun)
    spacy_verbs.append(spacy_verb)
    spacy_adjs.append(spacy_adj)
    spacy_names.append(spacy_name)

# nltk_noun_sim = find_sim_can(nltk_nouns, titles, len(samples_titles))
# nltk_verb_sim = find_sim_can(nltk_verbs, titles, len(samples_titles))
# nltk_adj_sim = find_sim_can(nltk_adjs, titles, len(samples_titles))
nltk_name_sim = find_sim_can(nltk_names, titles, len(samples_titles))

nltk_noun_sim = find_sim_can_svd(nltk_nouns, titles, len(samples_titles), 10)
nltk_verb_sim = find_sim_can_svd(nltk_verbs, titles, len(samples_titles), 10)
nltk_adj_sim = find_sim_can_svd(nltk_adjs, titles, len(samples_titles), 10)
# nltk_name_sim = find_sim_can_svd(nltk_names, titles, len(samples_titles), 75)

result = []
for i in range(0, len(samples_titles)):
    query_index = nltk_noun_sim[i][0] 
    candidates = []
    found = False
    for j in range(0, len(titles)):
        noun_sim = nltk_noun_sim[i][1][j][1]
        verb_sim = nltk_verb_sim[i][1][j][1]
        adj_sim = nltk_adj_sim[i][1][j][1]
        name_sim = nltk_name_sim[i][1][j][1]

        sim = eval(noun_sim, verb_sim, adj_sim, name_sim)
        # sim = eval(noun_sim, noun_sim, noun_sim, noun_sim)
        # sim = eval(verb_sim, verb_sim, verb_sim, verb_sim)
        # sim = eval(adj_sim, adj_sim, adj_sim, adj_sim)
        candidates.append((j, sim))
    top_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:10]

    print('-' * 80)
    print(f"Query Title: {titles[query_index]}")
    for doc_id, sim_score in top_candidates:
        if(doc_id == query_index): continue
        if (titles[query_index] in titles[doc_id]) or (titles[doc_id] in titles[query_index]):
            print(f"Candidate ID: {doc_id}, Similarity: {sim_score}")
            print(f"Candidate Description: {titles[doc_id]}")
            found = True

    result.append(found)

nltk_acc = sum(result)/len(result)

# spacy_noun_sim = find_sim_can(spacy_nouns, titles, len(samples_titles))
# spacy_verb_sim = find_sim_can(spacy_verbs, titles, len(samples_titles))
# spacy_adj_sim = find_sim_can(spacy_adjs, titles, len(samples_titles))
spacy_name_sim = find_sim_can(spacy_names, titles, len(samples_titles))

spacy_noun_sim = find_sim_can_svd(spacy_nouns, titles, len(samples_titles), 10)
spacy_verb_sim = find_sim_can_svd(spacy_verbs, titles, len(samples_titles), 10)
spacy_adj_sim = find_sim_can_svd(spacy_adjs, titles, len(samples_titles), 10)
# spacy_name_sim = find_sim_can_svd(spacy_names, titles, len(samples_titles), 75)

result = []
for i in range(0, len(samples_titles)):
    query_index = spacy_noun_sim[i][0] 
    candidates = []
    found = False
    for j in range(0, len(titles)):
        noun_sim = spacy_noun_sim[i][1][j][1]
        verb_sim = spacy_verb_sim[i][1][j][1]
        adj_sim = spacy_adj_sim[i][1][j][1]
        name_sim = spacy_name_sim[i][1][j][1]

        sim = eval(noun_sim, verb_sim, adj_sim, name_sim)
        # sim = eval(noun_sim, noun_sim, noun_sim, noun_sim)
        # sim = eval(verb_sim, verb_sim, verb_sim, verb_sim)
        # sim = eval(adj_sim, adj_sim, adj_sim, adj_sim)
        candidates.append((j, sim))
    top_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:10]

    print('-' * 80)
    print(f"Query Title: {titles[query_index]}")
    for doc_id, sim_score in top_candidates:
        if(doc_id == query_index): continue
        if (titles[query_index] in titles[doc_id]) or (titles[doc_id] in titles[query_index]):
            print(f"Candidate ID: {doc_id}, Similarity: {sim_score}")
            print(f"Candidate Description: {titles[doc_id]}")
            found = True

    result.append(found)

spacy_acc = sum(result)/len(result)

print("NLTK ACC: ",nltk_acc)
print("Spacy ACC: ",spacy_acc)