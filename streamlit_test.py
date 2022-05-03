# -*- coding: utf-8 -*-
"""Streamlit-test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ctypoInYRlaXmlnUOlK5lrLwom4kEzCs
"""



"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Uber pickups in NYC')
st.write("Hello")

hour_to_filter = st.slider('hour', 0, 23, 17)

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'
st.markdown(hour_to_filter, unsafe_allow_html=True)

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    
with st.sidebar:
   with st.echo():
        st.write("This code will be printed to the sidebar.")

   with st.spinner("Loading..."):
        time.sleep(5)
   st.success("Done!")
