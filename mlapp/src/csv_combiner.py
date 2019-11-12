import pandas as pd
import sys

# Combines two CSV given as arguments in the command line
orig_df = pd.read_csv(sys.argv[1]) # DataFrame with our original 9 companies' data. Stock prices are the last 9 columns
new_df = pd.read_csv(sys.argv[2]) # New DataFrame with the users' companies' data. Stock prices are the last columns

if len(new_df.columns) % 12 != 0:
    print('ERROR: DataFrame must contain 12 features per company.')
elif len(new_df) != len(orig_df):
    print('ERROR: DataFrames must contain the same number of rows.')
else:
    num_companies = len(new_df.columns) / 12
    combined_df = pd.concat([orig_df.iloc[:,:-9], new_df.iloc[:,:-num_companies], 
                             orig_df.iloc[:,-9:], new_df.iloc[:,-num_companies:]], axis=1)
    combined_df.to_csv('Combined_data_user_input.csv')