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

phone_fields = ['phone', 'your-phone']

def FillForm(driver):
    for field in form_fields:
        try:
            form_element = driver.find_element(By.NAME, field)
            if form_element:
                form_element.send_keys('John Doe')
        except:
            pass

def ExtractData():
    pass

def FindForm(driver): # check whether form exist in the frame.
    ret = 0
    is_phone = 0

    # check if form exist
    for field in form_fields:
        try:
            form_element = driver.find_element(By.NAME, field)
            if form_element:
                ret = 1
        except:
            pass

    # check phone field exist
    for field in phone_fields:
        try:
            phone_field = driver.find_element(By.NAME, field)
            if phone_field:
                # name_field.send_keys('John Doe')
                is_phone = 1
        except:
            # print('failed')
            pass

    if ret == 1 and is_phone == 0:
        print('no phone field.')
    ret &= is_phone

    # check if there's captcha break
    try:
        captcha_element = driver.find_element(By.CLASS_NAME, 'grecaptcha-logo')
        if(captcha_element):
            print('captcha detected')
            ret = 0
    except:
        pass

    return ret

def LeadGeneration(driver): # check whether form exist in the page.
    
    # chrome_options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options = chrome_options)
    # driver.get(url)
    form_exist = FindForm(driver)

    if form_exist:
        FillForm(driver)
        ExtractData()  
    else:
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        for index, frame in enumerate(frames):
            # Switch to each frame by index
            driver.switch_to.frame(index)

            # Perform operations within the frame
            # ...
            form_exist |= FindForm(driver)
            if form_exist:
                FillForm(driver)
                ExtractData()
                driver.switch_to.default_content()
                break

            # Switch back to the default content before moving to the next frame
            driver.switch_to.default_content()

    if form_exist:
        print('form filled')
    else:
        print('this page was skipped')
    return form_exist

def NavigateDomain(url):
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.page_load_strategy = self.load_mode
    driver = webdriver.Chrome(options = chrome_options)
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--allow-running-insecure-content')   

    driver.get(url)

    button_expression = f"//button[contains(text(), 'Accept')]"
    try:
        accept_link = driver.find_element(By.XPATH, button_expression)
        if accept_link:
            print('accept button clicked')
            accept_link.click()
    except:
        pass
    
    form_filled = LeadGeneration(driver)
    if not form_filled:
        for word in anchor_words:
            if(form_filled):
                break
            print(word)
            # within <span>
            xpath_expression = f"//a[.//span[contains(text(), '{word}')]]"
            try:
                anchor_link = driver.find_element(By.XPATH, xpath_expression)

                if anchor_link:
                    anchor_link.click()
                    form_filled = LeadGeneration(driver)
                    driver.back()
            except:
                pass

            # without <span>
            xpath_expression = f"//a[contains(text(), '{word}')]"
            try:
                anchor_link = driver.find_element(By.XPATH, xpath_expression)

                if anchor_link:
                    print('anchor: ' + word)
                    anchor_link.click()
                    form_filled = LeadGeneration(driver)
                    driver.back()
            except:
                pass

    time.sleep(5)
    # while True:
    #     pass
    driver.quit()



# NavigateDomain('https://adstage.io/')
# NavigateDomain('https://capeanalytics.com/')
# NavigateDomain('https://dotloop.com/')
# NavigateDomain('https://homelight.com/')
# NavigateDomain('https://indinero.com/')
# NavigateDomain('https://jyve.com/')
# NavigateDomain('https://parkstreet.com/')
# NavigateDomain('https://goguardian.com/')
# NavigateDomain('https://claylacy.com/')
# NavigateDomain('https://marketshareonline.com/')
NavigateDomain('https://intrepidib.com/')


'''

parkstreet.com                  // success
chassi.com/contact              // frame, no-phone
https://www.claylacy.com/contact-us/        // success
https://info.marketshareonline.com/contact  // capcha
https://intrepidib.com/contact-us/          // your-phone
https://www.alpertandalpert.com/contact-us.html // no phone
https://yscouts.com/contact/            // no phone
https://valorglobal.com/get-a-quote/        // captcha
https://myfw.com/contact/               // captcha

firstname
lastname
company
phone
email
'''