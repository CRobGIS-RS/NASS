## NASS
This repo consists of Python and Spark code for extracting data from the USDA National Agricultural Statistics Service Quick Stats API. This was developed to support my class project for CSIS638 Implementation of Database Management Systems.

The objective of the agricultural component of the database developed for CSIS638 was to focus on data for the U.S.’s primary crops. After some research, it was determined that Corn, Soybeans, Barley, and Oats were the most important crops to the U.S. economy. The United States Department of Agriculture (USDA) National Agricultural Statistics Service’s (NASS) Quick Stats tool was used to acquire production data at the county level. 

Quicks Stats is an online database containing official published aggregate estimates related to U.S. agricultural production. Sources for this database include hundreds of sample surveys that are conducted annually as well as the Census of Agriculture which occurs every five years. 

The code in this repo gains direct access to the data by leveraging the Quick Stats API (https://quickstats.nass.usda.gov/api). To use this API, the user must agree to the NASS terms of service and requesting an API key. 

# nass_quick_stat.py
 This script Relies on the Python Requests library to implement a GET request to acquire data for the crops of interest. The API is very flexible and provides a wide range of information. The following parameters are submitted to the API through the script to make the data request:

Source: Survey or Census
State: Abbreviation of the state being requested
Year: The beginning year in the range being queried
Statistic: Metric of interest (ex. Yield)
Unit: Level of aggregation (County or State)
* The script is designed to be run from the CLI with the user submitting the parameters as command line arguments.

The script returns monthly data for every year from the beginning year to the present in JSON format. The resulting data is transferred to a Pandas dataframe and aggregated by the county and year using a Group By function. The final aggregated dataframe is exported as a CSV file. 

# run_nass_for_all_states.py
Since nass_quick_stat.py only requests data for one crop and one state at a time, the code was integrated with this script to loop through a list of states and crops. 

# load_csv_tables_mysql_ag.py
Ingestion of the agriculture data required a few more preprocessing steps to organize the data in a manner that was consistent. The process is straightforward utilizing the Pandas and MySQL Connector for Python packages. MySQL Connector made it possible to insert a connection to the MySQL database into the scripts as well as submit SQL commands using a Cursor. 
All of the CSV files per crop type get read into a dataframe and appended together. Tables for each crop type are created and their schema is defined via the CREATE TABLE command. 