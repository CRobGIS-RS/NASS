"""
This script provides a subset of the command line arguments for selecting agricultural
information from USDA NASS QuickStat DB.
"""
import os
import argparse
import pandas as pd
import requests


def main():
    """ Sends request to the Quick Stats API and aggregates data by county and year

    Parameters
    ----------
    None

    Returns
    ---------
    csv file
        data summarized by county and year
        includes sum, mean, min, and max
    """
    api_key = "B6F71533-E3A1-3B55-BF31-5C331D862286"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-so", "--source", help= "SURVEY or CENSUS", type=str)
    parser.add_argument("-st", "--state", help= "Abreviation of state being queried", type=str)
    parser.add_argument("-yr", "--year", help= "Start year of range being queried", type=str)
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

    url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={api_key}\
        &source_desc={source_desc}\
        &commodity_desc={commodity_desc}\
        &agg_level_desc={agg_level_desc}\
        &statisticcat_desc={statisticcat_desc}\
        &year__GE={year}\
        &state_alpha={state}"
    api_call = requests.get(url, headers={'Accept': 'application/json'})
    data = api_call.json()
    nass_df = pd.DataFrame(data['data'])

    nass_df["Value"] = nass_df["Value"].astype(str).astype(float)

    sum_test = nass_df.groupby(['county_name', 'year']).agg({'Value': ['sum','mean', 'min', 'max']})
    sum_test.columns = ['value_sum', 'value_mean', 'value_min', 'value_max']
    sum_test = sum_test.reset_index()
    print(sum_test)

    output_path = '~/robinsonc6/data/agriculture'
    out_file = f'{state}_county_code_{commodity_desc}.csv'
    return sum_test.to_csv(os.path.join(output_path, out_file ))
if __name__ == "__main__":
    main()
    