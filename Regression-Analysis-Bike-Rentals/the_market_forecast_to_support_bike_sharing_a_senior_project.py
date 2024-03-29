# -*- coding: utf-8 -*-
"""The Market Forecast to Support Bike Sharing: A Senior Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11tCSsW5_ThRXqtiO0I75Pd5IpRFYQQoc

**Initial Preparations**

# Import necessary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_regression
from sklearn.inspection import permutation_importance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import skew
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error

import warnings
warnings.filterwarnings("ignore")

"""# Load the dataset"""

file_path = "/content/SeoulBikeData.csv"
data = pd.read_csv(file_path)

"""EDA:"""

# Display the first few rows of the dataset
print(data.head())

# Display the last 5 observations of the dataset
print(data.tail())

# Display the shape of the dataset
print(data.shape)

# Display the list of columns in the dataframe
print(data.columns)

# Display the statistical description of the dataframe
print(data.describe())

# Display a concise summary of the dataframe
print(data.info())

# Creating a function to return all the unique values each categorical column can have
def cat_unique_vals(cat_cols, df):
    for col in cat_cols:
        print("The values that the categorical column", col, "can take are:", df[col].unique())

# Checking the possible values important and meaningful categorical columns can have.
categorical_columns = ['Seasons', 'Holiday']
cat_unique_vals(categorical_columns, data)

# Creating a function that performs a groupby operation and returns a dataframe for analysis
def create_df_analysis(col):
    return data.groupby(col)['Rented Bike Count'].sum().reset_index()

# Example usage:
analysis_df_seasons = create_df_analysis('Seasons')
analysis_df_holiday = create_df_analysis('Holiday')

# Display the resulting dataframes
print("Analysis DataFrame for Seasons:")
print(analysis_df_seasons)

print("\nAnalysis DataFrame for Holiday:")
print(analysis_df_holiday)

# Seasons column analysis
seasons_col = create_df_analysis('Seasons')
print(seasons_col)



"""#Creating a visualisation for the seasons column

"""

plt.figure(figsize=(10, 7))
splot = sns.barplot(data=seasons_col, x='Seasons', y='Rented Bike Count')

"""# Annotating each bar with the count"""

for p in splot.patches:
    splot.annotate(format(p.get_height(), '.1f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   xytext=(0, 9),
                   textcoords='offset points')

plt.xlabel("Seasons", size=14)
plt.ylabel("Rented Bike Count", size=14)
plt.title("Rented Bike Count by Seasons", size=16)
plt.show()

# Initial preparations for plotting a pie chart with percentages
seasons_list = list(seasons_col['Seasons'])
rented_count_list = list(seasons_col['Rented Bike Count'])
palette_color = sns.color_palette('bright')
explode = (0.05, 0.05, 0.05, 0.05)

# Creating the pie chart visualization for the Seasons column
plt.figure(figsize=(5, 5))
plt.pie(rented_count_list, labels=seasons_list, colors=palette_color, explode=explode, autopct='%0.0f%%')
plt.title("Percentage of total number of bikes rented for each season")
plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

"""
**Bicycle Rental Statistics**

• Summer: Highest bike rental (37%), likely due to vacation mood and increased tourists.

• Winter: Lowest bike rental (8%)."""

# Holidays column analysis
holidays_col = create_df_analysis('Holiday')
print(holidays_col)

# Creating a visualization for the Holidays column
plt.figure(figsize=(7, 7))
splot = sns.barplot(data=holidays_col, x='Holiday', y='Rented Bike Count')

# Annotating each bar with the count
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.1f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   xytext=(0, 9),
                   textcoords='offset points')

plt.xlabel("Holiday variable", size=14)
plt.ylabel("Rented Bike Count", size=14)
plt.title("Rented Bike Count for Holidays", size=16)
plt.show()

"""The majority of bikes rented are on non-holiday days, requiring analysis for varying temperatures."""

print(data.columns)

# Execute the create_df_analysis function for Temperature
temp_bike = create_df_analysis('Temperature(?)')

# Display the resulting DataFrame
print(temp_bike)

# Creating a visualization for the Temperature vs. Rented Bike Count analysis
plt.figure(figsize=(10, 7))
splot = sns.barplot(data=temp_bike, x='Temperature(?)', y='Rented Bike Count')

# Annotating each bar with the count
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.1f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   xytext=(0, 9),
                   textcoords='offset points')

plt.xlabel("Temperature (?)", size=14)
plt.ylabel("Rented Bike Count", size=14)
plt.title("Rented Bike Count for Different Temperatures", size=16)
plt.show()

# Creating a line plot for the Temperature vs. Rented Bike Count analysis
plt.figure(figsize=(10, 7))
plt.plot(temp_bike['Temperature(?)'], temp_bike['Rented Bike Count'], marker='o', linestyle='-')

plt.xlabel("Temperature (?)", size=14)
plt.ylabel("Rented Bike Count", size=14)
plt.title("Rented Bike Count for Different Temperatures", size=16)
plt.grid(True)
plt.show()

# Display the list of columns in the dataframe
print(temp_bike.columns)

# Creating a scatter plot for different temperatures and rented bike count
plt.figure(figsize=(10, 7))
sns.scatterplot(data=temp_bike, x='Temperature(?)', y='Rented Bike Count')
plt.title('Number of bikes rented for different temperatures', size=15)
plt.xlabel('Temperature (°C)', size=14)
plt.ylabel('Rented Bike Count', size=14)
plt.show()

"""As we can see that the most number of bikes rented are in the temperature range of 15 degrees to 30 degrees.

Analysing for different intensities of snowfal
"""

# Creating a dataframe to analyze the number of bikes rented for different intensities of snowfall
snowfall_bike = create_df_analysis('Snowfall (cm)')

# Displaying the first few rows of the resulting DataFrame
snowfall_bike.head()

# Creating a scatter plot for different snowfall intensities and rented bike count
plt.scatter(data=snowfall_bike, x='Snowfall (cm)', y='Rented Bike Count')
plt.title('Number of bikes rented across different snowfall intensities', size=10)
plt.xlabel('Snowfall in cm')
plt.ylabel('Rented Bike Count')
plt.show()

"""Analysing for different intensities of rainfall"""

#Creating a dataframe to analyse the number of bikes rented for different intensities of rainfall
rainfall_bike = create_df_analysis('Rainfall(mm)')
rainfall_bike.head()

#Creating a visualisation for different rainfall intensities
plt.scatter(data=rainfall_bike,x='Rainfall(mm)',y='Rented Bike Count')
plt.title('Number of bikes rented across different rainfall intensities',size=10)
plt.xlabel('Rainfall in mm')
plt.ylabel('Rented Bike Count')
plt.show()

"""Here, we can observe that the majority of the bikes are hired during the complete absence of snowfall. Rainfall yields a similar result: when there is no rainfall, the greatest number of bikes are leased.

Note: Because the y axis in both cases is of order 10 to the power 6, it is not very noticeable that the lower numbers are lower.

examining data for various amounts of humidity

"""

#Creating a dataframe for analysing the number of bikes rented for different humidity percentages.
humidity_bike = create_df_analysis('Humidity(%)')
humidity_bike

#Plotting a visualisation for the different humidity percentages
plt.plot(humidity_bike['Humidity(%)'],humidity_bike['Rented Bike Count'])
plt.xlabel('Humidity(%)')
plt.ylabel("Rented Bike Count")
plt.title("Number of bikes rented across different humidity percentages")
plt.show()

"""It is evident that most of the bikes are hired at a humidity fraction between 30 and 70.

"""

#Creating a dataframe to analyse the number of bikes rented for different hours of the day
hour_df = create_df_analysis("Hour")
hour_df

#Creating a visualisation for different hours of the day
plt.figure(figsize=(7,7))
sns.barplot(data=hour_df,x='Hour',y='Rented Bike Count')
plt.title('Number of bikes rented across different hours of the day',size=15)
plt.xlabel('Hour',size=12)
plt.ylabel('Rented Bike Count',size=12)
plt.show()

"""This shows that the 18th hour, or 6 p.m., saw the most bike rentals, while the 4th hour, or 4 a.m., saw the fewest."""

#Creating a dataframe to analyse the number of bikes rented for different visibility rates
visibility_bike = create_df_analysis('Visibility (10m)')
visibility_bike

#Creating a visualisation for number of bikes rented in different visibility ranges
plt.plot(visibility_bike['Visibility (10m)'],visibility_bike['Rented Bike Count'])
plt.xlabel('Visibility(10m)')
plt.ylabel('Rented Bike Count')
plt.title('Number of bikes rented for different visibility')
plt.show()

"""We can see that higher visibility is preffered by the customers. Through further analysis of the visibility_bike dataframe we can see that for increasing visibility there is an increase in bikes rented

**Clean Up:**
Managing null values: In a particular dataset, missing data refers to values or information that are either not stored in the dataset or are not available.

Missing values have the potential to skew machine learning model outcomes and/or lower model accuracy.

As a result, handling null values before training our model is crucial. Null values can be handled in two primary ways: either all the observations containing the null values are deleted, or the null values are imputed with some meaningful complete values.
"""

# Checking for null values in the data DataFrame
data.isnull().sum()

"""As we can see there are no null values present in our dataset and therefore we are good to go.

Handling duplicate values:
When two features have the same set of values they are known as duplicate values.

Duplicate values can cause detrimental effect on our accuracy. Duplicate values can ruin the split between train,test and validation set, which ultimately leads to a biased performance estimates that disappoint the model in production.

The best way of dealing with duplicate values is to delete them.


"""

# Checking for duplicate values in the data DataFrame
data.duplicated().sum()

"""As we can see there are no duplicate values, so we can move ahead

**Eliminating anomalies:**
Data points that differ noticeably from the remainder of the dataset's data points are known as outliers. These may bias the data and compromise the ML model's accuracy.
"""

# Creating a list of columns that can possibly contain outliers
possible_outlier_cols = list(set(data.describe().columns) - {'Rented Bike Count', 'Hour'})

# Creating box plots for columns that can possibly contain outliers
plt.figure(figsize=(15, 8))

num_cols = len(possible_outlier_cols)
num_rows = (num_cols // 3) + (num_cols % 3 > 0)

for i, column in enumerate(possible_outlier_cols, 1):
    plt.subplot(num_rows, 3, i)
    sns.boxplot(x=data[column])
    plt.title(f'Boxplot of {column}')

plt.tight_layout()
plt.show()

"""As we can see, the columns with outliers in them are Windspeed, Solar Radiation, Rainfall, and Snowfall.

"""

# Assuming 'outlier_cols' is the list of columns with possible outliers
Q1 = data[outlier_cols].quantile(0.25)
Q3 = data[outlier_cols].quantile(0.75)
IQR = Q3 - Q1

# Displaying the calculated inter-quartile range
IQR

#Calculating the upper and lower fence for outlier removal
u_fence = Q3 + (1.5*IQR)
l_fence = Q1 - (1.5*IQR)

# Assuming 'outlier_cols' is the list of columns with possible outliers
for column in outlier_cols:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    # Calculate lower and upper fences
    l_fence = Q1 - 1.5 * IQR
    u_fence = Q3 + 1.5 * IQR

    # Remove outliers
    data = data[~((data[column] < l_fence) | (data[column] > u_fence))]

# Checking the number of outliers deleted
data.info()

"""Some null values have been created in these 4 columns as a result of outlier deletion.At this point, we have the option to either impute meaningful full values or delete the observations that have null values. I'll be imputing the median value of each column to them in this instance.

Keep in mind that The mean is typically used to impute null values, but since the median is less affected by outliers than the mean, I'll go with the latter.
"""

def impute_null(columns):
    for column in columns:
        # Your imputation logic here (e.g., filling null values with mean, median, or any other strategy)
        data[column].fillna(data[column].mean(), inplace=True)

# Checking if the imputation is successful
data.info()

# Checking for null values after imputation
data.isnull().sum()

"""The imputation is successful and therefore we have handled the outliers successfully

4.Feature Engineering: Encoding Features: Since machine learning models are limited to numerical values, it is necessary to translate or encode significant categorical columns into numerical variables. Feature encoding is the term for this procedure.

The Seasons, Holiday, and Functioning Day columns are the three that need to be encoded in this instance.
"""

# Encoding for the Seasons column using get_dummies
data = pd.get_dummies(data, columns=['Seasons'], prefix='', prefix_sep='')

# Optional: Drop the original 'Seasons' column if needed
# data.drop('Seasons', axis=1, inplace=True)

print(data.columns)

print(data.head())

# Display the list of columns in the dataframe
print(data.columns)

# Removing 'Seasons' column if present
if 'Seasons' in data.columns:
    data.drop(columns=['Seasons'], axis=1, inplace=True)

# Encoding for 'Holiday' column
data['Holiday'] = np.where(data['Holiday'] == 'Holiday', 1, 0)

# Encoding for 'Functioning Day'
data['Functioning Day'] = np.where(data['Functioning Day'] == 'Yes', 1, 0)

# Displaying the modified DataFrame
data.head()

"""**Checking correlation for feature removal:**"""

# Assuming data is the DataFrame containing your data
corr_matrix = data.corr()

# Plotting the correlation matrix heatmap
plt.figure(figsize=(15, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation between the variables of the Bike Sharing dataset')
plt.show()

"""We will drop the dew point temperature column since it has a strong correlation with the temperature column and can be removed without significantly affecting our model construction.

I will also remove the date column because I don't think it adds any value.
"""

# Assuming your DataFrame is named 'data'
columns_to_drop = ['Dew point temperature(?)', 'Date']

# Check if the columns exist before dropping them
for column in columns_to_drop:
    if column in data.columns:
        data.drop(columns=column, axis=1, inplace=True)

# Displaying the modified DataFrame
print(data.columns)

"""**Removing Multicollinearity:**

Two independent variables that have a strong correlation with one another are said to be multicollinear.


Regression model accuracy is impacted by multicollinearity, thus we will determine whether multicollinearity exists in our dataset and address it by eliminating the contributing columns.

Note: I'll use the variance inflation factor to determine whether our dataset is multicollinear. Less than ten is the accepted VIF.
"""

import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Assuming bike_sharing_df is your DataFrame, you should load it before using calc_vif
bike_sharing_df = pd.read_csv('/content/SeoulBikeData.csv')  # Replace 'your_dataset.csv' with your actual file path

# Creating a list of independent columns
idv_cols = list(set(bike_sharing_df.columns) - {'Rented Bike Count'})

# Creating a function to calculate the variance inflation factor (VIF)
def calc_vif(X):
    vif = pd.DataFrame()
    vif["Columns"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

# Converting DataFrame to numeric
bike_sharing_df_numeric = bike_sharing_df.apply(pd.to_numeric, errors='coerce')

# Handling missing values and infinity
bike_sharing_df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
bike_sharing_df_numeric.dropna(inplace=True)

# Check if there are still rows left after handling missing values
if bike_sharing_df_numeric.shape[0] == 0:
    print("No data left after handling missing values. Please check your input data.")
else:
    # Calculating the VIF for independent columns
    vif_result = calc_vif(bike_sharing_df_numeric[idv_cols])

    # Displaying the VIF results
    print(vif_result)

# Assuming bike_sharing_df is the DataFrame containing your data
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Display the list of columns in the dataframe
print(bike_sharing_df.columns)

# Removing 'Seasons' column if present
if 'Seasons' in bike_sharing_df.columns:
    bike_sharing_df.drop(columns=['Seasons'], axis=1, inplace=True)

# Encoding for 'Holiday' column
bike_sharing_df['Holiday'] = np.where(bike_sharing_df['Holiday'] == 'Holiday', 1, 0)

# Encoding for 'Functioning Day'
bike_sharing_df['Functioning Day'] = np.where(bike_sharing_df['Functioning Day'] == 'Yes', 1, 0)

# Displaying the modified DataFrame
print(bike_sharing_df.head())

# Plotting correlation matrix using sns.heatmap
import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = bike_sharing_df.corr()
plt.figure(figsize=(15, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation between the variables of Bike Sharing df')
plt.show()

# Removing unnecessary columns
columns_to_drop = ['Dew point temperature(?)', 'Date']
for column in columns_to_drop:
    if column in bike_sharing_df.columns:
        bike_sharing_df.drop(columns=column, axis=1, inplace=True)

# Encoding for Seasons column
bike_sharing_df['Winter'] = np.where(bike_sharing_df['Seasons'] == 'Winter', 1, 0)
bike_sharing_df['Spring'] = np.where(bike_sharing_df['Seasons'] == 'Spring', 1, 0)
bike_sharing_df['Summer'] = np.where(bike_sharing_df['Seasons'] == 'Summer', 1, 0)
bike_sharing_df['Autumn'] = np.where(bike_sharing_df['Seasons'] == 'Autumn', 1, 0)

# Removing Seasons column since we don't require it now.
bike_sharing_df.drop(columns=['Seasons'], axis=1, inplace=True)

# Encoding for Holiday column
bike_sharing_df['Holiday'] = np.where(bike_sharing_df['Holiday'] == 'Holiday', 1, 0)

# Encoding for Functioning day
bike_sharing_df['Functioning Day'] = np.where(bike_sharing_df['Functioning Day'] == 'Yes', 1, 0)

# Displaying the modified DataFrame
print(bike_sharing_df.head())

# Creating a list of independent columns
idv_cols = list(set(bike_sharing_df.columns) - {'Rented Bike Count'})

# Creating a function to calculate the variance inflation factor(VIF)
def calc_vif(X):
    vif = pd.DataFrame()
    vif["Columns"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

# Calculating the VIF for independent columns
vif_result = calc_vif(bike_sharing_df[idv_cols])
print(vif_result)

# Continue with VIF calculation if there is data left
if bike_sharing_df_numeric.shape[0] > 0:
    # Creating a list of independent columns
    idv_cols = list(set(bike_sharing_df_numeric.columns) - {'Rented Bike Count'})

    # Creating a function to calculate the variance inflation factor(VIF)
    def calc_vif(X):
        vif = pd.DataFrame()
        vif["Columns"] = X.columns
        vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        return vif

    # Calculating the VIF for independent columns
    vif_result = calc_vif(bike_sharing_df_numeric[idv_cols])

    # Displaying the VIF results
    print("VIF Results:")
    print(vif_result)
else:
    print("No data left after handling missing values. Please check your input data.")

#Creating a list of independent columns
idv_cols = list(set(bike_sharing_df.columns)-{'Rented Bike Count'})
#Creating a function to calculate the variance inflation factor(VIF)
def calc_vif(X):
    vif = pd.DataFrame()
    vif["Columns"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return(vif)
#Calculating the VIF for independent columns
calc_vif(bike_sharing_df[idv_cols])

"""We can see that the seasons encoding have very high VIF therefore we will eliminate one of the columns. We will drop winter because it has the lowest bikes rented. The columns Rainfall and Snowfall have no VIF at all so we will drop them too."""

# Creating a list of independent columns
idv_cols = list(set(bike_sharing_df.columns) - {'Rented Bike Count'})

# Creating a function to calculate the variance inflation factor(VIF)
def calc_vif(X):
    vif = pd.DataFrame()
    vif["Columns"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

# Dropping the unnecessary columns
columns_to_drop = {'Winter', 'Rainfall(mm)', 'Snowfall (cm)'}
columns_to_drop = {col for col in columns_to_drop if col in bike_sharing_df.columns}
bike_sharing_df.drop(columns=columns_to_drop, axis=1, inplace=True)

# Creating a list of remaining independent columns
idv_cols = list(set(bike_sharing_df.columns) - {'Rented Bike Count'})

# Calculating VIF for remaining independent columns
calc_vif(bike_sharing_df[idv_cols])

# Dropping the Functioning Day column
bike_sharing_df.drop(columns={'Functioning Day'}, axis=1, inplace=True)

# Creating a list with remaining independent columns
idv_cols = list(set(bike_sharing_df.columns) - {'Rented Bike Count'})

# Calculating the VIF for remaining independent columns
calc_vif(bike_sharing_df[idv_cols])

"""Now that we don't have any variable with VIF>10 we can move ahead.

**Obtaining correlation between independent and dependent variables:**

To determine this link, a regression plot will be utilized. This ascertains whether there is a linear relationship between the independent and dependent variables, which is a prerequisite for models such as linear regression.
"""

#printing the regression plot for all the numerical features
for col in idv_cols:
  fig,ax=plt.subplots(figsize=(10,6))
  sns.regplot(x=bike_sharing_df[col],y=bike_sharing_df['Rented Bike Count'],scatter_kws={"color": 'blue'}, line_kws={"color": "black"})
  corr=bike_sharing_df[col].corr(bike_sharing_df['Rented Bike Count'])
  ax.set_title('Column'+ col+'vs Rented Bike Count - correlation:'+str(corr))

"""As you can see, the dependent variable and every other column we have have a linear connection. We are consequently set to proceed as we have met the supposition.

**Pre-processing of the data:**
"""

#Creating the dataset for independent and dependent variables
X = bike_sharing_df.drop(columns={'Rented Bike Count'},axis=1)
Y = bike_sharing_df['Rented Bike Count']

#First look of the independent variable dataset
X.head()

#First look of the dependent variable dataset
Y.head()

"""**Target feature conditioning:**

The distribution of the target feature is observed and in this case because it is a positively skewed distribution it is normalised using square root transformation.
"""

# Checking for the distribution of the Target variable
plt.figure(figsize=(10, 7))
plt.title("Distribution of the target variable: Rented Bike Count. Skewness=" + str((bike_sharing_df['Rented Bike Count'])))
sns.histplot(data=bike_sharing_df, x='Rented Bike Count')
plt.show()

#Applying square root transformation on the dependent variable
Y = np.sqrt(Y)

#Creating a dataframe with values of Y for visualisation purposes
vis_Y = Y.reset_index()

#Checking how well the square root transformation has worked
plt.figure(figsize=(10,7))
plt.title("Distribution of the target variable: Rented Bike Count. Skewness="+str((vis_Y['Rented Bike Count'])))
sns.histplot(data=vis_Y,x='Rented Bike Count')
plt.show()

"""**Creating the test and train dataset:**

**We can see that the target variable has been normalised and we are good to go.**
"""

from sklearn.model_selection import train_test_split

#Splitting the dataset into test and train datasets
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.25,random_state=0)

#Shape of the train set of the independent values
X_train.shape

#Shape of the test set of the independent values
X_test.shape

"""**Feature Scaling:**
Feature Scaling is a technique to standardize the independent features present in the data in a fixed range. It is performed during the data pre-processing to handle highly varying magnitudes or values or units. If feature scaling is not done, then a machine learning algorithm tends to weigh greater values, higher and consider smaller values as the lower values, regardless of the unit of the values.

Two ways of feature scaling:

Min max normalization

Standardisation

In this project I'm going to use the standardisation method with the help of the StandardScaler() function.
"""

from sklearn.preprocessing import StandardScaler

#Creating object for the StandardScaler function
scaler = StandardScaler()

#Creating object for the StandardScaler function
scaler = StandardScaler()
#Standardizing the independent variables
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

#Overview of what a dataframe looks like after standardizing
X_train

"""#**Model Implementation**
Programs that are trained to identify patterns or trends in data and forecast the outcome for fresh data are known as machine learning models.

Regression models will be utilized in this project since it involves a regression problem. Polynomial and linear regression are two common examples.

The following models will be included in this project:


**Linear regression**
Ridge regression refers to L2 regularized linear regression.

L1 regularization in linear regression is known as Lasso regression.
regression using random forests.


"""



"""#**Regression using a linear model:**

As stated earlier linear regression is a regression technique, and it comes under supervised learning. Linear regression performs the task to predict a dependent variable value (y) based on a given independent variable value (x). So, this regression technique finds out a linear relationship between x (input) and y(output)

Programs that are trained to identify patterns or trends in data and forecast the outcome for fresh data are known as machine learning models.

Regression models will be utilized in this project since it involves a regression problem. Polynomial and linear regression are two common examples.

The following models will be included in this project:

Regression in line.
Ridge regression refers to L2 regularized linear regression.
L1 regularization in linear regression is known as Lasso regression.
Regression with random forests

#Linear regression:
As stated earlier linear regression is a regression technique, and it comes under supervised learning. Linear regression performs the task to predict a dependent variable value (y) based on a given independent variable value (x). So, this regression technique finds out a linear relationship between x (input) and y(output)
"""

from sklearn.linear_model import LinearRegression

#Training the linear regression model
lr_model = LinearRegression().fit(X_train,Y_train)

#Checking the score of the linear regression model
lr_model.score(X_train,Y_train)

#Checking the coefficient values of the linear regression model
lr_model.coef_

#Predicting the value of the dependent variable for train and test dataset
Y_train_pred_lr = lr_model.predict(X_train)
Y_test_pred_lr = lr_model.predict(X_test)

#Creating a function to plot the comparison between actual values and predictions
def plot_comparison(y_pred,model):
   plt.figure(figsize=(10,7))
   plt.title("The comparison of actual values and predictions obtained by "+model)
   plt.plot(np.array((Y_test)))
   plt.plot((y_pred),color='red')
   plt.legend(["Actual","Predicted"])
   plt.show()

#Plotting the comparison between actual and predicted values obtained by Linear Regression
plot_comparison(Y_test_pred_lr,'Linear Regression')

#Creating a function to calculate and display the evaluation metrics for the model
def eval_metrics(y_pred,model):
  print("The evaluation metrics for "+model+" are given as:")
  MSE  = mean_squared_error(Y_test,y_pred)      #Mean squared error for test set
  print("MSE :" , MSE)

  RMSE = np.sqrt(MSE)
  print("RMSE :" ,RMSE)

  r2_test = r2_score(Y_test,y_pred)             #r2 score for prediction on test set
  print("R2 :" ,r2_test)

  a_r2_test = 1-(1-r2_score(Y_test,y_pred))*((X_test.shape[0]-1)/(X_test.shape[0]-X_test.shape[1]-1))     #adjusted r2 score for test set
  print("Adjusted R2 :",a_r2_test)

from sklearn.metrics import mean_squared_error

from sklearn.metrics import r2_score

#Calculating the evaluation metrics for Linear Regression
eval_metrics(Y_test_pred_lr,'Linear Regression')

"""#Ridge Regression:
Ridge regression is a method of estimating the coefficients of regression models in scenarios where the independent variables are highly correlated. It uses the linear regression model with the L2 regularization method.
"""

from sklearn.linear_model import Ridge

from sklearn.model_selection import GridSearchCV

#Training the ridge regression model using GridSearchCV
ridge = Ridge()
parameters = {'alpha': [1,0.001,10,20,35,60,70,100,800,1200]}
ridge_model_grid = GridSearchCV(ridge, parameters, scoring='neg_mean_squared_error', cv=3)
ridge_model_grid.fit(X_train,Y_train)

#Getting the best parameters for Ridge regression fetched through GridSearchCV
print(f'The best value for alpha in ridge regression through GridSearchCV is found to be {ridge_model_grid.best_params_}')
print(f'\nUsing {ridge_model_grid.best_params_} as the value for aplha gives us a negative mean squared error of: {ridge_model_grid.best_score_}')

#Fitting the Ridge regression model on the dataset with appropriate alpha value
ridge_model=Ridge(alpha=35).fit(X_train,Y_train)

#Predicting values of the independent variable on the test set
Y_test_pred_ridge = ridge_model.predict(X_test)

#Plotting the comparison between actual and predicted values obtained by Ridge Regression
plot_comparison(Y_test_pred_ridge,'Ridge Regression')

#Calculating the evaluation metrics for Ridge Regression
eval_metrics(Y_test_pred_ridge,'Ridge Regression')

"""As far as we observe, there is not much of a difference between the outcomes obtained with Ridge regression and Linear regression.

#**Lasso Regression:**
Lasso regression analysis is a shrinkage and variable selection method for linear regression models. The goal of lasso regression is to obtain the subset of predictors that minimizes prediction error for a quantitative response variable. It uses the Linear regression model with L1 regularization.
"""

from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV

#Creating a Lasso regression model using GridSearchCV
lasso = Lasso()
parameters = {'alpha': [0.8,1,10,20,40,80,100,300,700,1000]}
lasso_model_grid = GridSearchCV(lasso, parameters, scoring='neg_mean_squared_error', cv=5)
lasso_model_grid.fit(X_train, Y_train)

#Getting the best parameters for Lasso regression fetched through GridSearchCV
print(f'The best value for alpha in ridge regression through GridSearchCV is found to be {lasso_model_grid.best_params_}')
print(f'\nUsing {lasso_model_grid.best_params_} as the value for aplha gives us a negative mean squared error of: {lasso_model_grid.best_score_}')

#Fitting the Ridge regression model on the dataset with appropriate alpha value
lasso_model=Lasso(alpha=0.8).fit(X_train,Y_train)

#Predicting values of the independent variable on the test set
Y_test_pred_lasso = lasso_model.predict(X_test)

#Plotting the comparison between actual and predicted values obtained by Lasso Regression
plot_comparison(Y_test_pred_lasso,'Lasso Regression')

import matplotlib.pyplot as plt

def plot_comparison(y_pred, model_name):
    plt.figure(figsize=(10, 6))
    plt.scatter(Y_test, y_pred, color='blue', edgecolors=(0, 0, 0), alpha=0.7)
    plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'k--', lw=2)
    plt.title(f'Comparison between Actual and Predicted values ({model_name})')
    plt.xlabel('Actual values')
    plt.ylabel('Predicted values')
    plt.show()

# Assuming Y_test_pred_lasso is the predicted values obtained by Lasso Regression
plot_comparison(Y_test_pred_lasso, 'Lasso Regression')

# Calculating the evaluation metrics for Lasso Regression
eval_metrics(Y_test_pred_lasso, 'Lasso Regression')

"""The model quality has depreciated by using the lasso regression method.

#Random Forest Regression:
A random forest is a meta estimator that fits a number of classifying decision trees on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting
"""

from sklearn.ensemble import RandomForestRegressor

#Creating a Random Forest Regression model using GridSearchCV
rand_forest = RandomForestRegressor()


parameters = {'n_estimators' : [int(x) for x in np.linspace(start=10,stop=20, num=5)],
             'max_depth' : [10,15,20],
             'min_samples_split':[2,4],
             'min_samples_leaf':[1,2],
             'bootstrap' : [True,False]
             }

rf_model_grid = GridSearchCV(rand_forest,parameters,scoring='r2',cv=5)
rf_model_grid.fit(X_train,Y_train)

#Getting the best parameters for Random Forest regression fetched through GridSearchCV
print(f'The best value for parameters in random forest regression through GridSearchCV is found to be {rf_model_grid.best_params_}')
print(f'\nUsing {rf_model_grid.best_params_} as the value for the parameters in random forest model, it gives us a negative mean squared error of: {rf_model_grid.best_score_}')

#Fitting Random Forest model on the dataset with appropriate paramter values
rf_model = RandomForestRegressor(bootstrap=True,max_depth=20,min_samples_leaf=2,min_samples_split=4,n_estimators=15).fit(X_train,Y_train)
#Predicting values of the independent variable on the test set
Y_test_pred_rf = rf_model.predict(X_test)
#Plotting the comparison between actual and predicted values obtained by Random Forest Regression
plot_comparison(Y_test_pred_rf,'Random Forest Regression')

#Calculating the evaluation metrics for Random Forest Regression
eval_metrics(Y_test_pred_rf,'Random Forest Regression')

"""As each of us are able to observe, there has been a significant improvement in model prediction quality.

#Model Explainability:
Model explainability refers to the concept of being able to understand the machine learning model. For example – If a healthcare model is predicting whether a patient is suffering from a particular disease or not. The medical practitioners need to know what parameters the model is taking into account or if the model contains any bias. So, it is necessary that once the model is deployed in the real world. Then, the model developers can explain the model.

Popular techniques for model explainability:

LIME
SHAP
ELI-5
In this project I'll be using SHAP for model explainability. Among the various methods in SHAP I'll be using the SHAP summary plot, which plots features/columns in order of their impact on the predictions and also plots the SHAP values.
"""

#Installing the shap library
!pip install shap

#Initialising javascript for visualisation of SHAP
import shap

#Creating a function to plot the shap summary plot
def shap_summary(model):
   explainer_shap = shap.Explainer(model=model, masker=X_train)
   shap_values = explainer_shap.shap_values(X_train)
   shap.summary_plot(shap_values,X_train,feature_names=X.columns)

#Plotting shap summary plot for linear regression
shap_summary(lr_model)

#Plotting shap summary plot for Ridge regression
shap_summary(ridge_model)

#Plotting shap summary plot for Lasso regression
shap_summary(lasso_model)

#Plotting shap summary plot for Random forest regression model
explainer_shap = shap.Explainer(model=rf_model, masker=X_train)
shap_values = explainer_shap.shap_values(X_train,check_additivity=False)
shap.summary_plot(shap_values,X_train,feature_names=X.columns)

"""We can observe that each model assigns a different weight or impact power to the features, which determines how well the model predicts. Random forest outperforms the other four models because it gives nearly all of the features a considerable influence power.

Understanding the SHAP values allows us to determine the feature relevance and impact power by examining the SHAP summary plot for each model.

#In conclusion

 EDA observations show that the summer months see the highest number of bike rentals, while the winter months see the lowest number.

On days that are not observed as holidays, more than 96% of the motorcycles are rented.
The majority of bikes that are hired are in the 15–30 degree temperature range.

The majority of motorcycles are leased in the absence of snow or rain.
The majority of the bikes are hired in the 30 to 70% humidity range.
The 18th hour, or 6 p.m., saw the most bike rentals, while the 4th hour, or 4 a.m., saw the fewest.
The majority of bike rentals have occurred during periods of high visibility.
Outcomes of machine learning models:
With a r2 score of 0.6645, Random Forest Regression is the best-performing model.


With a r2 score of 0.4264, Lasso Regression (L1 regularization) is the least effective model.

All four models have their Actual vs. Prediction visualization completed.
The SHAP library has been used to explain each of the four models.
Based on all the models, the two most significant elements are the hour and the temperature.

Obstacles encountered: Eliminating Outliers.
the categorical columns' encoding.
Removing the dataset's multicollinearity.
Selecting the Model Explainability Technique
"""