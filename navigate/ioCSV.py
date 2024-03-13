import pandas as pd
import csv

def ReadDomains(file_path):
    domains_df = pd.read_csv(file_path, header=None)
    domains_list = domains_df[0].tolist()
    # print(domains_list)
    return domains_list

# read_domains('domains.csv')

def ExtractData(data):
    
    # Open the CSV file in append mode
    with open('savedata.csv', 'a', newline='') as csvfile:
        # Create a writer object
        csvwriter = csv.writer(csvfile)
        
        # Append the row
        csvwriter.writerow(data)
