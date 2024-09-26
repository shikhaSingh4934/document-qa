import streamlit as st
import openai
import chromadb

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.secrets["API_KEY"]

# Display an initial assistant message when the app is loaded
with st.chat_message("assistant"):
    st.write("Hello, how can I help you today?")

# Check if 'messages' exists in the session state; if not, initialize it
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all chat history (last 3 messages)
for message in st.session_state.messages[-3:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Always display the input box for user input
prompt = st.chat_input("Ask anything")

# Function to generate embeddings for a given text
def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response['data'][0]['embedding']

# Function to search the vector database (ChromaDB) for relevant documents
def search_vectorDB(query):
    query_embedding = generate_embedding(query)
    collection = st.session_state.Lab4_vectorDB
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    
    # Concatenate the documents into a single text block for context
    documents = ""
    for i, doc in enumerate(results['documents'][0]):
        documents += f"Document {i+1}: {doc}\n"
    
    return documents

# Chatbot response generation, integrating vector search (RAG)
def chatbot_response(query):
    # Step 1: Search the vectorDB and retrieve relevant documents
    relevant_documents = search_vectorDB(query)

    # Step 2: Combine the user query and relevant documents into a prompt for GPT
    conversation_history = [{"role": "system", "content": """
        You are a helpful assistant. After giving any response, always ask 'Do you want more info?'. 
        If the user says 'yes', provide additional details on the previous response. If the user says 'no', ask the user what else they would like help with. 
        If the user asks a new question, answer the new question and then ask 'Do you want more info?' again.
        Provide explanations in a way that a 10-year-old can understand.
    """}]

    # Include the relevant documents fetched from ChromaDB
    conversation_history.append({
        "role": "system",
        "content": f"Relevant course information:\n{relevant_documents}"
    })

    # Add previous conversation history
    conversation_history.extend(st.session_state.messages)
    
    # Step 3: Send the complete prompt to GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    assistant_response = response['choices'][0]['message']['content']

    return assistant_response

# If the user provides a new prompt, process it
if prompt:
    # Display user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate chatbot response with RAG (retrieval-augmented generation)
    assistant_response = chatbot_response(prompt)

    # Display the assistant's response in the chat
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Save assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
