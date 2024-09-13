import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class FrontendTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize WebDriver (Chrome in this case)
        cls.driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Close browser after tests

    def test_register_page(self):
        self.driver.get('http://localhost:5000/register')  # Replace with your Flask app URL

        # Simulate typing user registration details
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')

        username_field.send_keys('new_user')
        password_field.send_keys('new_password')


        # Check if the page redirects after successful registration
        self.assertIn('Register', self.driver.title)

    def test_login_page(self):
        self.driver.get('http://localhost:5000/login')  # Replace with your Flask app URL

        # Simulate typing username and password
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')

        username_field.send_keys('test_user')
        password_field.send_keys('correct_password')
        password_field.send_keys(Keys.RETURN)

        # Check if the page redirects after successful login
        self.assertIn('Login', self.driver.title)


if __name__ == '__main__':
    unittest.main()
