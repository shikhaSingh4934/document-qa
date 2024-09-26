import os
import PyPDF2
import openai
import chromadb
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY")

def setup_lab4_database(directory):

    if 'lab4' not in st.session_state:
        
        client = chromadb.PersistentClient(path=".")
        collection = client.get_or_create_collection(name="Lab4Docs")

        
        def extract_text(pdf_file):
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
            return content

        
        def create_embedding(text):
            embedding = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return embedding['data'][0]['embedding']

       
        for pdf_file in os.listdir(directory):
            if pdf_file.endswith('.pdf'):
                file_path = os.path.join(directory, pdf_file)
                
                extracted_text = extract_text(file_path)
                
                file_embedding = create_embedding(extracted_text)

            
                collection.add(
                    ids=[pdf_file], 
                    documents=[pdf_file],  
                    embeddings=[file_embedding],  
                    metadatas=[{'filename': pdf_file}]  
                )


        st.session_state.lab4_database = collection
        st.write(f"Processed {len(os.listdir(directory))} PDFs and added them to the 'Lab4Docs' collection.")
    else:
        st.write("The Lab4 database is already set up.")


def search_lab4_database(query):
    
    if 'lab4_database' not in st.session_state:
        st.write("Please initialize the Lab4 database first.")
        return

    collection = st.session_state.lab4_database

   
