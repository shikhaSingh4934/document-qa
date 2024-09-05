import streamlit as st
from openai import OpenAI
import openai

# Show title and description.
st.title("📄 LAB 1 Question Answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Validate the API key when it's entered
if openai_api_key:
    try:
        # Test the API key with a simple request
        openai.api_key = openai_api_key
        openai.Model.list()  # A simple API call to validate the key
        st.success("API key is valid! You can now upload a document and ask a question.")
    except Exception as e:
        st.error("Invalid API key. Please check and try again.", icon="🚨")
        st.stop()
else:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:

    # Process the uploaded file and question.
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    # Generate an answer using the OpenAI API.
    try:
        stream = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using the specified LLM model
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write`.
        for chunk in stream:
            st.write(chunk.choices[0].delta.get("content", ""), end="")
    
    except Exception as e:
        st.error(f"Error generating a response: {str(e)}")