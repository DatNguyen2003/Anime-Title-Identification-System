import spacy
import stanza
import logging

# Suppress the unnecessary INFO logs from Stanza
logging.getLogger("stanza").setLevel(logging.WARNING)

# Load SpaCy for NER
nlp_spacy = spacy.load('en_core_web_sm')

# Initialize Stanza for dependency parsing (Relation Extraction)
# stanza.download('en')  # download the English model
nlp_stanza = stanza.Pipeline('en')

# Input document
document = """
Apple is considering buying a U.K. startup for $1 billion. 
Google was founded by Larry Page and Sergey Brin at Stanford University.
"""
document = """
It's a little slow-paced so far, but it's nice!
I've been reading this bit by bit as the chapters come out, so it may be more tedious to someone reading a lot of chapters at once, but it's sort of like a cute and relaxed novel leaning into slice of life.
The translator has divided the chapters, so what's numbered here as separate chapters are actually half-chapters. Given that context, I don't think it's unreasonable to be wrapping up the setup for the real conflicts in the plot in chapter 25. It did not take forever for the ML to be found and regain his memories, thank god.
It's honestly a bit too early to deliver a verdict on the ML and FL.
The FL is usually a bit passive, but she's stood up for herself when the situation is serious. Not sure where she, as an extra in the original story, will fall in the spectrum of believing that everything will or that everything should follow the original plot. With that said, she knows that she's changed the ML's original background--possibly significantly--and doesn't seem too concerned about making him go back to adhere to the narrative.
The ML at this point has mostly just been extremely devoted to the FL. He obviously has some latent obsessive and controlling tendencies, but they haven't come to the surface yet. Personally, I really appreciate the simple fact that he isn't a prince, emperor, duke of the north, someone with black or blonde hair, or named Calix or Khalid. (Why are these names used so much???) Magic users are fun!
Essentially, it's not something that pulls you in intensely, but it's still something I always enjoy reading. Step away from sweet potatoes, face slapping, and generic cider for a bit.
"""


# Step 1: Named Entity Recognition (NER) with SpaCy
doc_spacy = nlp_spacy(document)
print("Named Entities:")
entities = set()  # Create a set to store unique entities
for ent in doc_spacy.ents:
    entities.add((ent.text, ent.label_))  # Add entity and its label to the set

# Display the unique entities
for entity, label in entities:
    print(f"Entity: {entity}, Label: {label}")

# Step 2: Relation Extraction (RE) with Stanza
doc_stanza = nlp_stanza(document)

# Step 3: Extracting relations using dependency parsing from Stanza
print("\nRelations between entities:")
for sentence in doc_stanza.sentences:
    for word in sentence.words:
        # Only printing relations between words that are named entities in SpaCy's result
        if word.deprel in ['nsubj', 'dobj', 'obl', 'nmod']:
            governor = sentence.words[word.head - 1].text if word.head > 0 else 'ROOT'
            print(f"Word: {word.text}, Relation: {word.deprel}, Head: {governor}")
