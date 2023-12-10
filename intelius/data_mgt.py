import os
from os import listdir
import pandas as pd
import datetime as d
import shutil


def find_csv():
    # list all csv files only
    filenames = listdir(os.getcwd())
    csv_files = [filename for filename in filenames
                 if filename.endswith('.csv')
                 if filename != "input.csv"
                 if filename != "bank.csv"
                 if not filename.startswith("clean_combined")]
    return csv_files


def to_csv(data_set, name: str):
    date_time = d.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    df = pd.DataFrame(data_set)
    df.to_csv(name, index=False)


def merge_csv():
    df_csv_append = pd.DataFrame()
    csv_list = find_csv()

    # append the CSV files
    if len(csv_list) != 0:
        for file in csv_list:
            if file != 'input.csv':
                df = pd.read_csv(file)
                df_csv_append = df_csv_append._append(df, ignore_index=True)
    else:
        print('No .csv file in this directory!')

    # to_csv(df_csv_append, "intelius_combined_extraction_14_05_23_17_15.csv")
    return df_csv_append, csv_list


def append(ds):
    csv_append = pd.read_csv("bank.csv")
    df = pd.DataFrame(ds)
    csv_append = csv_append._append(df, ignore_index=True)

    csv_append = csv_append.drop_duplicates(subset=["Email"])
    csv_append = csv_append.dropna().reset_index(drop=True)

    csv_append.to_csv("bank.csv", index=False)


def clean_up():
    data, csv_list = merge_csv()
    res = []
    temp_list = []
    suffix = ['yahoo.com', 'gmail.com', 'msn.com', 'icloud.com', 'live.com', 'hotmail.com', 'verizon.net',
              'outlook.com']

    data['Email'] = data['Email'].astype(str)
    data['Street_Address'] = data['Street_Address'].astype(str)

    data.dropna(inplace=True)

    for index, row in data.iterrows():
        if row['Email'] != '[]' and row['Street_Address'] != []:

            row['Email'] = row['Email'].replace("'", "")
            row['Email'] = row['Email'].replace("[", "")
            row['Email'] = row['Email'].replace("]", "")
            row['Email'] = row['Email'].split(',')
            print(type(row['Email']))

            for m in row['Email']:
                for s in suffix:
                    if m.endswith(s):
                        temp_list.append(m)

            row['Email'] = temp_list
            temp_list = []
            print(type(row['Email']))

            if row['Email'] and row['Email'] != [] and row['Street_Address'] != []:
                row['Email'] = row['Email'][0]
                print(type(row['Email']))

            # row['Street_Address'] = row['Street_Address'].replace("',", "")
            # row['Street_Address'] = row['Street_Address'].replace("[", "")
            # row['Street_Address'] = row['Street_Address'].replace("]", "")
            # row['Street_Address'] = row['Street_Address'].split(',')
            # row['Street_Address'] = row['Street_Address'][0]

        if len(row['Email']) > 0 and row['Email'] != '[]' and row[
            'Street_Address'] != '[]' and len(row['Job_Title']) > 0:
            res.append(
                {
                    'First Name': row['First_Name'],
                    'Last Name': row['Last_Name'],
                    'Email': row['Email'],
                    'Job Title': row['Job_Title'],
                    'Street Address': row['Street_Address'],
                    'Age': row['Age']

                }
            )

    df = pd.DataFrame(res)
    df = df.drop_duplicates(subset=["Email"])

    append(df)

    # for csv in csv_list:
    #     shutil.move(csv, f'results/{csv}')

    # date_time = d.datetime.now()
    # dt = date_time.strftime("%d_%m_%y_%H_%M")
    # name = f'clean_combined_extraction_{dt}.csv'

    # to_csv(df, name)

    # to_csv(df1, "clean_combined_extraction.csv")


clean_up()
