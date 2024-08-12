#!/usr/bin/env python

"""Project_Group_18.py: Preprocess the employees dataset for the In21-S4-CS3121 Group Project."""

"""For further details about the preprocessing process please refer the following notebook https://colab.research.google.com/drive/1wi62UvgbIuwNohb7lm8HNTmw4guxfgIN?usp=sharing"""

__author__ = " RANASINGHE K.S. 210518H,  PERERA I.T.M. 210460V,  MADUSANKA G.I.D.L. 210353V,  SENARATHNA L.P.S.U.K. 210588U, PRABASHWARA D.G.H. 210483T"
__version__ = "0.0.1"
__status__ = "Draft"



import pandas as pd
import numpy as np



Marvellous = pd.read_csv('./employees.csv')


# 1 Handling Missing Values

# 1.1 Handling Missing Values in “Year_of_Birth” Column
Year_of_Birth_null_rows = Marvellous.loc[(Marvellous['Year_of_Birth'] == "'0000'") ]
Year_of_Birth_not_null_rows = Marvellous.loc[(Marvellous['Year_of_Birth'] != "'0000'") ]
Year_of_Birth_not_null_rows["Year_of_Birth"] = pd.to_numeric(Year_of_Birth_not_null_rows["Year_of_Birth"])
median = Year_of_Birth_not_null_rows["Year_of_Birth"].describe()["50%"]
Year_of_Birth_null_rows["Year_of_Birth"] = median
Marvellous = pd.concat([Year_of_Birth_null_rows,Year_of_Birth_not_null_rows], axis=0, sort=False).sort_index()

# 1.2 Handling Missing Values in “Marital_Status” Column
Marital_Status_null_rows = Marvellous.loc[pd.isnull(Marvellous["Marital_Status"]) ]
Marital_Status_not_null_rows = Marvellous.loc[ ~pd.isnull(Marvellous["Marital_Status"]) ]
mode = Marital_Status_not_null_rows["Marital_Status"].mode()[0]
Marital_Status_null_rows["Marital_Status"] = mode
Marvellous = pd.concat([Marital_Status_not_null_rows,Marital_Status_null_rows], axis=0, sort=False).sort_index()



# 2 Data quality issues

## 2.1 Handling the mismatch between Title and Gender
mr_female = Marvellous[(Marvellous['Title'] == 'Mr') & (Marvellous['Gender'] != 'Male')]
ms_male = Marvellous[(Marvellous['Title'] == 'Ms') & (Marvellous['Gender'] != 'Female')]
miss_male = Marvellous[(Marvellous['Title'] == 'Miss') & (Marvellous['Gender'] != 'Female')]

Marvellous.loc[mr_female.index[0], 'Title'] = 'Ms'
Marvellous.loc[mr_female.index[1], 'Title'] = 'Ms'
Marvellous.loc[mr_female.index[2], 'Title'] = 'Ms'
Marvellous.loc[mr_female.index[3], 'Gender'] = 'Male'

Marvellous.loc[ms_male.index[0], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[1], 'Title'] = 'Mr'
Marvellous.loc[ms_male.index[2], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[3], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[4], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[5], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[6], 'Gender'] = 'Female'
Marvellous.loc[ms_male.index[7], 'Title'] = 'Mr'

Marvellous.loc[miss_male.index[0], 'Title'] = 'Mr'
Marvellous.loc[miss_male.index[1], 'Gender'] = 'Female'
Marvellous.loc[miss_male.index[1], 'Title'] = 'Ms'

Marvellous.drop('Title', axis=1)


## 2.2 Handling repetitive religion information
Marvellous.drop('Religion_ID', axis=1)


## 2.3 Handling repetitive designation information
Marvellous.drop('Designation_ID', axis=1)

## 2.4

## 2.5 Handling repetitive working Status information
Marvellous.drop('Status', axis=1)



# 3 Data transformations 

# 3.1 Transform all missing value formats to nan 
Marvellous.loc[Marvellous['Date_Resigned'].isin(['\\N']), 'Date_Resigned'] = np.nan
Marvellous.loc[Marvellous['Date_Resigned'].isin(['0000-00-00']), 'Date_Resigned'] = np.nan
Marvellous.loc[Marvellous['Inactive_Date'].isin(['\\N']), 'Inactive_Date'] = np.nan
Marvellous.loc[Marvellous['Inactive_Date'].isin(['0000-00-00']), 'Inactive_Date'] = np.nan
Marvellous.loc[Marvellous['Reporting_emp_1'].isin(['\\N']), 'Reporting_emp_1'] = np.nan
Marvellous.loc[Marvellous['Reporting_emp_2'].isin(['\\N']), 'Reporting_emp_2'] = np.nan

# 3.2 Converting Date_Joined to timestamps
Marvellous['Date_Joined'] = pd.to_datetime(Marvellous['Date_Joined']).apply(lambda x: int(x.timestamp()))
Marvellous['Date_Resigned'] = pd.to_datetime(Marvellous['Date_Resigned']).apply(lambda x: int(x.timestamp()) if x is not pd.NaT else np.nan)
Marvellous['Inactive_Date'] = pd.to_datetime(Marvellous['Inactive_Date']).apply(lambda x: int(x.timestamp()) if x is not pd.NaT else np.nan)


# 3.3 Converting Data Types of the Columns
categorical_cols = ['Name','Gender','Marital_Status','Status','Employment_Category','Employment_Type','Religion','Designation']
for col in categorical_cols:
    Marvellous[col] = Marvellous[col].astype('category')

numerical_list = ["Reporting_emp_1","Reporting_emp_2","Year_of_Birth"]
for col in numerical_list:
    Marvellous[col] = pd.to_numeric(Marvellous[col], errors='coerce')


# print(employees_data.info())


# Creating the csv file
Marvellous.to_csv("employee_preprocess_Group_18.csv")





