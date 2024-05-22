import streamlit as st
import pandas as pd

# Initialize session state
def initialize_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Add user message
def add_user_message(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Add assistant message
def add_assistant_message(response: str):
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Generate label information based on product name
def generate_label(product_name: str):
    df = pd.read_csv('drinks.csv')
    if product_name not in df['product_name'].values:
        return "Product not found"
    
    product_info = df[df['product_name'] == product_name].iloc[0]
    label = f"""
    **Product Name:** {product_info['product_name']}
    **Description:** {product_info['description']}
    **Ingredients:** {product_info['ingredients']}
    **Volume:** {product_info['volume']}
    """
    return label

# Main application
initialize_session_state()

st.title("飲料水ラベル生成チャットボット")

# Display chat history
display_chat()

# User input
user_input = st.text_input("Enter the product name to generate label information:")

if st.button("Send"):
    add_user_message(user_input)
    
    # Generate label information
    response = generate_label(user_input)
    add_assistant_message(response)

# Display updated chat history
display_chat()
