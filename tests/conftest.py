import pytest
import os
from selenium import webdriver
from pages.login_page import LoginPage
from utils.locator_reporter import generate_html_report

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    file_path = f"file:///{os.path.abspath('login.html')}"
    page = LoginPage(driver)
    page.open(file_path)
    return page

@pytest.fixture(scope="session", autouse=True)
def final_report():
    yield
    generate_html_report()
