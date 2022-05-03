# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Employee Attrition Predictor')
st.write("Predict whether an employee is at risk of leaving the organization using this Employee Attrition Predictor tool. This tool, developed using advanced machine learning techniques, predicts employee attrition with over 98% accuracy")

st.image("https://blog.mavenlink.com/hubfs/employee-turnover-blog-image.png")

with st.form(key='my_form'):
    satisfaction_level = st.slider('satisfaction level', 0, 23, 17)
    last_evaluation = st.slider('last evaluation',0,50)
    number_project = st.slider('number of projects',0,10)
    submit_button = st.form_submit_button(label='Submit')

d = {'satisfaction_level':satisfaction_level,'last_evaluation':last_evaluation,'number_project':number_project}
df=pd.DataFrame(data=d,index=[0])

st.write(df.head())
