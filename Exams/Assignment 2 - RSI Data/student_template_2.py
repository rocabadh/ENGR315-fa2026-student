"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

#Importing needed packages
import os

import numpy as np
import pandas as pd
from scipy import stats 
import matplotlib.pyplot as plt

#Setting the function that turns the dataset into a dataframe
def load_dataset() -> pd.DataFrame:
    """
    Locates and imports the RSI dataset using a relative file path.
    :return: Dataset loaded into a dataframe.
    """
    return pd.read_csv("data/drop-jump/all_participant_data_rsi.csv")

#Setting the function that answers task 1
def task_1(df: pd.DataFrame):
    """
    Completes a paired-sample t-test that compares all the force plate and accelerometer RSI values.

    :param df: A dataframe that contains force plate and accelerometer RSI values.
    :return: none 
    """

    #Fixed alpha value
    alpha = 0.05

    #Isolate the force plate and accelerometer data
    force_plate= df["force_plate_rsi"]
    accelerometer= df["accelerometer_rsi"]

    #Calculate paired t-test
    t_stat, p_val = stats.ttest_rel(force_plate, accelerometer)

    #Stating hypotheses
    null_hyp="There is no significant mean difference betweem the force plate and accelerometer RSI values."
    alt_hyp="There is a significant mean difference between the force plate and accelerometer RSI values."

    #Determine whether to accept or reject the null hypothesis
    if p_val < alpha:
        decision = "Reject the null hypothesis"
    else:
        decision= "Fail to reject the null hypothesis"

    #Print results
    print("Task 1 Results:")
    print(f"Null Hypothesis: {null_hyp}")
    print(f"Alternative Hypothesis: {alt_hyp}")
    print(f"T-Value: {t_stat}")
    print(f"P-Value: {p_val}")
    print(f"Conclusion: {decision}")

#Setting the function that answers task 2
def task_2(df: pd.dataframe):
    """
    Fits a normal distribution to the accelerometer RSI values, performs a Chi-Square test, and plots a histogram with the normal distrivution overlaid on top. 

    :param df: A dataframe that constains the accelerometer RSI values,
    :return: none
    """

    #Fixed alpha 
    alpha=0.05

    #Isolate accelerometer RSI data
    accelerometer=df["accelerometer_rsi"]

    #Fit a normal distribution to find sample mean (mu) and standard deviation (sigma)
    mu, sigma =stats.norm.fit(accelerometer)

    #set up bins for Chi-Squared Test  

    