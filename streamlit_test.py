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

st.title('Uber pickups in NYC')
st.write("Hello")

hour_to_filter = st.slider('hour', 0, 23, 17)
