import streamlit as st
import pandas as pd

# Load the data
file_path = 'drinks.csv'  # Replace with the actual path to your drinks.csv file
drinks_df = pd.read_csv(file_path)

# Display the dataframe
st.title('Drinks Data')
st.write(drinks_df)