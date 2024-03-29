# -*- coding: utf-8 -*-
"""Final Copy of Team12-Final Project-HR Analytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K8TqU_KiH--9XobW8LHDkPpJ86dfnIjL
"""

#Import Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import sys,traceback
import seaborn as sns
plt.style.use("seaborn")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn import model_selection

import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
from sklearn import preprocessing
from scipy.stats import normaltest , skewtest ,kurtosistest
from scipy.stats import chi2_contingency

from sklearn.model_selection import train_test_split , KFold
from sklearn.metrics import accuracy_score
import xgboost
import csv as csv
from xgboost import plot_importance
from matplotlib import pyplot
from sklearn.model_selection import cross_val_score

# train a logistic regression model on the training set
from sklearn.linear_model import LogisticRegression

#Import Dataset
hr_data = pd.read_csv('HR_comma_sep.csv')

"""# Data Cleaning

-Data preprocessing, EDA part.
- mentor available from 12 to 1
- univariate, bivariate, multivariate analysis, 
- univariate -take single columns and prepare graphs for them, get some fruitful information-- find patterns in the data
- bivariate - take 2 columns at a time - 1.target variable and 2, independent variable.
- multivariate - plot heatmaps, correlation plots figure out some patterns.
- use plotly - libs used for visualizations.
- dedicated marks for each capstone project
- 10 marks for completing data preprocessing, EDA, give a quick introduction of what is being done just like mini projects.
- discuss about data balancing once tasks are done


- Univariate Analysis - Madhav
- Bivariate analysis - Durga P
- Multivariate - Mallika
- Visualization - Abhijitram



"""

#Describe data set
hr_data.describe()

hr_data.head()

hr_data.head()

#Rename 'sales' column to department 
hr_data=hr_data.rename(columns = {'sales':'department'})
#Display data type for each column
hr_data.dtypes

#To get the unique values for department
hr_data['department'].unique()

#Check for missing values
hr_data.isnull().any()

"""## Bivariate Analysis

"""

def show_values(axs, orient="v", space=.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{:.1f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.1f}'.format(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

categorical = ['promotion_last_5years' ,'left' ,'Work_accident' ,'salary' , 'department']
for i in categorical :
    hr_data[i] = hr_data[i].astype('category')
hr_data.describe(include=['category'])

"""Relations between employees who Left the organisation  and satisfaction level"""

for i in hr_data.select_dtypes(['float' , 'int']).columns:

    sns.boxplot(x='left', y=i, data=hr_data, color='#99c2a2')
    plt.show()
    model = ols( '{} ~ C(left)'.format(i), data=hr_data).fit()

sns.heatmap(hr_data.select_dtypes(['float' , 'int']).corr() , annot = True , vmin=-1, vmax=1, center= 0, cmap= 'RdYlGn')

for i in hr_data.select_dtypes(['category']).drop(columns=['left']).columns:
    p =  (chi2_contingency(pd.crosstab(hr_data[i], hr_data['left']))[1])
    if p < .001 :
        print('employee choice regarding leaving gets affected by {} (reject H0)'.format(i))
    else :
        print('employee choice regarding leaving not affected by {} (fail to reject H0)'.format(i))

    contigency_pct = pd.crosstab(hr_data[i], hr_data['left'], normalize='index')
    sns.heatmap(contigency_pct, annot=True, cmap="YlGnBu")
    plt.show()

"""## Multivariate analysis"""

#To get the unique values for department and salary
hr_data['department'].unique()

hr_data['department_cat'] = hr_data['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
       'IT', 'product_mng', 'marketing', 'RandD'],
                        [0,1,2,3,4,5,6,7,8,9])

hr_data['salary'].unique()

hr_data['salary_cat'] = hr_data['salary'].replace(['low', 'medium', 'high'],[0,1,2])

hr = hr_data.drop(labels = ['department','salary'],axis=1)

#plot heatmap
plt.figure(figsize=(10,10))
heat_map = sns.heatmap( hr, linewidth = 1 , annot = True)
plt.title( "HeatMap for HR data" )
plt.show()

"""## Conclusions from EDA
* satisfaction level, work accidents, salary, time spent in the company seem to affect whether an employee will leave the organization the most.
* Satisfaction level and left are negatively correlated so less the satisfaction_level, more likely the employee is to leave the org
* work accidents and left are negatively correlated so an employee facing a work accident is less likely to leave the org
* salary and left are negatively correlated so an employee being paid less is more likely to leave the org
* time spent in the company and left are positively correlated so an employee who has spend more time in the org is more likely to leave it.

# Data Modelling
* Decision Trees - this method takes into account observations about an item to 
predict that item’s value
* Random Forest - It can handle binary features, categorical features, and numerical features. There is very little pre-processing that needs to be done
* Logistic Regression - To understand the relationship between the dependent variable and one or more independent variables by estimating probabilities
* Support Vector Machine - a supervised machine learning algorithm used for both classification and regression

## Decision Tree

### Import required packages
"""

# Install dtreeviz library
!pip -qq install dtreeviz

# Commented out IPython magic to ensure Python compatibility.
from matplotlib.colors import ListedColormap                                    # to import color map                                          
from sklearn import datasets
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor          # to import DT classifier and Regressor
import graphviz                                                                 # to import graphviz 
from dtreeviz.trees import dtreeviz                                             # to import dtreeviz 
# %matplotlib inline

"""### Training the Decision Tree"""

# Prepare the data into X (predictor) and Y (target)
X = hr.drop(labels='left',axis=1)
y = hr['left']

x_train_dt , x_test_dt , y_train_dt , y_test_dt = train_test_split(X , y)

# First tree without restrictions
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(x_train_dt,y_train_dt)

# Second tree with hyperparameters
tree_clf2 = DecisionTreeClassifier(max_depth =2, min_samples_leaf =1, min_samples_split = 2, random_state=2)
tree_clf2.fit(x_train_dt,y_train_dt)

#third tree with class weights balanced and hyperparameters
tree_clf3 = DecisionTreeClassifier(max_depth =2, min_samples_leaf =1, min_samples_split = 2, random_state=2, class_weight='balanced')
tree_clf3.fit(x_train_dt,y_train_dt)

"""### Predictions"""

# Predictions
y_pred_train_dt = tree_clf.predict (x_train_dt)
y_pred_train_2 = tree_clf2.predict (x_train_dt)
y_pred_train_3 = tree_clf3.predict (x_train_dt)

accuracy_score(y_train_dt,y_pred_train_dt)

"""Decision tree classifier with no hyperparameter tuning is closely fitting itself according to the training instances and hence the accuracy is 1, i.e. there is overfitting."""

accuracy_score(y_train_dt,y_pred_train_2)

"""To avoid overfitting the training data, the hyperparameters have been restricted and passed during the modeling."""

accuracy_score(y_train_dt,y_pred_train_3)

"""### Testing the Model"""

# Model 1 with no hyperparameter tuning
y_pred_test = tree_clf.predict (x_test_dt)

accuracy_score(y_test_dt,y_pred_test)

# Classification Report for Model 1
print(classification_report(y_test_dt,y_pred_test))

# Model 2 with hyperparameter tuning
y_pred_test_2 = tree_clf2.predict (x_test_dt)

accuracy_score(y_test_dt,y_pred_test_2)

# Classification report for Model 2
print(classification_report(y_test_dt,y_pred_test_2))

#Model 3 with balanced dataset and hyperparameter tuning
y_pred_test_3 = tree_clf3.predict (x_test_dt)

accuracy_score(y_test_dt,y_pred_test_3)

# Classification report for model 3
print(classification_report(y_test_dt,y_pred_test_3))

"""# Logistic Regression"""

X = pd.get_dummies(hr_data, columns=['Work_accident',  'promotion_last_5years', 'department', 'salary'] , drop_first=True).drop(columns=['left'])

Y = hr_data['left']

columns =X.columns

"""Dividing data into train and test sets"""

x_train_lr , x_test_lr , y_train_lr , y_test_lr = train_test_split(X , Y )

"""Scaling data (to get rid of skewness)"""

scaler  = preprocessing.MinMaxScaler()

x_train_lr= scaler.fit_transform(x_train_lr)

x_test_lr = scaler.fit_transform(x_test_lr)

# instantiate the model
logreg = LogisticRegression( random_state=0)

# fit the model
logreg.fit(x_train_lr, y_train_lr)

LogisticRegression(random_state=0)

y_pred_train_lr = logreg.predict (x_train_lr)

accuracy_score(y_train_lr,y_pred_train_lr.reshape(-1,))

"""Testing the model logistic regression"""

y_pred_test_lr = logreg.predict (x_test_lr)

accuracy_score(y_test_lr,y_pred_test_lr.reshape(-1,))

"""# Random Forest"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn import model_selection

df1 = hr_data

cat_vars=['department','salary']
for var in cat_vars:
    cat_list='var'+'_'+var
    cat_list = pd.get_dummies(df1[var], prefix=var)
    df2=df1.join(cat_list)
    df1=df2

X = df1.drop(['left', 'department', 'salary'] ,axis=1)

y = hr_data['left']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
X_train.shape, X_test.shape

# Model with hyperparameters
classifier_rf = RandomForestClassifier(random_state=42, n_jobs=-1, max_depth=5,
                                       n_estimators=100, oob_score=True)

classifier_rf.fit(X_train, y_train)

classifier_rf.oob_score_

y_pred = classifier_rf.predict(X_test)

accuracy_score(y_test, classifier_rf.predict(X_test))

print(classification_report(y_test, classifier_rf.predict(X_test)))

kfold = model_selection.KFold(n_splits=10, shuffle=True,random_state=7)
modelCV = RandomForestClassifier()
scoring = 'accuracy'
results = model_selection.cross_val_score(modelCV, X_train, y_train, cv=kfold, scoring=scoring)
print("10-fold cross validation average accuracy for Random Forest Classifier: %.3f" % (results.mean()))

"""# Model selection

"""

print('Logistic regression accuracy: {:.3f}'.format(accuracy_score(y_test_lr, logreg.predict(x_test_lr))))
print('Random Forest Accuracy: {:.3f}'.format(accuracy_score(y_test, classifier_rf.predict(X_test))))
print('Decision tree Accuracy: {:.3f}'.format(accuracy_score(y_test_dt, tree_clf3.predict(x_test_dt))))

"""Precision and Recall

We construct confusion matrix to visualize predictions made by a classifier and evaluate the accuracy of a classification.
"""

#Precison Recall Scores for Random Forest
print(classification_report(y_test, classifier_rf.predict(X_test)))

#Confusion Matrix for Random Forest
y_pred = classifier_rf.predict(X_test)
from sklearn.metrics import confusion_matrix
import seaborn as sns
forest_cm = confusion_matrix(y_pred, y_test)
sns.heatmap(forest_cm, annot=True, fmt='.2f',xticklabels = ["Left", "Stayed"] , yticklabels = ["Left", "Stayed"] )
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.title('Random Forest')
plt.savefig('random_forest')

#PRScores for Logistic Regression
print(classification_report(y_test_lr, logreg.predict(x_test_lr)))

#Confusion Matrix for Logistic Regression
logreg_y_pred = logreg.predict(x_test_lr)
logreg_cm = confusion_matrix(logreg_y_pred, y_test_lr)
sns.heatmap(logreg_cm, annot=True, fmt='.2f',xticklabels = ["Left", "Stayed"] , yticklabels = ["Left", "Stayed"] )
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.title('Logistic Regression')
plt.savefig('logistic_regression')

#PRScores for Decision Tree
print(classification_report(y_test_dt, tree_clf3.predict(x_test_dt)))

#Confusion Matrix for Decision Tree
dt_y_pred = tree_clf3.predict(x_test_dt)
dt_cm = confusion_matrix(dt_y_pred, y_test_dt)
sns.heatmap(dt_cm, annot=True, fmt='.2f',xticklabels = ["Left", "Stayed"] , yticklabels = ["Left", "Stayed"] )
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.title('Decision Tree')
plt.savefig('Decision Tree')

"""* Collate all the different metrics into one single doc or excel file to present to the professors
* Mention prediction times
* Balance the dataset manually first
* Front-end structure?
* Pick the best model and test the front-end part
* For next session, front end part should be ready
* Use advanced techniques to tune hyper parameters
* Need to have proper evidence on why a model was selected
* Next Steps - Some people need to work on trying models with hyper parameter tuning, some have to work on balancing the dataset, some have to work on completing the front-end part through webapps - enter information to see if someone will leave the organization or not.
* Should labels be given to the employees - Not required
* Features to be added to the webapp - Only use the features being used to train the model, ask these details from the user, so the model should be able to predict.
* Save your model in a pickl, write pre-processing steps in a function so whenever a new record comes in it is pre-processed and send for prediction. Whatever is predicted is displayed to the front-end user.
* Proper dashboard - 1 person
* 2 people - modelling, hyper parameter tuning
* 2 people - front-end
* Dashboard can be in what? Power BI?
* Dashboard has to make business sense, end users need to understand the story.


"""