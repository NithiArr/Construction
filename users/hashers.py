from django.contrib.auth.hashers import BasePasswordHasher
from werkzeug.security import check_password_hash, generate_password_hash

class WerkzeugScryptPasswordHasher(BasePasswordHasher):
    """
    Password hasher that uses werkzeug.security.check_password_hash
    to verify passwords migrated from Flask.
    """
    algorithm = "scrypt:32768:8:1"

    def verify(self, password, encoded):
        """
        Check if the given password is correct.
        """
        try:
            print(f"Verifying password with WerkzeugScryptPasswordHasher")
            print(f"Encoded hash prefix: {encoded[:20]}...")
            # werkzeug's check_password_hash handles the format automatically
            # format example: scrypt:32768:8:1$salt$hash
            result = check_password_hash(encoded, password)
            print(f"check_password_hash result: {result}")
            return result
        except Exception as e:
            print(f"Hasher error: {e}")
            return False

    def safe_summary(self, encoded):
        return {
            'algorithm': self.algorithm,
            'hash': encoded,
        }

    def must_update(self, encoded):
        """
        Return True so that Django re-hashes the password
        to its default (PBKDF2) upon successful login.
        """
        return True

    def encode(self, password, salt):
        """
        This shouldn't be used for new passwords, but required by API.
        """
        # We don't want to generate new passwords with this hasher,
        # but if forced, use standard werkzeug scrypt
        return generate_password_hash(password, method='scrypt')

    def harden_runtime(self, password, encoded):
        pass
