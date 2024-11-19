import math
from sklearn.decomposition import TruncatedSVD
import numpy as np

def process_data(inputs):
    terms = []           # List to hold unique terms
    term_map = {}       # Dictionary to map terms to their index
    term_sets = []      # List to hold sets of terms for each description
    count_maps = []     # List to hold count maps for each description

    for input in inputs:

        input_count_map = {}
        # Count the occurrences of each word in the description
        for word in input:
            if word not in input_count_map:
                input_count_map[word] = 0  # Initialize count if word is new
            input_count_map[word] += 1  # Increment the count for the word
        count_maps.append(input_count_map)  # Append the count map to the list

        # Create a set of unique input for the current description
        term_set = list(set(input))

        # Update the term map and the terms list with new input
        for word in term_set:
            if word not in term_map:
                term_map[word] = len(terms)  # Map the new word to its index
                terms.append(word)            # Add the new word to the terms list

        term_sets.append(term_set) 

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

def find_sim_can(inputs, titles, num_sample):
    term_sets, terms, term_map, count_maps = process_data(inputs)
    idf_weights = calculate_idf(term_sets)

    # Construct the TF-IDF matrix
    n_documents = len(term_sets)
    n_terms = len(terms)

    # Initialize and populate the term-document matrix
    tf_matrix = np.zeros((n_terms, n_documents))
    for i, term_set in enumerate(term_sets):
        for term in term_set:
            term_index = term_map[term]
            tf_matrix[term_index, i] = count_maps[i][term]

    # Normalize term frequencies (TF normalization)
    tf_matrix = tf_matrix / tf_matrix.sum(axis=0)

    # Calculate the TF-IDF matrix
    idf_vector = np.array([idf_weights[term] for term in terms])

    # Tile the IDF vector to match the size of the term count matrix
    idf_matrix = np.tile(idf_vector, (len(term_sets), 1))

    # Compute the TF-IDF matrix by multiplying the term frequency matrix with the IDF matrix
    tf_idf_matrix = np.multiply(tf_matrix, idf_matrix.T)

    # Normalize columns (document vectors) in TF-IDF matrix
    tf_idf_matrix = tf_idf_matrix / np.linalg.norm(tf_idf_matrix, axis=0)

    samples_candidates = []

    for query_index in range(len(titles) - num_sample,len(titles)):
        query_vector = tf_idf_matrix[:, query_index]
        candidates = []
        for i in range(tf_idf_matrix.shape[1]):
                similarity = np.dot(query_vector.T, tf_idf_matrix[:, i])
                candidates.append((i, similarity))

        samples_candidates.append((query_index, candidates))
    
    return samples_candidates




def find_sim_can_svd(inputs, titles, num_sample, n_components):
    term_sets, terms, term_map, count_maps = process_data(inputs)
    idf_weights = calculate_idf(term_sets)

    # Construct the TF-IDF matrix
    n_documents = len(term_sets)
    n_terms = len(terms)

    # Initialize and populate the term-document matrix
    tf_matrix = np.zeros((n_terms, n_documents))
    for i, term_set in enumerate(term_sets):
        for term in term_set:
            term_index = term_map[term]
            tf_matrix[term_index, i] = count_maps[i][term]

    # Normalize term frequencies (TF normalization)
    tf_matrix = tf_matrix / tf_matrix.sum(axis=0)

    # Calculate the TF-IDF matrix
    idf_vector = np.array([idf_weights[term] for term in terms])

    # Tile the IDF vector to match the size of the term count matrix
    idf_matrix = np.tile(idf_vector, (len(term_sets), 1))

    # Compute the TF-IDF matrix by multiplying the term frequency matrix with the IDF matrix
    tf_idf_matrix = np.multiply(tf_matrix, idf_matrix.T)

    # Normalize columns (document vectors) in TF-IDF matrix
    tf_idf_matrix = tf_idf_matrix / np.linalg.norm(tf_idf_matrix, axis=0)

    # Apply SVD to reduce dimensions
    svd = TruncatedSVD(n_components)
    reduced_matrix = svd.fit_transform(tf_idf_matrix.T)  # Transpose for SVD

    samples_candidates = []

    for query_index in range(len(titles) - num_sample, len(titles)):
        query_vector = reduced_matrix[query_index]
        candidates = []
        for i in range(reduced_matrix.shape[0]):
            similarity = np.dot(query_vector, reduced_matrix[i]) / (
                np.linalg.norm(query_vector) * np.linalg.norm(reduced_matrix[i])
            )
            candidates.append((i, similarity))

        samples_candidates.append((query_index, sorted(candidates, key=lambda x: x[1], reverse=True)))

    return samples_candidates
