# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Employee Attrition Predictor')
st.write("Predict whether an employee is at risk of leaving the organization using this Employee Attrition Predictor tool. This tool, developed using advanced machine learning techniques, predicts employee attrition with over 98% accuracy")

st.image("https://blog.mavenlink.com/hubfs/employee-turnover-blog-image.png")


satisfaction_level = st.slider('satisfaction level', 0, 23, 17)
last_evaluation = st.slider('last evaluation',0,50)
number_of_projects = st.slider('number of projects',0,10)

d = ('satisfaction_level':satisfaction_level,'last_evaluation':last_evaluation,'number_project':number_project)
df=pd.DataFrame(data=d,index=[0])

st.write(df.head())

trial = 10 * hour_to_filter

st.write(trial)

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
    

    st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")
    
container = st.container()
container.write("This is inside the container")
st.write("This is outside the container")

# Now insert some more in the container
container.write("This is inside too")
