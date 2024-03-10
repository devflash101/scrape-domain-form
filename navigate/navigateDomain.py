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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

anchor_words = ['Demo', 'Call', 'Book', 'Schedule', 'Consultation', 'Consult', 'Appointment', 'Get Started', 'Start', 'Inquire', 'Learn', 'Discover', 'More Info', 'Find Out', 'Get a Quote', 'Talk',
                'Explore', 'Details', 'Request', 'Connect', 'Get in', 'Contact']

form_fields = ['firstname', 'lastname', 'name', 'email', 'company', 'company_website', 'phone', 'contact_reason', 'message']

def FindForm(driver): # check whether form exist in the frame.
    ret = 0

    # check form exist
    for field in form_fields:
        try:
            name_field = driver.find_element(By.NAME, field)
            if name_field:
                name_field.send_keys('John Doe')
                time.sleep(5)
                # print('success')
                ret = 1
        except:
            # print('failed')
            pass


    # check if phone number field exist
    try:
        name_field = driver.find_element(By.NAME, 'phone')
        if name_field:
            name_field.send_keys('John Doe')
            time.sleep(5)
            # print('success')
            ret = 1
    except:
        ret = 0
    return ret

def FormExist(url): # check whether form exist in the page.
    
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    form_exist = FindForm(driver)

    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    for index, frame in enumerate(frames):
        # Switch to each frame by index
        driver.switch_to.frame(index)

        # Perform operations within the frame
        # ...
        form_exist |= FindForm(driver)

        # Switch back to the default content before moving to the next frame
        driver.switch_to.default_content()

    if form_exist:
        print('exist')
    else:
        print('do not exist')
    time.sleep(5)
    driver.quit()

def LeadGeneration():
    pass

def navigate_domain(url):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.page_load_strategy = self.load_mode
    driver = webdriver.Chrome(options = chrome_options)
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--allow-running-insecure-content')   
        
    driver.get(url)
  
    contact_link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Contact')]]")
    contact_link.click()
    driver.switch_to.frame('hs-form-iframe-0')
    # try:
    #     WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.NAME, 'firstname'))
    #     )
    #     name_field = driver.find_element(By.NAME, 'firstname')
    #     name_field.send_keys('John Doe')
    #     print('Field found and filled.')
    # except Exception as e:
    #     print('Field not found:', e)


    name_field = driver.find_element(By.NAME, 'firstname')
    if name_field:
        name_field.send_keys('John Doe')
        time.sleep(5)
        print('success')
    # while True:
    #     pass
    driver.quit()



# navigate_domain('https://chassi.com/')
# navigate_domain('https://parkstreet.com/')
FormExist('https://chassi.com/contact/')

'''

parkstreet.com                  // success
chassi.com/contact              // frame, no-phone
https://www.claylacy.com/contact-us/        // success
https://info.marketshareonline.com/contact  // capcha

firstname
lastname
company
phone
email
'''