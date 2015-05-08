from nose.tools import *
from mailbox.Mailbox import resolve_real_recipient

def test_resolve_recipient():
    test_users =  {"TestUser": {
        "aliases": ["xxx"]
    }}



    assert_equals("TestUser", resolve_real_recipient("testuser", test_users))
    assert_equals("TestUser", resolve_real_recipient("xxx", test_users))
    assert_is_none(resolve_real_recipient("xyx", test_users))
