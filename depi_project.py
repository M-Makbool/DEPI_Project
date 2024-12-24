# -*- coding: utf-8 -*-
"""DEPI_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15vYnafjX4dtawPTow6GQUtqtzqgNLSzA
"""

!pip install sqlalchemy
!pip install pandas
!pip install pyodbc
!pip install matplotlib
!pip install seaborn
!pip install kagglehub

from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

#Connect to the SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=CustomerReviews1;'
                      'Trusted_Connection=yes;')

#Query to get data frame from the CustomerReviews1 table
query = "SELECT * FROM CustomerReviews2"
df = pd.read_sql(query, conn)
conn.close()

# Download latest version of dataset from kaggle
path = kagglehub.dataset_download("chaudharyanshul/airline-reviews")
print("Path to dataset files:", path)

#Read the csv file and make a data frame
full_path = path + '/BA_AirlineReviews.csv'
#
!mv $full_path .

df = pd.read_csv('./BA_AirlineReviews.csv')
df

#Explore the Data
# Renaming the 'ID' column
column_index_to_rename = 0 # Index of the 'ID' column
new_column_name = 'ID'

# Renaming the column using the 'rename' method
df.rename(columns={df.columns[column_index_to_rename]: new_column_name}, inplace=True)

print(df)                  # Displaying the DataFrame after renaming
print(df.info())           # Get info on data types and non-null counts
print(df.describe())       # Get basic statistics for numeric columns

# Print the number of null values per column
print(df.isnull().sum())

# Visualize the null values as a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.show()

#Drop the specified columns
df.drop(columns =
    ['ID','ReviewHeader','ReviewBody','Aircraft','Wifi&Connectivity', 'InflightEntertainment' ], inplace=True)

# Visualize the null values as a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.show()

# Step 2:
# Identify object type columns
object_columns = df.select_dtypes(include='object').columns



for column in df.columns:
    # Fill the null values in numerical columns by the median of each SeatType category
    if df[column].dtypes == 'float64':
       df[column] = df.groupby('SeatType')[column].transform(lambda x: x.fillna(x.median()))
    #Drop rows with null values in object type columns
    elif df[column].dtype == 'object':
         df.dropna(subset=[column], inplace=True)


# Verify the result
print(df.info())  # Get info on data types and non-null counts
print(df.isnull().sum())  # Print the number of null values per column

# Visualize the null values as a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.show()

# Visualize the Distribution
CatogiralColumns=['VerifiedReview','TypeOfTraveller','SeatType']
# Loop through each column in the DataFrame
for column in df.columns:
    # Check if the column is numeric
    if df[column].dtype == 'float64':
        #Plot histogram
        sns.histplot(df[column], bins=30, kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()
    elif df[column].dtype == 'bool' or column in CatogiralColumns:
        #Plot count plot for categorical columns
        plt.figure(figsize=(10, 4))
        sns.countplot(y=df[column])
        plt.title(f'Distribution of {column}')
        plt.ylabel(column)
        plt.xlabel('Count')
        plt.show()

df.to_csv('./CustomerReviews2.csv', index=False)

#Database connection details
server = 'localhost'
database = 'CustomerReviews2'
driver = 'ODBC Driver 17 for SQL Server'

#Connection string to connect DB
connection_string = f"mssql+pyodbc://{server}/{database}?driver={driver}"
engine = create_engine(connection_string)

#Save the DataFrame to new DB and replace table if it exists
df.to_sql('CustomerReview2', engine, if_exists='replace', index=False)
print("DataFrame saved successfully to SQL Server!")

from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

#Connect to the SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=CustomerFeedbackDW;'
                      'Trusted_Connection=yes;')

#Read the csv file and make a data frame
data = pd.read_csv('./CustomerReview2.csv')
data

# Querying data from the data warehouse
query = """
SELECT
    c.Name AS CustomerName,
    c.VerifiedReview,
    st.SeatType,
    tt.TypeOfTraveller,
    fr.SeatComfort,
    t.Date
FROM
    Fact_Review fr
JOIN
    Dim_Customer c ON fr.CustomerID = c.CustomerID
JOIN
    Dim_SeatType st ON fr.SeatTypeID = st.SeatTypeID
JOIN
    Dim_TravellerType tt ON fr.TravellerTypeID = tt.TravellerTypeID
JOIN
    Dim_Time t ON fr.DateKey = t.DateKey
"""
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Displaying the first few rows of the dataframe
print(data.head())

# Set the style
sns.set_theme(style="whitegrid")

# Create a count plot for OverallRating
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='OverallRating', palette='viridis')
plt.title('Distribution of Overall Ratings')
plt.xlabel('Overall Rating')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='SeatComfort', y='OverallRating', palette='coolwarm')
plt.title('Seat Comfort vs. Overall Rating')
plt.xlabel('Seat Comfort Rating')
plt.ylabel('Overall Rating')
plt.show()



plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='TravellerTypeID', hue='Recommended', palette='pastel')
plt.title('Recommendations by Traveller Type')
plt.xlabel('Traveller Type ID')
plt.ylabel('Count')
plt.legend(title='Recommended', loc='upper right')
plt.show()



# Ensure Datetime is in datetime format
data['Datetime'] = pd.to_datetime(data['Datetime'])



# Create a box plot to show the distribution of OverallRating
plt.figure(figsize=(10, 6))
sns.boxplot(x='Recommended', y='OverallRating', data=data, palette='pastel')
plt.title('Overall Rating Distribution by Recommendation')
plt.xlabel('Recommended')
plt.ylabel('Overall Rating')
plt.xticks(ticks=[0, 1], labels=['Not Recommended (0)', 'Recommended (1)'])
plt.show()



# Calculate average OverallRating for each Recommendation category
average_rating = data.groupby('Recommended')['OverallRating'].mean().reset_index()

# Plotting the average OverallRating
plt.figure(figsize=(8, 5))
sns.barplot(x='Recommended', y='OverallRating', data=average_rating, palette='viridis')
plt.title('Average Overall Rating by Recommendation')
plt.xlabel('Recommended')
plt.ylabel('Average Overall Rating')
plt.xticks(ticks=[0, 1], labels=['Not Recommended (0)', 'Recommended (1)'])
plt.show()



# Summary statistics for OverallRating
print(data['OverallRating'].describe())

# Count of Recommended
recommended_counts = data['Recommended'].value_counts()
print(recommended_counts)



# Create a count plot for OverallRating colored by Recommended
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='OverallRating', hue='Recommended', palette='muted')
plt.title('Count of Recommendations by Overall Rating')
plt.xlabel('Overall Rating')
plt.ylabel('Count')
plt.legend(title='Recommended', loc='upper right', labels=['No (0)', 'Yes (1)'])
plt.show()

# Check if 'SeatType' and 'SeatComfort' exist
if 'SeatType' in data.columns and 'SeatComfort' in data.columns:
    # Create a box plot for SeatComfort by SeatType
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=data, x='SeatType', y='SeatComfort', palette='muted')
    plt.title('Seat Comfort Ratings by Seat Type')
    plt.xlabel('Seat Type')
    plt.ylabel('Seat Comfort Rating')
    plt.xticks(rotation=45)  # Rotate x labels for better readability
    plt.ylim(0, 10)  # Adjust based on the expected rating scale
    plt.show()

    # Calculate the average seat comfort for each SeatType
    average_comfort = data.groupby('SeatType')['SeatComfort'].mean().reset_index()

    # Plotting the average seat comfort
    plt.figure(figsize=(10, 5))
    sns.barplot(x='SeatType', y='SeatComfort', data=average_comfort, palette='viridis')
    plt.title('Average Seat Comfort Rating by Seat Type')
    plt.xlabel('Seat Type')
    plt.ylabel('Average Seat Comfort Rating')
    plt.xticks(rotation=45)  # Rotate x labels for better readability
    plt.ylim(0, 10)  # Adjust based on the expected rating scale
    plt.show()
else:
    print("One or both of the columns 'SeatType' and 'SeatComfort' are missing from the DataFrame.")

plt.savefig('plot_name.png', dpi=300)  # Save with high resolution