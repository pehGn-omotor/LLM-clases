import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import cohere
import pandas as pd
import umap
import altair as alt
from utils import umap_plot

co = cohere.Client(os.environ['COHERE_API_KEY'])
three_words = pd.DataFrame({'text':
  [
      'joy',
      'happiness',
      'potato'
  ]})

three_words

three_words_emb = co.embed(texts=list(three_words['text']),
                           model='embed-english-v2.0').embeddings

sentences = pd.DataFrame({'text':
  [
   'Where is the world cup?',
   'The world cup is in Qatar',
   'What color is the sky?',
   'The sky is blue',
   'Where does the bear live?',
   'The bear lives in the the woods',
   'What is an apple?',
   'An apple is a fruit',
  ]})

sentences

emb = co.embed(texts=list(sentences['text']),
               model='embed-english-v2.0').embeddings

# Explore the 10 first entries of the embeddings of the 3 sentences:
for e in emb:
    print(e[:3])

len(emb[0])