import streamlit as st
import openai
import pandas as pd
import os

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

st.title("Carbonated Drink Package Generator")

# Check if the CSV file exists, if not create an empty dataframe and save it as a CSV file
csv_file = "drinks.csv"
if not os.path.exists(csv_file):
    data = pd.DataFrame(columns=["file_name", "product_name", "description", "taste", "volume"])
    data.to_csv(csv_file, index=False)
else:
    # Load the CSV file
    data = pd.read_csv(csv_file)

# Display the data
st.write("Here is the current data on carbonated drinks:")
st.dataframe(data)

# Input form for new drink
st.header("Enter details for a new carbonated drink")
file_name = st.text_input("File Name")
product_name = st.text_input("Product Name")
description = st.text_input("Description")
taste = st.text_input("Taste")
volume = st.text_input("Volume")

if st.button("Generate Image"):
    if file_name and product_name and description and taste and volume:
        # Create the prompt for DALL-E
        prompt = f"Create an image of a {taste}-flavored carbonated drink with a {volume} capacity. The bottle should be clear, showcasing the fizzy {taste} beverage inside. The label should be bright yellow with a bold {taste} graphic, and the brand name {product_name} should be prominently displayed at the top. The label should also highlight that it contains high vitamin C. The design should be modern and refreshing, with some water droplets on the bottle to indicate coldness. The background should be simple and white to keep the focus on the bottle."

        # Call OpenAI API to generate the image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response['data'][0]['url']
        
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