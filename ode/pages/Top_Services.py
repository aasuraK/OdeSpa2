import pandas as pd
import streamlit as st
import seaborn as sb
import matplotlib.pyplot as plt

filepath2= r"D:/topcombinations1.csv"
data = pd.read_csv(filepath2)

a = st.text_input("How many top combinations do you want", value='5')  # Default value set to 10

if a.isdigit():
    x = data.head(int(a))
    st.write(x)
else:
    st.write("Please enter a valid number")
