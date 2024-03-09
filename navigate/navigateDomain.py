# get the domain url from main.py

# navigate the domain using selenium
#   LeadGeneration()
#   navigate subpages within the domain
#       LeadGeneration()
#               

# dev LeadGeneration():
#   if form_exist():
#       fill_form(), extract_data()
#   else return False

# def form_exist():
#   ...
#   check phone number
#   check captcha
from selenium import webdriver

def navigate_domain(url):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.page_load_strategy = self.load_mode
    driver = webdriver.Chrome(options = chrome_options)
        
    driver.get(url)

    name_field = driver.find_element_by_name('firstname')
    if name_field:
        print('success')
    driver.quit()


navigate_domain('http://parkstreet.com/')