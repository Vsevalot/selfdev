import pytest
from simplemail.re_search import (get_bracket_content, sender_from_eml)
from tests.test_data import get_sender_test_data


@pytest.mark.parametrize("string, b1, b2, answer",
                         [("<user@yandex.ru>", '<', '>', "user@yandex.ru"),
                          ("<user@yandex.ru>", '[', ']', None),
                          ("[user@yandex.ru]", '<', '>', None),
                          ("[user@yandex.ru]", '[', ']', "user@yandex.ru"),
                          ("user@yandex.ru", '<', '>', None)])
def test_get_bracket_content(string, b1, b2, answer):
    res = get_bracket_content(string, b1, b2)
    assert res == answer


eml_bodies, answers, ids = get_sender_test_data()


@pytest.mark.parametrize("eml_body, answer",
                         [(b, a) for b, a in zip(eml_bodies, answers)],
                         ids=ids)
def test_get_bracket_content(eml_body, answer):
    res = sender_from_eml(eml_body)
    assert res == answer
