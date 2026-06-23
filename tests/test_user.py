from user import UserManager, User

def test_create_user():
    manager = UserManager()
    user = manager.create_user("test@example.com", "password")
    assert user.email == "test@example.com"
    assert user.password_hash == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

def test_create_user_with_google():
    manager = UserManager()
    user = manager.create_user_with_google("google_id", "test@example.com")
    assert user.email == "test@example.com"
    assert user.google_id == "google_id"

def test_validate_password():
    manager = UserManager()
    manager.create_user("test@example.com", "password")
    assert manager.validate_password("test@example.com", "password")
    assert not manager.validate_password("test@example.com", "wrong_password")

def test_rate_limit_signup():
    manager = UserManager()
    assert manager.rate_limit_signup("192.168.1.1")
    assert manager.rate_limit_signup("192.168.1.1")
    assert manager.rate_limit_signup("192.168.1.1")
    assert manager.rate_limit_signup("192.168.1.1")
    assert manager.rate_limit_signup("192.168.1.1")
    assert not manager.rate_limit_signup("192.168.1.1")

def test_set_session_cookie():
    manager = UserManager()
    manager.create_user("test@example.com", "password")
    cookie = manager.set_session_cookie("test@example.com")
    assert cookie["session"].value == "1"

def test_get_user_from_session():
    manager = UserManager()
    manager.create_user("test@example.com", "password")
    user = manager.get_user_from_session("1")
    assert user.email == "test@example.com"
