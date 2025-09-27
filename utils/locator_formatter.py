from selenium.webdriver.common.by import By

STRING_TO_BY = {
    "id": "By.ID",
    "name": "By.NAME",
    "xpath": "By.XPATH",
    "css_selector": "By.CSS_SELECTOR",
    "class_name": "By.CLASS_NAME",
    "tag_name": "By.TAG_NAME",
    "link_text": "By.LINK_TEXT",
    "partial_link_text": "By.PARTIAL_LINK_TEXT",
}

def format_locator(locator_tuple):
    by_raw, value = locator_tuple
    if hasattr(by_raw, "upper"):  # string case
        by_str = STRING_TO_BY.get(by_raw.lower(), f"By.UNKNOWN('{by_raw}')")
    else:  # By.ID etc. constant case
        by_str = f"By.{by_raw.name}"
    return f"{by_str}, \"{value}\""
