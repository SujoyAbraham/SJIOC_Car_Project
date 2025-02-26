import fitz  # PyMuPDF for extracting PDF content
from langchain.docstore.document import Document  # For creating Document objects
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM


# Step 1: Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF file
    pdf_text = ""

    # Extract text page by page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Load each page
        pdf_text += f"--- Page {page_num + 1} ---\n"  # Add page number for reference
        pdf_text += page.get_text()  # Extract text from page

    return pdf_text


# Step 2: Convert text to embeddings using Ollama
def get_embeddings_from_text(texts, model="llama3.2"):
    embeddings = OllamaEmbeddings(model=model)  # Initialize Ollama embeddings
    return embeddings.embed_documents(texts)  # Convert text to embeddings


# Step 3: Store embeddings in Chroma (alternative to FAISS)
def store_embeddings_in_chroma(documents):
    # Convert each chunk into a Document object with the page_content attribute
    documents_with_content = [Document(page_content=doc) for doc in documents]

    # Create a Chroma vector store
    vector_store = Chroma.from_documents(documents_with_content, embedding=OllamaEmbeddings(model="llama3.2"))
    return vector_store


# Step 4: Set up LangChain to query the vector store (RAG)
def setup_rag_chain(pdf_path, model="llama3.2"):
    # Extract content from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Split content into chunks (e.g., by paragraphs, pages, etc.)
    pdf_chunks = pdf_text.split("\n--- Page ")
    if pdf_chunks[0].startswith("---"):
        pdf_chunks[0] = pdf_chunks[0][7:]  # Skip the first page header if split is on the first page

    # Step 5: Convert chunks to embeddings
    embeddings = get_embeddings_from_text(pdf_chunks, model=model)
    print('Splitting completed')

    # Step 6: Store embeddings in Chroma
    vector_store = store_embeddings_in_chroma(pdf_chunks)
    print('Storing Vector completed')

    # Step 7: Extract the retriever from Chroma vector store
    retriever = vector_store.as_retriever()  # Create a retriever object from Chroma
    print("Retriever completed")

    # Step 8: Setup LangChain for retrieval-augmented generation (RAG)
    llm = OllamaLLM(model=model)  # Initialize the Ollama model directly

    # Use the new retrieval chain constructor
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # Optional, if you want to return the source of the response
    )

    return rag_chain


# Main function to interact with the user
def main():
    # Ask the user for the path of the PDF file
    pdf_path = "./files/MOSC-Constitution.pdf"

    # Initialize the RAG chain only once
    rag_chain = setup_rag_chain(pdf_path)

    # Continuous query loop
    while True:
        query = input("Ask about the MOSC Constitution (or type 'exit' to quit): ")

        if query.lower() == 'exit':
            print("Exiting the query loop.")
            break

        # Get the response from the document using RAG
        response = rag_chain.invoke(query)

        # Access the result and source documents
        answer = response['result']
        source_documents = response['source_documents']

        # Print or process the answer and source documents
        print("Answer to your query:", answer)
        #print("Source Documents:", source_documents)


if __name__ == "__main__":
    main()
