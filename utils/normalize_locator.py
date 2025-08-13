from selenium.webdriver.common.by import By

BY_MAP = {
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'css_selector': By.CSS_SELECTOR,
    'class_name': By.CLASS_NAME,
    'tag_name': By.TAG_NAME,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
}

def fix_locator(locator_tuple):
    by_str, value = locator_tuple
    by_enum = BY_MAP.get(by_str.lower())
    if not by_enum:
        raise ValueError(f"Unknown locator type: {by_str}")
    return (by_enum, value)
