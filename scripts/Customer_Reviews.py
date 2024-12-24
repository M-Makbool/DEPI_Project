
from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns


#Connect to the SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=CustomerReviews1;'
                      'Trusted_Connection=yes;')

#Query to get data frame from the CustomerReviews1 table
query = "SELECT * FROM CustomerReviews2"
df = pd.read_sql(query, conn)
conn.close()

#Read the csv file and make a data frame
#df = pd.read_csv('E:\BA_AirlineReviews.csv')


# Check for invalid date formats
invalid_dates = df[~df['Datetime'].str.match(r'^\d{4}-\d{2}-\d{2}$') | df['Datetime'].isnull()]

# Display the invalid dates
print("Invalid Dates:")
print(invalid_dates.sum())


#Explore the Data
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
    ['Id','ReviewHeader','ReviewBody','Aircraft','Wifi_Connectivity', 'InflightEntertainment' ], inplace=True)

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


#Database connection details
server = 'localhost'
database = 'CustomerReviews2'
driver = 'ODBC Driver 17 for SQL Server'

#Connection string to connect DB
connection_string = f"mssql+pyodbc://{server}/{database}?driver={driver}"
engine = create_engine(connection_string)

#Save the DataFrame to new DB and replace table if it exists
df.to_sql('CustomerService2', engine, if_exists='replace', index=False)
print("DataFrame saved successfully to SQL Server!")

