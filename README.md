Overview

PDF Query LangChain is a versatile tool designed to streamline the extraction and querying of information from PDF documents. Leveraging LangChain’s powerful language processing capabilities, OpenAI’s language models, and Cassandra’s vector store, this application provides an efficient and interactive way to interact with PDF content.

Features

    •	PDF Text Extraction: Automatically extracts text from PDF files using PyPDF2 for easy processing.
    •	Intelligent Text Splitting: Splits extracted text into manageable chunks to optimize for token limits and improve query accuracy.
    •	Vector Store Integration: Utilizes Cassandra to create and manage a vector store for efficient text storage and retrieval.
    •	Advanced Language Models: Integrates OpenAI’s language models for embedding and querying text data.
    •	Interactive Question-Answer Interface: Allows users to input queries and receive relevant answers from the PDF content in real-time.
    •	Relevance-Based Document Retrieval: Displays the most relevant documents based on the query, along with their relevance scores.
    Installation and Setup

Clone the Repository

    git clone https://github.com/yourusername/pdf-query-langchain.git
    cd pdf-query-langchain
    
Install Dependencies

    pip install -q cassio datasets langchain openai tiktoken
    pip install pyarrow==14.0.1
    pip install requests==2.28.2
    pip check
    pip install pyPDF2
    
LangChain and CassIO Components:

    pip install langchain
    pip install langchain-community
    pip install cassio
    from langchain.vectorstores.cassandra import Cassandra
    from langchain.indexes.vectorstore import VectorstoreIndexCreator
    from langchain.llms import OpenAI
    from langchain.embeddings import OpenAIEmbeddings
    
Initialize Database Connection:

    import cassio
    cassio.init(token="YOUR_ASTRA_DB_APPLICATION_TOKEN", database_id="YOUR_ASTRA_DB_ID")
    
Read and Extract Text from PDF:
    
    from PyPDF2 import PdfReader
    pdfreader = PdfReader('path_to_your_pdf.pdf')
    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
        
Text Splitting:

    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    
Create and Load Vector Store:

    astra_vector_store = Cassandra(
        embedding=embedding,
        table_name = "qa_mini_demo",
        session=None,
        keyspace=None,
    )
    astra_vector_store.add_texts(texts[:50])
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
    
Usage

Interactive QA:

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
            score = doc[1]
            print("\nScore: %.4f\n%s\n" % (score, doc[0].page_content[:84]))
            
Users can interact with the application by entering their queries to extract specific information from the PDF content. The app processes the queries using the vector store and language models to provide accurate answers and displays the most relevant documents for additional context.

Applications

    •	Data Analysis: Extract and analyze specific data points from large PDF documents.
    •	Research: Retrieve relevant information for academic or professional research.
    •	Automated Reporting: Generate reports by querying specific sections of PDF documents.
    •	Legal and Compliance: Quickly find relevant legal clauses or compliance information within lengthy documents.
    This application simplifies the process of querying and extracting information from PDFs, making it an invaluable tool for various use cases that require detailed document analysis.
