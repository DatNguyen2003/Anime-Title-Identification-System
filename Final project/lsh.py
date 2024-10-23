import math
import numpy as np
import matplotlib.pyplot as plt
import random
import mysql.connector
import re
import csv
import seaborn as sns


common_symbols = ['.','!', '?', '-', '</br>','$', ',', ';',':','"','(',')', '{','}','[',']']

def read_csv_to_list(filename):
    # Initialize an empty list to store the data from the CSV file
    data_list = []
    
    # Open the CSV file in read mode with UTF-8 encoding
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        # Create a CSV reader object to read the file
        csvreader = csv.reader(csvfile)

        # Skip the header row (if present) to focus on the data
        header = next(csvreader, None)
        
        # Iterate through each row in the CSV file
        for row in csvreader:
            # Append the current row to the data_list
            data_list.append(row)
    
    # Return the list containing all rows from the CSV file
    return data_list

def fetch_anime_data():
    # Configuration settings for connecting to the MySQL database
    db_config = {
        'user': 'root',          # Database username
        'password': '2003',      # Database password
        'host': 'localhost',     # Database host
        'database': 'anime_db'   # Name of the database to connect to
    }
    
    # Establish a connection to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_config)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SQL query to select anime data, including titles, descriptions, and genres
    cursor.execute('''
    SELECT a.id, a.title_romaji, a.description, GROUP_CONCAT(g.genre) AS genres
    FROM anime a
    LEFT JOIN genres g ON a.id = g.anime_id
    GROUP BY a.id;
    ''')

    # Fetch all results from the executed query
    anime_data = cursor.fetchall()

    # Close the cursor to release database resources
    cursor.close()
    
    # Close the database connection
    conn.close()

    # Return the fetched anime data
    return anime_data

def clean_description(description):
    # Check if the description is None; if so, return a default message
    if description is None:
        return "No description available"

    # Compile a regular expression to match HTML tags
    clean = re.compile('<.*?>')
    # Remove HTML tags from the description using the compiled regex
    description = re.sub(clean, '', description)

    # Replace each common symbol with a space in the description
    for symbol in common_symbols:
        description = description.replace(symbol, ' ')

    # Return the cleaned description by splitting it into words and joining them back with a single space
    return ' '.join(description.split())

def process_data(descriptions):
    # Initialize lists and dictionaries to store terms and their mappings
    terms = []           # List to hold unique terms
    term_map = {}       # Dictionary to map terms to their index
    term_sets = []      # List to hold sets of terms for each description
    count_maps = []     # List to hold count maps for each description

    # Iterate through each description to process its words
    for description in descriptions:
        # Split the description into words
        words = description.split()

        # Initialize a count map for the current description
        description_count_map = {}
        # Count the occurrences of each word in the description
        for word in words:
            if word not in description_count_map:
                description_count_map[word] = 0  # Initialize count if word is new
            description_count_map[word] += 1  # Increment the count for the word
        count_maps.append(description_count_map)  # Append the count map to the list

        # Create a set of unique words for the current description
        term_set = list(set(words))

        # Update the term map and the terms list with new words
        for word in term_set:
            if word not in term_map:
                term_map[word] = len(terms)  # Map the new word to its index
                terms.append(word)            # Add the new word to the terms list

        term_sets.append(term_set)  # Append the set of terms for this description

    # Return the processed data: term sets, unique terms, term mapping, and count maps
    return term_sets, terms, term_map, count_maps

def calculate_idf(term_sets):
    # Initialize a dictionary to count the number of documents each term appears in
    term_doc_count = {}

    # Iterate through each set of terms from the term_sets
    for term_set in term_sets:
        # For each word in the current term set
        for word in term_set:
            if word not in term_doc_count:
                term_doc_count[word] = 0  # Initialize the count for the word if it's new
            term_doc_count[word] += 1  # Increment the document count for the word

    # Initialize a dictionary to store the IDF values for each word
    idf_map = {}
    n_documents = len(term_sets)  # Get the total number of documents

    # Calculate the IDF for each word
    for word in term_doc_count:
        idf_map[word] = math.log(n_documents / term_doc_count[word])  # Compute IDF using the formula

    # Return the dictionary containing IDF values for all words
    return idf_map

def main():

    # Example usage
    filename = './/test.csv'  
    samples = read_csv_to_list(filename)
    samples = [sample[0] for sample in samples]

    # Fetch anime data from the database
    anime_data = fetch_anime_data()

    # Extract titles and descriptions from the fetched anime data
    titles = [anime[1] for anime in anime_data]
    descriptions = [anime[2] for anime in anime_data]
    descriptions = descriptions + samples

    # Clean descriptions by removing HTML tags and common symbols
    descriptions = [clean_description(description) for description in descriptions]

    # Process the cleaned descriptions to generate term sets, term list, term map, and count maps
    term_sets, terms, term_map, count_maps = process_data(descriptions)

    # Calculate IDF (Inverse Document Frequency) weights for the terms
    idf_weights = calculate_idf(term_sets)

    # Initialize a matrix for counting term occurrences across the articles (term x article matrix)
    count_matrix = []
    for i in range(len(terms)):
        # Create a row initialized to 0 for each term
        row = [0 for _ in range(len(term_sets))]
        count_matrix.append(row)

    # Populate the count matrix with the term frequencies in each article
    for i in range(len(term_sets)):
        term_set = term_sets[i]  # Get unique terms for each article
        for term in term_set:
            count = count_maps[i][term]  # Get the count of the term in the article
            term_index = term_map[term]  # Get the index of the term from the term map
            count_matrix[term_index][i] = count  # Update the count matrix

    # Set seed for random operations to ensure reproducibility
    np.random.seed(42)
    random.seed(42)

    # Normalize the term frequency matrix by column (TF - Term Frequency normalization)
    term_count_matrix = np.matrix(count_matrix)
    term_count_matrix = term_count_matrix / term_count_matrix.sum(axis=0)

    # Get the number of rows (terms) and columns (articles)
    n_rows = term_count_matrix.shape[0]
    n_columns = term_count_matrix.shape[1]

    # Create an IDF weight vector from the term list
    idf_weight_vector = np.array([idf_weights[terms[i]] for i in range(len(terms))])

    # Tile the IDF vector to match the size of the term count matrix
    idf_matrix = np.tile(idf_weight_vector, (len(term_sets), 1))

    # Compute the TF-IDF matrix by multiplying the term frequency matrix with the IDF matrix
    tf_idf_matrix = np.multiply(term_count_matrix, idf_matrix.T)

    # Normalize each column vector (article) in the TF-IDF matrix
    for i in range(n_columns):
        vec = tf_idf_matrix[:, i]
        vec = vec / np.linalg.norm(vec)  # Normalize to unit length
        tf_idf_matrix[:, i] = vec  # Store the normalized vector

    # Create an empty similarity matrix
    sim_matrix = np.zeros((n_columns, n_columns))

    # Calculate the pairwise similarities and store them in the sim_matrix
    for i in range(n_columns):
        vector_i = tf_idf_matrix[:, i]
        for j in range(i, n_columns):  # start from i to ensure no duplicate calculations
            vector_j = tf_idf_matrix[:, j]
            sim = np.dot(vector_i.T, vector_j)[0, 0]  # similarity value
            sim_matrix[i, j] = sim  # set the similarity for (i, j)
            sim_matrix[j, i] = sim  # set the similarity for (j, i), since it's symmetric

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(sim_matrix, annot=False, cmap="coolwarm", square=True)
    plt.title("Pairwise Similarity Heatmap")
    # plt.show()
    
    # Initialize parameters for Locality Sensitive Hashing (LSH)
    signature_size = 64  # Number of random vectors
    band_size = 4  # Number of bands for LSH
    random_vectors = []

    # Generate random vectors to project TF-IDF vectors into a lower-dimensional space
    for i in range(signature_size):
        vec = np.random.normal(size=n_rows)  # Generate random vector
        vec = vec / np.linalg.norm(vec)  # Normalize the vector
        random_vectors.append(vec)

    # Convert the list of random vectors into a matrix
    lsh_vector_matrix = np.matrix(random_vectors)

    # Compute the signature matrix by applying LSH (dot product followed by binary thresholding)
    signature_matrix = lsh_vector_matrix.dot(tf_idf_matrix) > 0

    # Finding duplicates in the dataset using LSH binning
    print('--- Find duplicates in the dataset. ---')

    n_bins = 100000  # Number of hash bins
    binned_ids = {}  # Dictionary to store article ids that fall into the same bin

    # Hash each column (article) based on its signature
    for i in range(n_columns):
        signature = tuple(list(signature_matrix[:, i].flat))  # Convert signature matrix column to a tuple
        bin = hash(signature) % n_bins  # Hash the signature to assign it to a bin
        if bin not in binned_ids:
            binned_ids[bin] = [i]  # Create a new bin if not exists
        else:
            binned_ids[bin].append(i)  # Add the article to the existing bin

    # Compare articles in the same bin to identify potential duplicates
    for bin in binned_ids:
        if len(binned_ids[bin]) > 1:  # Only check bins with multiple articles
            print(bin, binned_ids[bin])
            ids = binned_ids[bin]
            for i in range(len(ids)):
                id_i = ids[i]
                vec_i = tf_idf_matrix[:, id_i]  # TF-IDF vector of article i
                for j in range(i + 1, len(ids)):
                    id_j = ids[j]
                    vec_j = tf_idf_matrix[:, id_j]  # TF-IDF vector of article j
                    cossim = np.dot(vec_i.T, vec_j)[0, 0]  # Calculate cosine similarity
                    print(id_i, id_j, cossim)
                    # print(titles[id_i])  # Print the title of the first article
                    # print(titles[id_j])  # Print the title of the second article

    # Select a random article as the query
    column_index = random.choice(list(range(n_columns)))
    column_index = 100

    query_vector = tf_idf_matrix[:, column_index]  # Get the TF-IDF vector of the query article
    query_signature = signature_matrix[:, column_index]  # Get the LSH signature of the query article

    # Find candidates for the query by comparing signature subsets (bands)
    candidates = []
    for i in range(0, signature_size, band_size):
        query_signature_subset = list(query_signature[i:(i + band_size), 0].flat)  # Subset of the query signature
        bin = hash(tuple(query_signature_subset)) % n_bins  # Hash the signature subset
        for j in range(n_columns):
            test_signature_subset = list(signature_matrix[i:(i + band_size), j].flat)
            check_bin = hash(tuple(test_signature_subset)) % n_bins
            if bin == check_bin:  # If the hashes match, consider it a candidate
                candidates.append(j)

    # Display the query article and the candidate articles
    print('query:', descriptions[column_index])
    candidates = list(set(candidates))  # Remove duplicates from the candidate list
    print(candidates)
    print(len(candidates))
    for id in candidates:
        candidate_vector = tf_idf_matrix[:, id]  # Get the candidate TF-IDF vector
        cossim = np.dot(query_vector.T, candidate_vector)[0, 0]  # Calculate cosine similarity
        if cossim > 0.1:  # Only display candidates with significant similarity
            print('candidate:', id, descriptions[id])
            print('sim:', cossim)
            print()

main()
