# locator_reporter.py
"""
1. This log_locator_change will be called from a different file when locator is found to be changed.
2. The generate html report will generate the list of locators changed - 
it will display both old locators and updated locators
"""

from utils.locator_formatter import format_locator

locator_changes = []

def log_locator_change(locator_name, old_locator, new_locator):
    locator_changes.append({
        "locator_name": locator_name,
        "old_locator": old_locator,
        "new_locator": new_locator,
    })

def generate_html_report(filepath="locator_changes_report.html"):
    html_content = """
    <html>
    <head><title>Locator Changes Report</title></head>
    <body>
        <h1>Locator Changes Report</h1>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Locator Name</th>
                <th>Old Locator</th>
                <th>New Locator</th>
            </tr>
    """

    for change in locator_changes:
        old_loc_str = format_locator(change['old_locator'])
        new_loc_str = format_locator(change['new_locator'])
        html_content += f"""
            <tr>
                <td>{change['locator_name']}</td>
                <td>{old_loc_str}</td>
                <td>{new_loc_str}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📝 Locator changes report generated at: {filepath}")
