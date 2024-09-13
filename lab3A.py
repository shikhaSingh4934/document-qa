import streamlit as st
import openai

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.secrets["API_KEY"]

# Display an initial assistant message when the app is loaded
with st.chat_message("assistant"):
    st.write("Hello")

# Check if 'messages' exists in the session state; if not, initialize it
if "messages" not in st.session_state:
    st.session_state.messages = []


# After processing new input, display all chat history
for message in st.session_state.messages[-3:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])      

 

# Always display the input box for user input
prompt = st.chat_input("ask anything")



# If the user has entered a prompt, process it
if prompt:
    # Display user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    conversation_history = [{"role": "system", "content": """
        You are a helpful assistant. After giving any response, always ask 'Do you want more info?'. 
        If the user says 'yes', provide additional details on the previous response. If the user says 'no', ask the user what else they would like help with. 
        If the user asks a new question, answer the new question and then ask 'Do you want more info?' again.
        Provide explanations in a way that a 10-year-old can understand.
    """}]

    conversation_history.extend(st.session_state.messages)
    
    openai.api_key = st.secrets["API_KEY"]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        assistant_response = response["choices"][0]["message"]["content"]

    except Exception as e:
        assistant_response = f"Error: {str(e)}"          
        

    # Generate an assistant response (here it echoes the user's input)
    
    # Display the assistant's response in the chat
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        
    
    # Save assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})



print(type(st.session_state.messages))