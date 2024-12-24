
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
sns.set(style="whitegrid")

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


