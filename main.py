from navigate.navigateDomain import NavigateDomain
from navigate.ioCSV import ReadDomains

domain_list = ReadDomains('domains.csv')

for domain in domain_list:
    # print(domain)
    domain_url = 'https://' + domain + '/'
    print(domain_url)
    NavigateDomain(domain_url)
    # print(domain_url)