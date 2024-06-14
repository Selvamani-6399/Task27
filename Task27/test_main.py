"""
TEST MAIN
"""
from Data import Data
from Locators import Locators

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# exceptions
from selenium.common.exceptions import *


class TestOrangeHRM():

    #Fixtures are defined using the @pytest.fixture decorator in Python.
    @pytest.fixture
    def boot(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(Data.WebData().url)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    @pytest.mark.html
    def test_successful_employee_login(self,boot):
        # Login to the Webpage using credentials
        try:
            # Username - 2
            # Password - 3
            # Test Results - 7
            locator = Locators.WebLocators() # here we created variables for code easy to understand
            sheet = Data.WebData()
            for row in range(2, Data.WebData().rowCount() + 1):
                username = sheet.readData(row, 2)
                password = sheet.readData(row, 3)
                # Here we write a current date , time & username in the excel. 
                sheet.writeData(row,4,datetime.now().strftime("%Y-%m-%d"))
                sheet.writeData(row, 5, datetime.now().strftime("%H:%M:%S"))
                sheet.writeData(row, 6,"Selva")
                self.wait.until(EC.presence_of_element_located((By.NAME, locator.usernameLocator))).send_keys(username)
                self.wait.until(EC.presence_of_element_located((By.NAME, locator.passwordLocator))).send_keys(password)

                self.wait.until(EC.presence_of_element_located((By.XPATH, locator.buttonLocator))).click()
           # Check whether we have loged in to the webpage successfully or not

                curenturl = self.driver.current_url
                if (curenturl == Data.WebData().dashboardURL):
                    
                    print("login successfully")
                    # if we successfully loged in means it will write test passed in  excel 
                    sheet.writeData(row,7,"Passed")

                    # This is locate the logout button and click on that button
                    self.wait.until(EC.presence_of_element_located((By.XPATH, locator.dropdownMenuLocator))).click()
                    self.wait.until(EC.presence_of_element_located((By.XPATH, locator.logoutLocator))).click()
                else:
                    print("Login failed")
                    sheet.writeData(row, 7, "Failed")


        except Exception as e:
            print(f"Exception occurred: {e}")

