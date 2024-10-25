import os
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

def process_text_files(input_file, output_directory):
    """
    Reads from an input text file, extracts nouns, verbs, and adjectives,
    and writes them to separate files in an output directory.
    
    Parameters:
        input_file (str): The path to the input text file.
        output_directory (str): The path to the output directory.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the content from the input file
    try:
        with open(input_file, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' file not found. Please create the file and add some text.")
        return

    # Filter nouns, verbs, and adjectives
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)

    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]
    verbs = [word for word, pos in tagged_tokens if pos.startswith('VB')]
    adjectives = [word for word, pos in tagged_tokens if pos.startswith('JJ')]

    # Write the extracted words to separate files in the output directory
    with open(os.path.join(output_directory, 'nouns.txt'), 'w') as file:
        file.write('\n'.join(nouns))
    
    with open(os.path.join(output_directory, 'verbs.txt'), 'w') as file:
        file.write('\n'.join(verbs))
    
    with open(os.path.join(output_directory, 'adjectives.txt'), 'w') as file:
        file.write('\n'.join(adjectives))

# Run the method
process_text_files('./video.txt', 'output_files')
