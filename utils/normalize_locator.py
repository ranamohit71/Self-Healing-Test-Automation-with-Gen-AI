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
    print("inside fix_locator")
    by_key, value = locator_tuple
    print("by_key = ", by_key)
    print("value = ", value)
    by_key_updated = BY_MAP.get(by_key.lower(), by_key)
    print("by_key_updated = ", by_key_updated)
    if not by_key_updated:
        raise ValueError(f"Unknown locator type: {by_key}")
    return (by_key_updated, value)
