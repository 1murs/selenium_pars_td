import csv
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
import pickle


class SelectParameters:

    def __init__(self, game: str, first_service: str, second_service, price_from: float, price_to: float,
                 steam_sales: int = 100):
        """
        Initializes an instance of the SelectParameters class.

        Parameters:
        - game (str): The game identifier.
        - first_service (str): The identifier for the first service.
        - second_service (str): The identifier for the second service.
        - price_from (float): The lower limit of the price range.
        - price_to (float): The upper limit of the price range.
        - Steam_sales (int): number of sales on Steam (default - 100).
        """

        self.game = game
        self.first_service = first_service
        self.second_service = second_service
        self.price_from = price_from
        self.price_to = price_to
        self.steam_sales = steam_sales
        self.url = 'https://tradeback.io/en'
        self.firefox_options = Options()  # Set up FireFox options for headless mode
        self.firefox_options.headless = True
        self.driver = webdriver.Firefox()

    def set_cookies(self):
        """
        Sets cookies for the WebDriver by loading them from a file.
        """
        with open('cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.get(self.url)
                self.driver.add_cookie(cookie)

    def browser_action(self):
        """
        Performs a series of actions on the website, including selecting game, services, and setting filters.
        """
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/a[5]/span').click()
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]'))).click()
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div.dropdown-select:nth-child(3) > div:nth-child(2)')))
            nav_menu_games = self.driver.find_elements(By.CSS_SELECTOR, 'div.show:nth-child(3) > div > ul > li')
            [item.click() for item in nav_menu_games[1:] if int(item.get_attribute('value')) == self.game]
            self.driver.implicitly_wait(0.50)
            # disabling autoupdate
            self.driver.find_element(By.CSS_SELECTOR, 'div.dropdown-select:nth-child(6) > div:nth-child(1)').click()
            WebDriverWait(self.driver, 1, ).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                    'div.show:nth-child(2) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > label:nth-child(2)'))).click()

            # Select first service
            self.driver.find_element(By.CSS_SELECTOR,
                                     'div.comparison-service:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)').click()
            self.driver.implicitly_wait(0.50)
            menu_first_service = self.driver.find_elements(By.CSS_SELECTOR,
                                                           'div.show:nth-child(3) > div:nth-child(1) > ul:nth-child(2) > li')
            [item.click() for item in menu_first_service if item.get_attribute('data-short-name') == self.first_service]

            # Select second service
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]').click()
            self.driver.implicitly_wait(0.50)
            menu_second_service = self.driver.find_elements(By.CSS_SELECTOR,
                                                            'div.show:nth-child(3) > div:nth-child(1) > ul:nth-child(2) > li')

            [item.click() for item in menu_second_service if
             item.get_attribute('data-short-name') == self.second_service]
            self.driver.implicitly_wait(0.50)

            # Select sales for Steam
            self.driver.find_element(By.CSS_SELECTOR, '#more-filters.comparison-filters-btn').click()
            self.driver.implicitly_wait(0.50)
            filter_menu = self.driver.find_element(By.CSS_SELECTOR,
                                                   'div.comparison-sales-block:nth-child(1) > input:nth-child(2)')
            filter_menu.clear()
            filter_menu.send_keys(self.steam_sales)
            self.driver.find_element(By.CSS_SELECTOR,
                                     '#filters-modal > div:nth-child(1) > div:nth-child(3) > a').click()

            # Choose the price for the first and second service
            self.driver.implicitly_wait(0.50)
            self.driver.find_element(By.CSS_SELECTOR,
                                     'th.center:nth-child(8) > div:nth-child(2) > [placeholder="From"]').send_keys(
                self.price_from)

            self.driver.implicitly_wait(0.50)

            self.driver.find_element(By.CSS_SELECTOR,
                                     'th.center:nth-child(10) > div:nth-child(2) > [placeholder="To"]').send_keys(
                self.price_to)
            self.driver.implicitly_wait(0.50)

            # Refresh

            time.sleep(1)
            self.driver.find_element(By.ID, 'table-refresh').click()
            print('Setting of parameters is completed.')
            print()
            print('I start parsing the page and saving it as CSV...')
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#table-body > tr')))
        except ElementClickInterceptedException as ex1_:  # Error handling when clicking on an element.
            print(f"Error when clicking: {ex1_}")
            self.driver.quit()
        except TimeoutException as ex2_:  # Handle timeout error.
            print(f"Timeout: {ex2_}")
            self.driver.quit()
        except NoSuchElementException as ex3_:  # Handling missing element error.
            print(f"Element not found: {ex3_}")
            self.driver.quit()

    @staticmethod
    def save_product(title_name: str):
        """
        Writes product information to a CSV file, in this case, only the product name.

        Parameters:
        - title_name (str): The name of the product.
        """
        with open('skins_base.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title_name])

    def page_parsing(self):
        """
        Parses the webpage to extract product information and writes it to a CSV file.
        """
        print('A list of items appeared.')
        data_id = []
        c = 0
        flag = True
        while flag:
            items = self.driver.find_elements(By.CSS_SELECTOR, '#table-body > tr')
            for item in items:
                if item.get_attribute('data-item-id') in data_id:
                    """
                    You can pull out the name, price, number of sales, etc., 
                    But for my task I only need the name of the product
                    """
                    self.save_product(item.find_element(By.CLASS_NAME, 'copy-name').text.strip())
                    flag = False

                else:
                    data_id += [item.get_attribute('data-item-id')]
                    flag = True
                    self.driver.execute_script("window.scrollBy(0, 500000);")

        print('Recording completed.')
        self.driver.quit()
