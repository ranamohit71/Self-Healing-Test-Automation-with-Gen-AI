import os
import inspect

class LocatorUpdater:
    BY_MAP = {
        "id": "By.ID",
        "name": "By.NAME",
        "xpath": "By.XPATH",
        "css_selector": "By.CSS_SELECTOR",
        "class_name": "By.CLASS_NAME",
        "tag_name": "By.TAG_NAME",
        "link_text": "By.LINK_TEXT",
        "partial_link_text": "By.PARTIAL_LINK_TEXT"
    }

    @staticmethod
    def update_locator(locator_class, locator_name, new_by, new_value):
        if not hasattr(locator_class, locator_name):
            raise AttributeError(f"Locator '{locator_name}' not found in {locator_class.__name__}")

        old_locator = getattr(locator_class, locator_name)
        setattr(locator_class, locator_name, (new_by, new_value))  # in-memory update

        locator_file_path = inspect.getfile(locator_class)

        with open(locator_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Normalize new_by to lowercase for mapping
        by_key = new_by.lower() if isinstance(new_by, str) else new_by

        if isinstance(by_key, str) and by_key in LocatorUpdater.BY_MAP:
            by_str = LocatorUpdater.BY_MAP[by_key]
        else:
            # Fallback: write as string with quotes
            by_str = f"'{new_by}'"

        updated_lines = []
        found = False
        for line in lines:
            if line.strip().startswith(f"{locator_name} ="):
                found = True
                updated_lines.append(f"    {locator_name} = ({by_str}, {repr(new_value)})\n")
            else:
                updated_lines.append(line)

        if not found:
            raise ValueError(f"Locator '{locator_name}' not found in {locator_file_path}.")

        with open(locator_file_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

        log_path = os.path.join(os.path.dirname(locator_file_path), "locator_changes.log")
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"{locator_name} updated from {old_locator} to ({new_by}, {new_value})\n")

        print(f"✅ Locator '{locator_name}' updated and logged at {log_path}")
