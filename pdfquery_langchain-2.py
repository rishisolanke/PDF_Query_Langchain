# -*- coding: utf-8 -*-
"""PDFQuery_Langchain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nfQYyJGv90KF-VOeWECd5mCpFInwo0Og
"""

!pip install -q cassio datasets langchain openai tiktoken

# Downgrade pyarrow to a compatible version
!pip install pyarrow==14.0.1

# Downgrade requests to the required version
!pip install requests==2.28.2

!pip check

# Langchain Components to use
!pip install langchain
!pip install langchain-community
!pip install cassio
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

# Support for dataset retrieval with HuggingFace
from datasets import load_dataset

# With CassIO, the engine powering the Astra DB integration in Langchain,
# you will also initialize the DB connection
import cassio

!pip install pyPDF2

from PyPDF2 import PdfReader

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:TdpSyHrhkPekSBYxirceQYGg:a6cb46e6e812f8180901c07415cc2ef3d0cd0ece06d7750c5d9f166a1b0a9f9e"
ASTRA_DB_ID = "fe2914a2-1142-4a38-8fe0-de4089c9a200"

OPEN_API_KEY = "your_open_api_key"

# Providing the path of pdf file/files.

pdfreader = PdfReader('budget_speech.pdf')

from typing_extensions import Concatenate

# read text from pdf

raw_text = ''
for i, page in enumerate(pdfreader.pages):
  content = page.extract_text()
  if content:
    raw_text += content

raw_text

!pip install cassio
import cassio
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

llm = OpenAI(openai_api_key=OPEN_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)

"""## Create your LangChain vector store....backed by Astra DB!"""

astra_vector_store = Cassandra(
    embedding=embedding,
    table_name = "qa_mini_demo",
    session=None,
    keyspace=None,
)

from langchain.text_splitter import CharacterTextSplitter
# we need to split the text using Text Split such that it should not increase token size
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

texts[:50]

"""### Load the dataset into the vector store"""

from langchain.indexes.vectorstore import VectorStoreIndexWrapper
astra_vector_store.add_texts(texts[:50])
print("Inserted %i headlines." % len(texts[:50]))
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

"""## Run the QA cycle

Simply run the cells and ask a question -- or quit to stop. (you can also stop execution with the "-" button on the top toolbar)

Here are some suggested questions:
• What is the current GDP?
• How much the agriculture target will be increased to and what the focus will be
"""

first_question = True
while True:
    if first_question:
        query_text = input("\nEnter your question (or type 'quit' to exit): ").strip()
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

    if query_text.lower() == 'quit':
        break

    first_question = False

    print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("\nANSWER: \"%s\"\n" % answer)

    print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc in astra_vector_store.similarity_search_with_score(query_text, k=4):
    # Print the doc to understand its structure
      print(doc)
    score = doc[1]  # Extracting score from the tuple
    print("\nScore: %.4f\n%s\n" % (score, doc[0].page_content[:84]))





