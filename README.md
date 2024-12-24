# Customer Feedback Analysis and Improvement

## Project Overview
This repository contains the code, workflows, and documentation for the **Customer Feedback Analysis and Improvement** project. The goal of this project is to analyze customer reviews of British airline customers using data science techniques to gain actionable insights and identify areas of improvement.

## Project Phases

### Phase 1: Creating the Database
- **Database Creation**: Set up a SQL Server database to store customer feedback data.
- **Table Definition**: Defined tables with appropriate columns and data types.
- **Data Import**: Imported the provided dataset (CSV format) into the database.

### Phase 2: Data Cleansing using Python
- **ETL Process**:
  - **Extraction**: Retrieved the dataset from the SQL Server database to Python.
  - **Transformation**: Cleansed the data by:
    - Handling missing values
    - Correcting data types
  - **Validation**: Applied techniques to remove duplicates, outliers, and incorrect formats.
- **Result**: Cleaned and transformed data was loaded back into a separate database for further processing.

### Phase 3: Staging Process
- **Data Preparation**: Stored the cleansed data in a staging area within the database to prepare it for data warehousing.

### Phase 4: Data Warehousing
- **Warehouse Creation**: Built a data warehouse in SQL Server for customer feedback analysis.
- **Schema Design**:
  - Defined a fact table for customer reviews.
  - Created associated dimension tables for better data organization.
- **Data Integration**: Extracted data from the staging database and loaded it into the data warehouse using SQL Server Integration Services (SSIS).

## Key Features
- **Database Management**: Scalable database structure for efficient storage and retrieval of customer feedback.
- **ETL Pipeline**: End-to-end pipeline for extracting, transforming, and loading data.
- **Data Warehouse**: Centralized repository for analytical insights.
- **Visualization**: Before and after snapshots of dataset transformations.

## Technology Stack
- **Database**: SQL Server
- **Data Processing**: Python (pandas, NumPy)
- **Data Warehousing**: SQL Server, SSIS
- **Version Control**: Git

## Repository Structure
```plaintext
├── data/                     # Dataset files
├── scripts/                  # Python scripts for ETL
├── sql/                      # SQL scripts for database and warehouse creation
├── notebooks/                # Jupyter notebooks for exploratory analysis
├── visuals/                  # Data visualizations and reports
├── README.md                 # Project overview
```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/M-Makbool/DEPI_Project.git
   ```

2. Set up the database:
   - Use the scripts in the `sql/` folder to create the database and tables.

3. Use the Python scripts for data processing

4. Load the cleaned data into the data warehouse

## Results
The project provides a comprehensive framework for analyzing customer feedback and identifying improvement areas, along with visual comparisons of raw and cleaned datasets.


