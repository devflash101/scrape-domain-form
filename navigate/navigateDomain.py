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
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

anchor_words = ['Demo', 'Call', 'Book', 'Schedule', 'Consultation', 'Consult', 'Appointment', 'Get Started', 'Start', 'Inquire', 'Learn', 'Discover', 'More Info', 'Find Out', 'Get a Quote', 'Talk',
                'Explore', 'Details', 'Request', 'Connect', 'Get in', 'Contact']

def navigate_domain(url):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.page_load_strategy = self.load_mode
    driver = webdriver.Chrome(options = chrome_options)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')   
        
    driver.get(url)
  
    # contact_link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Contact')]]")
    # contact_link.click()
    
    name_field = driver.find_element(By.NAME, 'firstname')
    if name_field:
        name_field.send_keys('John Doe')
        print('success')
    while True:
        pass
    driver.quit()


navigate_domain('https://chassi.com/contact/')
# navigate_domain('https://parkstreet.com/')

'''
firstname
lastname
company
phone
email
'''