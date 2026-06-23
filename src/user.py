import hashlib
import time
from dataclasses import dataclass
from http import cookies
from typing import Dict, List, Optional


@dataclass
class User:
    """Simple user record."""
    id: int
    email: str
    password_hash: str
    google_id: Optional[str] = None


class UserManager:
    """Manages users, password validation, session cookies and sign‑up rate limiting."""

    # Rate‑limit configuration
    _MAX_ATTEMPTS = 5          # max attempts per window
    _WINDOW_SECONDS = 60      # time window in seconds

    def __init__(self) -> None:
        # email -> User
        self.users: Dict[str, User] = {}
        # ip -> list[timestamp of attempts]
        self.rate_limit: Dict[str, List[float]] = {}

    # --------------------------------------------------------------------- #
    # User creation
    # --------------------------------------------------------------------- #
    def create_user(self, email: str, password: str) -> User:
        """Create a user with an email/password."""
        if email in self.users:
            raise ValueError("Email already in use")
        password_hash = self._hash_password(password)
        user = User(id=len(self.users) + 1, email=email, password_hash=password_hash)
        self.users[email] = user
        return user

    def create_user_with_google(self, google_id: str, email: str) -> User:
        """Create a user that signed up via Google OAuth."""
        if email in self.users:
            raise ValueError("Email already in use")
        user = User(id=len(self.users) + 1, email=email, password_hash="", google_id=google_id)
        self.users[email] = user
        return user

    # --------------------------------------------------------------------- #
    # Password handling
    # --------------------------------------------------------------------- #
    @staticmethod
    def _hash_password(password: str) -> str:
        """Return a SHA‑256 hash of the password."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, email: str, password: str) -> bool:
        """Validate a password for the given email."""
        user = self.users.get(email)
        if not user:
            return False
        return user.password_hash == self._hash_password(password)

    # --------------------------------------------------------------------- #
    # Rate limiting
    # --------------------------------------------------------------------- #
    def rate_limit_signup(self, ip: str) -> bool:
        """
        Allow up to ``_MAX_ATTEMPTS`` sign‑up attempts from ``ip`` within
        ``_WINDOW_SECONDS``. Returns ``True`` if the attempt is allowed,
        ``False`` otherwise.
        """
        now = time.time()
        attempts = self.rate_limit.setdefault(ip, [])

        # Discard timestamps older than the window
        attempts = [ts for ts in attempts if now - ts < self._WINDOW_SECONDS]
        self.rate_limit[ip] = attempts

        if len(attempts) < self._MAX_ATTEMPTS:
            attempts.append(now)
            self.rate_limit[ip] = attempts
            return True
        return False

    # --------------------------------------------------------------------- #
    # Session handling
    # --------------------------------------------------------------------- #
    def set_session_cookie(self, email: str) -> cookies.BaseCookie:
        """Create an HTTP‑only session cookie for the user identified by ``email``."""
        user = self.users.get(email)
        if not user:
            raise ValueError("User not found")
        cookie = cookies.BaseCookie()
        cookie["session"] = str(user.id)
        cookie["session"]["httponly"] = True
        # Expires in 30 days (seconds since epoch)
        cookie["session"]["expires"] = str(int(time.time()) + 30 * 24 * 60 * 60)
        return cookie

    def get_user_from_session(self, session_id: str) -> Optional[User]:
        """Return the user whose ``id`` matches ``session_id``."""
        for user in self.users.values():
            if str(user.id) == session_id:
                return user
        return None
