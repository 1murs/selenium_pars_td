from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
import pickle


class AccountConnection:

    def __init__(self, login, password):
        """Constructor for the `AccountConnection` class.
        Accepts `login` and `password` parameters, providing login information."""
        self.login = login
        self.password = password
        self.url = 'https://tradeback.io/en'


    def save_cookies(self, dr: object):
        """Saves browser cookies to a file. Takes a browser object (`dr`) as a parameter."""
        try:
            with open("cookies.pkl", "ab") as f:
                pickle.dump(dr.get_cookies(), f)
        except (IOError, PermissionError) as ex_:
            print(f'Problem with saving cookies {ex_}')
        finally:
            dr.quit()
            print('Cookie mining is complete.')

    def registration(self):
        """Carry out the registration process on the tradeback.io website using the provided login and password."""
        firefox_options = Options()  # Set up FireFox options for headless mode
        firefox_options.headless = True

        with webdriver.Firefox(options=firefox_options) as driver:
            try:
                driver.get(self.url)
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'login'))).click()
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.iziModal-content img'))).click()
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      '.newlogindialog_TextField_2KXGK input'))).send_keys(self.login)
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      '.newlogindialog_TextField_2KXGK input[type="password"]'))).send_keys(
                    self.password)
                driver.find_element(By.CSS_SELECTOR,
                                    '.newlogindialog_CheckboxField_2QWD5 .newlogindialog_Checkbox_3tTFg').click()
                driver.implicitly_wait(0.5)
                driver.find_element(By.CSS_SELECTOR, '.newlogindialog_SignInButtonContainer_14fsn button').click()

                print('Confirm your login via phone!')
                if int(input('If you confirmed press 1 for me to make cookies: ')):
                    driver.find_element(By.ID, 'imageLogin').click()
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/a[5]/span'))).click()
                self.save_cookies(driver)

            except ElementClickInterceptedException as ex1_:  # Error handling when clicking on an element.
                print(f"Error when clicking: {ex1_}")
            except TimeoutException as ex2_:  # Handle timeout error.
                print(f"Timeout: {ex2_}")
            except NoSuchElementException as ex3_:  # Handling missing element error.
                print(f"Element not found: {ex3_}")
