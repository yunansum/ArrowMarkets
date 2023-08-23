import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Function to generate random username and Ethereum address (you may use a different method if desired)
import random
import string

def generate_random_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def generate_random_ethereum_address():
    characters = "abcdef" + string.digits
    return '0x' + ''.join(random.choice(characters) for i in range(40))

# URL and referral code
url = "https://www.arrow.markets/waitlist?referralCode=mh2eXFPl"

# Set up Selenium web driver in headless mode
chrome_path = "/home/yunan/Automation/ArrowMarkets/pip/chromedriver"  # Replace with the path to your chromedriver executable
chrome_options = Options()
#chrome_options.add_argument("--headless")
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

max_attempts = 1000

while True:
    # Create a new driver instance for each attempt
    driver = webdriver.Chrome(service=service, options=chrome_options)
    attempts = 0
    signed_up = True

    while signed_up and attempts < max_attempts:
        try:
            # Open the URL in the browser
            driver.get(url)
            #driver.maximize_window()

            # Wait for the sign-up form to load
            wait = WebDriverWait(driver, 10)
            username_input = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
            wallet_address_input = wait.until(EC.presence_of_element_located((By.NAME, "Wallet Address")))
            sign_up_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/form/button")))

            # Generate random username and Ethereum address
            random_username = generate_random_username()
            random_ethereum_address = generate_random_ethereum_address()

            # Fill in the sign-up form
            username_input.send_keys(random_username)
            wallet_address_input.send_keys(random_ethereum_address)

            #time.sleep(1)
            # Click the sign-up button
            driver.implicitly_wait(10)
            sign_up_button.click()
            #driver.implicitly_wait(10)
            # Wait for the response and check for the "Network Error" pop-up
            try:
                signed_up_succesfully = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-typography elements__StyledHeading-sc-1h3erfw-0 gRrPFZ"))
                )
                if signed_up_succesfully.is_displayed():
                    # If there's a network error, refresh the page and try again
                    signed_up = False
                    attempts += 1
            except:
                # If no pop-up is found within the timeout, assume sign-up was successful and break the loop
                signed_up = True
                print("Sign-up successful!")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
        #driver.implicitly_wait(10)
        # Close the browser after each sign-up attempt
        driver.quit()

    # Wait for some time before starting the sign-up process again
    time.sleep(0)
