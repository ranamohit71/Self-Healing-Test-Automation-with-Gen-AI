import pytest

test_data = [
    ("testuser", "pass123", "Active", "Login successful"),
    ("", "pass123", "Active", "Please fill all fields"),
    ("testuser", "", "Active", "Please fill all fields"),
    ("testuser", "pass123", "", "Please fill all fields"),
]

@pytest.mark.parametrize("username,password,status,expected", test_data)
def test_login_functionality(login_page, username, password, status, expected):
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.select_status(status)
    login_page.click_login()
    message = login_page.get_message()
    assert expected in message
