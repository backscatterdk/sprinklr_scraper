"""
Merge the excel files to one big csv, then save.
Excepts this script to be above a folder called 'data',
and for the excels to be in that folder:

└── sprinklr_scraper
    ├── data
    │   ├── excel_file_1.xlsx
    │   ├── excel_file_2.xlsx
    │   └── excel_file_3.xlsx
    └── merge_excel_files.py

"""

import os
import pandas as pd


data_dir = os.path.join(os.getcwd(), 'data')  # excel files are here
full_data_path = os.path.join(data_dir, 'full_data.csv')

files = [os.path.join(data_dir, file)
         for file in os.listdir(data_dir)]  # list of files

data = pd.DataFrame()  # we will store the big dataframe here

# open up each excel sheet and append to the big dataframe
for file in files:
    imp = pd.read_excel(file)
    data = data.append(imp)

data.to_csv(full_data_path)  # save backup
