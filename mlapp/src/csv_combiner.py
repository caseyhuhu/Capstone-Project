import pandas as pd
import sys
import os
cwd = os.getcwd()
cwd = cwd+'/src/'


# Combines two CSV given as arguments in the command line
orig_df = pd.read_csv(cwd+'Combined_data_adjusted_full.csv')
new_df = pd.read_csv(cwd+'upload/'+sys.argv[1]) # New DataFrame with the users' companies' data. Stock prices are the last columns
if new_df.columns.tolist()[0] == 'Unnamed: 0':
    new_df = pd.read_csv(cwd+'upload/'+sys.argv[1], index_col=0)

if len(new_df.columns) % 12 != 0:
    print('ERROR: DataFrame must contain 12 features per company.')
elif len(new_df) != len(orig_df):
    print('ERROR: DataFrames must contain the same number of rows.')
else:
    num_companies = int(len(new_df.columns) / 12)
    combined_df = pd.concat([orig_df.iloc[:,:-9], new_df.iloc[:,:-num_companies], 
                             orig_df.iloc[:,-9:], new_df.iloc[:,-num_companies:]], axis=1)
    combined_df.to_csv(cwd+'Combined_data_user_input.csv', index=False)

