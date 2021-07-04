import spacy
import pickle
import sys, fitz


nlp = spacy.blank('en')

train_data = pickle.load(open('train_data.pkl', 'rb'))


nlp_model = spacy.load('nlp_model')

doc = nlp_model(train_data[0][0])
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}- {ent.text}')