import pandas as pd
import os
import argparse
import sys
import requests


def main():
    api_key = "B6F71533-E3A1-3B55-BF31-5C331D862286"

    parser = argparse.ArgumentParser(description='Program for extarcting data from USDA Quick Stats.')
    parser.add_argument("-so", "--source", help= "SURVEY or CENSUS", type=str)
    parser.add_argument("-st", "--state", help= "Abreviation of state being queried", type=str)
    parser.add_argument("-yr", "--year", help= "Beginning year of timeframe being queried", type=str)
    parser.add_argument("-cr", "--crop", help= "Type of crop being queried ", type=str)
    parser.add_argument("-stc", "--statistic", help= "Metric being queried ", type=str)
    parser.add_argument("-u", "--unit", help= "Level of aggregation (STATE or COUNTY)", type=str)

    args = parser.parse_args()

    source_desc = args.source
    state = args.state
    year = args.year
    commodity_desc = args.crop
    statisticcat_desc = args.statistic
    agg_level_desc = args.unit

    url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={api_key}&source_desc={source_desc}&commodity_desc={commodity_desc}&agg_level_desc={agg_level_desc}&statisticcat_desc={statisticcat_desc}&year__GE={year}&state_alpha={state}"
     
    r = requests.get(url, headers={'Accept': 'application/json'})
    data = r.json()
    nass_df = pd.DataFrame(data['data'])

    nass_df["Value"] = nass_df["Value"].astype(str).astype(float)

    sum_test = nass_df.groupby(['county_name', 'year']).agg({'Value': ['sum','mean', 'min', 'max']})
    sum_test.columns = ['yield_sum', 'yield_mean', 'yield_min', 'yield_max']
    sum_test = sum_test.reset_index()
    print(sum_test)

    os.makedirs('C:/Projects/CSIS638/Project/data', exist_ok=True)  
    return sum_test.to_csv('C:/Projects/CSIS638/Project/data/test_survey_county_code.csv')  
        
if __name__ == "__main__":
    main()