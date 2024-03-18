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
from re import sub
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib.parse import urlparse
from datetime import datetime
from .ioCSV import ExtractData

anchor_words = ['Demo', 'Call', 'Book', 'Schedule', 'Consultation', 'Consult', 'Appointment', 'Get Started', 'Start', 'Inquire', 'Learn', 'Discover', 'More Info', 'Find Out', 'Get a Quote', 'Talk',
                'Explore', 'Details', 'Request', 'Connect', 'Get in', 'Contact']

# anchor_words = ['Contact']

form_fields = ['firstname', 'First Name', 'Last Name', 'lastname', 'name', 'email', 'company', 'company_website', 'phone', 'contact_reason', 'message']

phone_fields = ['phone', 'your-phone']

def FillForm(driver, anchor_text):
    data = []

    # keep domain url.
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    data.append('domain: ' + parsed_url.netloc)
    # keep date filled out form
    today = datetime.today()
    data.append('date: ' + today.strftime("%Y-%m-%d"))  # This formats the date as YYYY-MM-DD
    # keep time filled out form
    now = datetime.now()
    data.append('time: '+ now.strftime("%H:%M:%S"))

    data.append('anchor text: ' + anchor_text)
    
    for field in form_fields:
        try:
            form_element = driver.find_element(By.NAME, field)
            if form_element:
                form_element.send_keys('John Doe')
        except:
            pass
        
    xpath_expression = f"//input[@type='submit']"
    submit_button = driver.find_element(By.XPATH, xpath_expression)
    try:
        if submit_button:
            submit_button.click()
    except:
        pass

    return data

def FindForm(driver): # check whether form exist in the frame.
    ret = 0
    is_phone = 0

    # check if form exist
    for field in form_fields:
        xpath_expression = f"//input[@name='{field}']"
        xpath_expression1 = f"//input[contains(@placeholder, '{field}')]"
        try:
            form_element = driver.find_element(By.XPATH, xpath_expression)
            if form_element:
                ret = 1
        except:
            pass
        try:
            form_element1 = driver.find_element(By.XPATH, xpath_expression1)
            if form_element1:
                ret = 1
                print('  - found with placeholder')
        except:
            pass

    # check phone field exist
    for field in phone_fields:
        xpath_expression = f"//input[@name='{field}']"
        try:
            phone_field = driver.find_element(By.XPATH, xpath_expression)
            if phone_field and phone_field.is_displayed():
                # name_field.send_keys('John Doe')
                is_phone = 1
        except:
            # print('failed')
            pass
    
    if ret == 1:
        print('   - field found')
    if ret == 1 and is_phone == 0:
        print('   - no phone field.')
    ret &= is_phone

    # check if there's captcha break
    try:
        captcha_element = driver.find_element(By.CLASS_NAME, 'grecaptcha-badge')
        if captcha_element and captcha_element.get_attribute('data-style') == 'inline':
            print('   - captcha detected')
            ret = 0
    except:
        pass

    print('return the value when FindForm', ret)

    return ret

def LeadGeneration(driver, anchor_text): # check whether form exist in the page.
    
    # chrome_options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options = chrome_options)
    # driver.get(url)
    print('LeadGeneration', anchor_text)

    form_exist = FindForm(driver)

    try:
        if form_exist:
            data = FillForm(driver, anchor_text)
            ExtractData(data)
        else:
            print('form does not exist in the page', anchor_text, 'so looking into frames.')
            frames = driver.find_elements(By.TAG_NAME, 'iframe')
            # print('checking.......')
            for index, frame in enumerate(frames):
                # Switch to each frame by index
                print(' - looking for an iframe..')
                if not frame.is_displayed():
                    print("form skipped due to it's not displayed.")
                    continue
            
                actions = ActionChains(driver)
                actions.move_to_element(frame).perform()

                src_value = frame.get_attribute('src')
                if "video" in src_value:
                    print(' - src value continas "video"')
                    continue

                driver.switch_to.frame(index)

                # Perform operations within the frame
                # ...
                form_exist |= FindForm(driver)
                if form_exist:
                    data = FillForm(driver, anchor_text)
                    ExtractData(data)
                    driver.switch_to.default_content()
                    break

                # Switch back to the default content before moving to the next frame
                driver.switch_to.default_content()

        if form_exist:
            print(' - form filled')
        else:
            print(' - this page was skipped')
    except Exception as e:
        print(e)
        # pass
    return form_exist

def NavigateDomain(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    #chrome_options.page_load_strategy = self.load_mode
    driver = webdriver.Chrome(options = chrome_options)
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--allow-running-insecure-content')   

    try:
        driver.get(url)

        # close recommandation system
        try:
            # This XPath finds any button element whose class attribute contains the word 'close'
            close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")
            if close_button:
                print('#close button found')
                close_button.click()
                print("#Close button clicked.")
        except Exception as e:
            print("#Close button not clicked.")



        # Accept cookies button
        button_expression = f"//button[contains(text(), 'Accept')]"
        try:
            accept_link = driver.find_element(By.XPATH, button_expression)
            if accept_link:
                print('@accept button clicked')
                accept_link.click()
        except:
            pass

        # Accept cookies <a>
        button_expression = f"//a[contains(text(), 'Accept')]"
        try:
            accept_link = driver.find_element(By.XPATH, button_expression)
            if accept_link:
                print('@accept anchor clicked')
                accept_link.click()
        except:
            pass

        # close popup dlg.
        # Find the button by class name containing 'close' and click it
        # This XPath finds any button element whose class attribute contains the word 'close'
        close_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'close popup')]")
        if close_buttons:
            print('&close button found')
            for close_button in close_buttons:
                # close_buttons[1].click()
                try:
                    close_button.click()
                except Exception as e:
                    # print("Close button not clicked.")
                    pass

        
        form_filled = LeadGeneration(driver, 'hompage')
        if not form_filled:
            for word in anchor_words:
                if form_filled:
                    break
                print(word)
                # within <span>
                xpath_expression = f"//a[.//span[contains(text(), '{word}')]]"
                try:
                    anchor_link = driver.find_element(By.XPATH, xpath_expression)

                    if anchor_link:
                        anchor_link.click()
                        form_filled = LeadGeneration(driver, word)
                        driver.back()
                except:
                    pass

                # without <span>
                xpath_expression = f"//a[contains(text(), '{word}')]"
                try:
                    anchor_links = driver.find_elements(By.XPATH, xpath_expression)

                    for anchor_link in anchor_links:
                        if not anchor_link.is_displayed():
                            continue
                        print('**anchor: ' + word)
                        anchor_link.click()
                        print('**anchor ', word, ' clicked')
                        form_filled = LeadGeneration(driver, word)
                        driver.back()
                except Exception as e:
                    print(e)
                    # pass
            if not form_filled:
                data = []
                data.append('domain: ' + url + ' skipped')
                ExtractData(data)

        time.sleep(5)
        # while True:
        #     pass
    except Exception as e:
        # print(e)
        pass
    driver.quit()



# NavigateDomain('https://adstage.io/')
# NavigateDomain('https://capeanalytics.com/contact/')
# NavigateDomain('https://dotloop.com/')
# NavigateDomain('https://homelight.com/')
# NavigateDomain('https://indinero.com/')
# NavigateDomain('https://jyve.com/')
# NavigateDomain('https://parkstreet.com/')
# NavigateDomain('https://www.goguardian.com/')
# NavigateDomain('https://claylacy.com/')
# NavigateDomain('https://marketshareonline.com/')
# NavigateDomain('https://intrepidib.com/')
# NavigateDomain('https://alpertandalpert.com/')
# NavigateDomain('https://yscouts.com/')
# NavigateDomain('https://laneterralever.com/')
# NavigateDomain('https://valorglobal.com/')


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
https://laneterralever.com/             // cookie, popup close, no phone

firstname
lastname
company
phone
email
'''