import pytest
from simplemail.validation import is_email


@pytest.mark.parametrize("email, answer",
                         [("user@yandex.ru", True),
                          ("user1233@gmail.ofc", True),
                          ("user-super.winner123@yahooooooo.com", True),
                          ("asdasdsadds@asdasda", False),
                          ("!not_valid?@gmail.ru", False),
                          (None, False),
                          (1, False),
                          (True, False)])
def test_is_email(email, answer):
    res = is_email(email)
    assert res == answer
