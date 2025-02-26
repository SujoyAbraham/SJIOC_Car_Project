import warnings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# Path to CSV document
doc_path = "./files/sjioc.csv"
model = "llama3.2"

pages = []

# Step 1: Load CSV
if doc_path:
    loader = CSVLoader(file_path=doc_path)
    for page in loader.load():  # Use loader.load() and a regular for loop
        pages.append(page)
    print("done loading....")
else:
    print("Upload a CSV file")

# Step 2: Extract text and split into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(pages)
print("Done splitting")

# Suppress the warning about requested results being greater than the number of available results
warnings.filterwarnings("ignore", message="Number of requested results .* is greater than number of elements in index.*, updating n_results = .*")

# Step 3: Add to vector database (Chroma)
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model=model),
    collection_name="simple-rag"
)
print("Done adding to vector database.")

# Step 4: Set up the LLM and retriever
llm = OllamaLLM(model=model)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm
)

# Step 5: Define RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)


# Step 6: Continuous query loop
def query_loop():
    while True:
        query = input("Enter your query (or type 'exit' to quit): ")

        if query.lower() == 'exit':
            print("Exiting the query loop.")
            break

        # Get the response from the document using RAG
        response = chain.invoke(query)

        # Output the answer
        print("Answer to your query:", response)


# Run the loop
query_loop()
