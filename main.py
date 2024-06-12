import streamlit as st
import openai
import pandas as pd
import os
import requests

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

st.title("Carbonated Drink Package Generator")

# Function to check and clean the CSV file
def clean_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        if len(data.columns) != 5:
            raise ValueError("CSV file does not have the expected number of columns.")
    except pd.errors.ParserError as e:
        st.error(f"Error reading CSV file: {e}")
        with open(file_path, 'r') as f:
            content = f.readlines()
        st.text("CSV file content (first 50 lines):")
        st.text("".join(content[:50]))  # Show the first 50 lines of the CSV file
        data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    return data

# Check if the CSV file exists, if not create an empty dataframe and save it as a CSV file
csv_file = "drinks.csv"
if not os.path.exists(csv_file):
    data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    data.to_csv(csv_file, index=False)
else:
    # Load and clean the CSV file
    data = clean_csv(csv_file)

# Display the data
st.write("Here is the current data on carbonated drinks:")
st.dataframe(data)

# Input form for new drink
st.header("Enter details for a new carbonated drink")
product_name = st.text_input("Product Name")
description = st.text_input("Description")
taste = st.text_input("Taste")
volume = st.text_input("Volume")

if st.button("Generate Image"):
    if product_name and description and taste and volume:
        # Create the prompt for the image generation
        prompt = f"prompt = f"容量{volume}の{taste}風味の炭酸飲料の画像を作成してください。ボトルは透明で、中に炭酸の{taste}飲料が見えるようにしてください。ラベルは入力された{product_name}を参照して、{taste}のグラフィックが大胆に描かれ、ブランド名{product_name}が上部に目立つように表示されるようにしてください。デザインはモダンでリフレッシュ感があり、ボトルに水滴がついて冷たさを感じさせるようにしてください。背景はシンプルで白にして、ボトルに焦点が当たるようにしてください。"

        # Call OpenAI API to generate the image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response['data'][0]['url']
        
        # Save the generated image
        image_response = requests.get(image_url)
        file_name = f"{product_name.replace(' ', '_')}.jpg"
        with open(file_name, 'wb') as f:
            f.write(image_response.content)
        
        # Display the generated image
        st.image(image_url, caption=f"{product_name} Package")

        # Add new data to dataframe
        new_data = pd.DataFrame({
            "file_name": [file_name],
            "product_name": [product_name],
            "description": [description],
            "taste": [taste],
            "volume": [volume]
        })
        
        data = data.append(new_data, ignore_index=True)
        
        # Save updated data
        data.to_csv(csv_file, index=False)
        
        st.success("New drink added and image generated!")
    else:
        st.error("Please fill in all fields.")

# Optionally, display the updated dataframe
st.write("Updated data on carbonated drinks:")
st.dataframe(data)