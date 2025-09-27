from utils.ollama_helper import get_best_locator_from_llm
from selenium.common.exceptions import NoSuchElementException
from pages.locators import LoginPageLocators
from utils.locator_updater import LocatorUpdater
from utils.normalize_locator import fix_locator
from utils.locator_reporter import log_locator_change
from utils.locator_formatter import format_locator

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    #method to find the new locators - will be called when Noelement found exception is raised.
    def safe_find(self, locator, locator_name):
        """Find element safely with error handling."""
        try:
            print("locator 1 = ", locator)
            locator = fix_locator(locator)
            print("locator 2 = ", locator)
            return self.driver.find_element(*locator)                    
        except NoSuchElementException:
            print(f"⚠️ Element not found: {locator} with locator name {locator_name} - {format_locator(locator)}")
            print(f'calling LLM to get the new locator for locator name {locator_name}')
            
            old_locator_by_type, old_locator_value = locator
            if locator_name:
                #get html page source
                html_source = self.driver.page_source
                
                new_locator_by_type, new_locator_value = get_best_locator_from_llm(html_source, locator_name)
                
                # Update locator in locator file
                LocatorUpdater.update_locator(
                    LoginPageLocators,
                    locator_name,
                    new_locator_by_type,
                    new_locator_value
                )    
                
                updated_locator = getattr(LoginPageLocators, locator_name)
                
                final_updated_locator = fix_locator(updated_locator)
                                
                #log the locator change for reporting
                log_locator_change(locator_name,locator, final_updated_locator)

                print(f"🔄 Retrying with updated locator for {locator_name} - {format_locator(final_updated_locator)}...")
                return self.driver.find_element(*final_updated_locator)
             
            return None
        except Exception as e:
            print("unknown exception = ", e)

    def open(self, file_path):
        self.driver.get(file_path)

    def enter_username(self, username):
        print("def enter username called")
        print(LoginPageLocators.USERNAME_INPUT)
        print(type(LoginPageLocators.USERNAME_INPUT))

        elem = self.safe_find(LoginPageLocators.USERNAME_INPUT, "USERNAME_INPUT")
        if elem:
            elem.send_keys(username)

    def enter_password(self, password):
        elem = self.safe_find(LoginPageLocators.PASSWORD_INPUT, "PASSWORD_INPUT")
        if elem:
            elem.send_keys(password)

    def select_status(self, status):
        elem = self.safe_find(LoginPageLocators.STATUS_DROPDOWN, "STATUS_DROPDOWN")
        if elem:
            elem.send_keys(status)

    def click_login(self):
        elem = self.safe_find(LoginPageLocators.LOGIN_BUTTON, "LOGIN_BUTTON")
        if elem:
            elem.click()

    def get_message(self):
        elem = self.safe_find(LoginPageLocators.MESSAGE_TEXT, "MESSAGE_TEXT")
        return elem.text if elem else "Message element not found"
