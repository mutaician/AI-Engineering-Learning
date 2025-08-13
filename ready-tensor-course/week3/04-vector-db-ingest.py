import numpy as np
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

PUBLICATION_PATH = "data/publication.md"

# initialize db
client = chromadb.PersistentClient("./outputs/research.db")

# create a collection
research_collection = client.get_or_create_collection(
    name="publications",
    configuration={
        "hnsw": {'space': 'cosine'}
    }
)

# load  publication
with open(PUBLICATION_PATH) as file:
    publication_text = file.read()
    
# chunk publication
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunked_publication = text_splitter.split_text(publication_text)

# set embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# embed documents
embeddings = embedding_model.embed_documents(chunked_publication)
embeddings = np.array(embeddings)

# add chunks and embeddings to db
next_id = research_collection.count()
ids = list(range(next_id, next_id + len(chunked_publication)))
ids = [f"document_{id}" for id in ids]
research_collection.add(
    embeddings=embeddings,
    ids=ids,
    documents=chunked_publication
)

print(f"Total documents in collection: {research_collection.count()}")
