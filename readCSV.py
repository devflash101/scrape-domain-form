import pandas as pd

def read_domains(file_path):
    domains_df = pd.read_csv(file_path, header=None)
    domains_list = domains_df[0].tolist()
    # print(domains_list)
    return domains_list

# read_domains('domains.csv')