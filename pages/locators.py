from selenium.webdriver.common.by import By

#Login page Locators class
class LoginPageLocators:
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    STATUS_DROPDOWN = (By.ID, 'status')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    MESSAGE_TEXT = (By.ID, 'message')
