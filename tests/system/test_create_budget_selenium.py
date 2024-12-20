# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 11:58:26 2024

@author: apgra
"""
import unittest
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import time

class TestCreateBudget(unittest.TestCase):

    def setUp(self):
        self.db = pymongo.MongoClient("mongodb://localhost:27017/").budget_app_test
        options = webdriver.ChromeOptions()
        driver_path = ChromeDriverManager().install() 
        service = webdriver.chrome.service.Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)  # Adjust if using a different browser
        self.driver.get("http://127.0.0.1:5000/")
        self.unique_username = f"Anthony_{int(time.time())}"
        result = self.db.users.insert_one({'username': self.unique_username, 'password': 'Anthony'})
        assert result.acknowledged, "User insertion failed"
        print(f"User inserted successfully: {self.unique_username}")
        self.driver.set_window_size(1247, 732)

    def test_create_budget(self):
        driver = self.driver

        # Verify Log in
        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.find_element(By.ID, "username").send_keys(self.unique_username)
        driver.find_element(By.ID, "password").send_keys("Anthony")
        driver.find_element(By.CSS_SELECTOR, "button").click()

        # Wait for dashboard and create budget form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )

        # Enter the budget name and submit
        driver.find_element(By.ID, "name").send_keys("Testing_Budget")
        driver.find_element(By.CSS_SELECTOR, "button").click()

        # Verify the budget is added to the list
        budget_list_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[h4[text()='Testing_Budget']]")
            )
        )
        self.assertTrue(
            budget_list_item.is_displayed(),
            "Newly created budget 'Testing_Budget' not found in the list."
        )

    def tearDown(self):
        self.db.users.delete_one({'username': self.unique_username})
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
