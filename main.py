import streamlit as st
import pandas as pd

# Load the data
file_path = 'path_to_your_drinks.csv'  # Replace with the actual path to your drinks.csv file
drinks_df = pd.read_csv(file_path)

# Display the dataframe
st.title('Drinks Data')
st.write(drinks_df)