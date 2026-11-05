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
    Completes a paired-sample t-test that compares all the force plate 
    and accelerometer RSI values.

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
def task_2(df: pd.DataFrame):
    """
    Fits a normal distribution to the accelerometer RSI values, performs a 
    Chi-Square test, and plots a histogram with the normal distrivution
    overlaid on top. 

    :param df: A dataframe that constains the accelerometer RSI values,
    :return: none
    """

    #Fixed alpha 
    alpha=0.05

    #Isolate accelerometer RSI data into array
    accelerometer=df["accelerometer_rsi"].to_numpy()

    #Fit a normal distribution to find sample mean (mu) and standard deviation (sigma)
    mu, sigma =stats.norm.fit(accelerometer)

    #Finding length of array
    n=len(accelerometer)

    #set up bins for Chi-Squared Test  
    num_bins=max(4, n//8)

    #Spread bins 
    bins=np.linspace(mu-2*sigma, mu+2*sigma, num_bins+1)

    #Set endpoints to capture outliers
    bins[0]=-np.inf
    bins[-1]=np.inf

    #Expected count by normal CDF
    bin_probabilities= np.diff(stats.norm.cdf(bins, loc=mu,scale=sigma))
    expected=bin_probabilities*n

    #Observed count
    observed,_=np.histogram(accelerometer, bins=bins)

    #Chi-Squared Test
    chi2_stat, p_value=stats.chisquare(f_obs=observed, f_exp=expected, ddof=2)

    #Prove or disprove hypothesis 
    if p_value < alpha:
        assessment= "Not a good fit (Rejects Null Hypothesis)"
    else:
        assessment ="Good fit (Fail to Reject Null Hypothesis)"

    #Print results
    print("Task 2 Results:")
    print(f"Chi2 Stat: {chi2_stat}")
    print(f"P-Value: {p_value}")
    print(f"Goodness of Fit: {assessment}")

    #Plot figure
    plt.figure(figsize=(8,5))

    #Observed histogram
    plt.his(accelerometer, bins=15, density=True, edgecolor="black", label="Observed Data")

    #X-axis range generated based on data bounds
    x=np.linspace(accelerometer.min()-0.1,accelerometer.max()+0.1,500)
    y=stats.norm.pdf(x,loc=mu,scale=sigma)
    plt.plot(x,y,color="red",linewidth=2, label="Fitted Normal Curve")
    
    #Give histogram axis labels, title, lengend, and display
    plt.title("Accelerometer RSI Distribution with a Normal Fit")
    plt.xlabel("Accelerometer RSI")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True, linestyle="--")
    plt.show()

#Setting the function that answers task 3
def task_3(df: pd.DataFrame):
    """ 
    Filters the dataframe for trials from participant F, 
    prints the new dataframe, and calulates a 95% confidence
    interval for both force plate and accelerometer RSI.
    
    :param df: Total RSI DataFram
    :return: none
    """

    #Setting confidence level
    confidence=0.95

    #Filter dataframe for participant F
    f_df=df[df["trials"].str.startswith(F_).copy()]

    #Turn force plate and accelerometer RSI into an array
    fp_array= f_df["force_plate_rsi"].to_numpy()
    accel_array=f_df["accelerometer_rsi"].to_numpy()

    #Find mean and standard errer of mean
    fp_mean=np.mean(fp_array)
    fp_sem=stats.sem(fp_array)
    accel_mean=np.mean(accel_array)
    accel_sem=stats.sem(accel_array)

    #find length of both arrays
    n_fp=len(fp_array)
    n_accel=len(accel_array)

    #Calculate 95% confidence interval
    fp_ci=stats.t.interval(confidence=confidence, df=n_fp-1, loc=fp_mean, scale=fp_sem)
    accel_ci=stats.t.interval(confidence=confidence, df=n_accel-1, loc=accel_mean, scale=accel_sem)
  
    #Print task 3 results
    print("Task 3 Results:")
    print("Force Plate RSI:")
    print(f"Mean= {fp_mean}")
    print(f"95% Confience Interval= [{fp_ci[0]},{fp_ci[1]}]")
    print("Accelerometer RSI:")
    print(f"Mean= {accel_mean}")
    print(f"95% Confience Interval= [{accel_ci[0]},{accel_ci[1]}]")
    print("Participant F DataFrame=")
    print(f_df.to_string)

#Execution 
if __name__=="__main__":
    #Load data 
    df=load_data()

    #Complete all tasks
    task_1(df)
    task_2(df)
    task_3(df)