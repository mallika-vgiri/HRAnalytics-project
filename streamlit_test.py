# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import time
import pickle

st.title('Employee Attrition Predictor')
st.write("Predict whether an employee is at risk of leaving the organization using this Employee Attrition Predictor tool. This tool, developed using advanced machine learning techniques, predicts employee attrition with over 98% accuracy")

st.image("https://blog.mavenlink.com/hubfs/employee-turnover-blog-image.png")

st.subheader('Enter some key information below about the employee to predict whether the employee will leave the organization or not')
with st.form(key='my_form'):
    satisfaction_level = st.number_input("What is the employee's satisfaction level? (Enter a value between 0 to 1 where 0 - least satisfied 1 - most satisfied)", 0.50)
    last_evaluation = st.number_input("Number of years since the employee's last evaluation",0)
    number_project = st.number_input('Number of projects the employee has worked on',0)
    avg_monthly_hours = st.number_input('On an average, how many hours did the employee work each month?',0)
    time_spend_company = st.number_input('How many years has the employee spent in the company?',0)
    work_accident = st.selectbox('Has the employee encountered a work accident during their tenure?',('Yes','No'))
    promotion_last_5years = st.selectbox('Has the employee been promoted in the last 5 years?',('Yes','No'))
    submit_button = st.form_submit_button(label='Submit')

def txt_num(val):
    if val == "Yes":
        return 1
    else:
        return 0
    
promotion_last_5years_num = txt_num(promotion_last_5years)
work_accident_num = txt_num(work_accident)

d = {'satisfaction_level':satisfaction_level,'last_evaluation':last_evaluation,'number_project':number_project, 'avg_monthly_hours': avg_monthly_hours,'time_spend_company' : time_spend_company, 'work_accident': work_accident_num, 'promotion_last_5years': promotion_last_5years_num}
df=pd.DataFrame(data=d,index=[0])

st.write(df.head())

Classifier_model = pickle.load(open(model_filename, 'rb'))


