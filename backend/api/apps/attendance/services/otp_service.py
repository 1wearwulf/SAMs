"""
OTP (One-Time Password) services for additional security.
"""
import pyotp
import hashlib
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from typing import Optional, Dict, Any


class OTPService:
    """
    Service for handling OTP operations.
    """

    @staticmethod
    def generate_secret_key(user_id: int, session_id: int) -> str:
        """
        Generate a secret key for TOTP based on user and session.

        Args:
            user_id: User ID
            session_id: Session ID

        Returns:
            Base32 encoded secret key
        """
        # Create a unique secret based on user and session
        secret_data = f"{user_id}_{session_id}_{timezone.now().date()}"
        secret_hash = hashlib.sha256(secret_data.encode()).digest()

        # Convert to base32 for TOTP
        import base64
        secret_b32 = base64.b32encode(secret_hash).decode()[:32]

        return secret_b32

    @staticmethod
    def generate_totp(secret: str, interval: int = 30) -> str:
        """
        Generate a TOTP code.

        Args:
            secret: Base32 encoded secret key
            interval: Time interval in seconds

        Returns:
            6-digit TOTP code
        """
        totp = pyotp.TOTP(secret, interval=interval)
        return totp.now()

    @staticmethod
    def verify_totp(secret: str, code: str, interval: int = 30, window: int = 1) -> bool:
        """
        Verify a TOTP code.

        Args:
            secret: Base32 encoded secret key
            code: TOTP code to verify
            interval: Time interval in seconds
            window: Verification window (number of intervals to check)

        Returns:
            True if code is valid, False otherwise
        """
        totp = pyotp.TOTP(secret, interval=interval)
        return totp.verify(code, valid_window=window)

    @staticmethod
    def generate_hotp(secret: str, counter: int) -> str:
        """
        Generate an HOTP code.

        Args:
            secret: Base32 encoded secret key
            counter: Counter value

        Returns:
            6-digit HOTP code
        """
        hotp = pyotp.HOTP(secret)
        return hotp.at(counter)

    @staticmethod
    def verify_hotp(secret: str, code: str, counter: int, window: int = 10) -> Optional[int]:
        """
        Verify an HOTP code with counter synchronization.

        Args:
            secret: Base32 encoded secret key
            code: HOTP code to verify
            counter: Current counter value
            window: Verification window

        Returns:
            New counter value if verification succeeds, None otherwise
        """
        hotp = pyotp.HOTP(secret)

        for i in range(window):
            if hotp.verify(code, counter + i):
                return counter + i + 1

        return None

    @staticmethod
    def cache_otp_secret(user_id: int, session_id: int, secret: str, timeout: int = 300) -> None:
        """
        Cache OTP secret for a limited time.

        Args:
            user_id: User ID
            session_id: Session ID
            secret: OTP secret
            timeout: Cache timeout in seconds
        """
        cache_key = f"otp_secret_{user_id}_{session_id}"
        cache.set(cache_key, secret, timeout=timeout)

    @staticmethod
    def get_cached_otp_secret(user_id: int, session_id: int) -> Optional[str]:
        """
        Get cached OTP secret.

        Args:
            user_id: User ID
            session_id: Session ID

        Returns:
            Cached secret or None
        """
        cache_key = f"otp_secret_{user_id}_{session_id}"
        return cache.get(cache_key)

    @staticmethod
    def generate_backup_codes(user_id: int, count: int = 10) -> list:
        """
        Generate backup codes for OTP.

        Args:
            user_id: User ID
            count: Number of backup codes to generate

        Returns:
            List of backup codes
        """
        codes = []
        for i in range(count):
            code_data = f"backup_{user_id}_{i}_{timezone.now().timestamp()}"
            code_hash = hashlib.sha256(code_data.encode()).hexdigest()[:10].upper()
            codes.append(code_hash)

        return codes

    @staticmethod
    def verify_backup_code(user_id: int, code: str) -> bool:
        """
        Verify a backup code.

        Args:
            user_id: User ID
            code: Backup code to verify

        Returns:
            True if code is valid, False otherwise
        """
        # In a real implementation, you'd store hashed backup codes
        # and check against them. For now, we'll use a simple check.
        cache_key = f"backup_codes_{user_id}"
        used_codes = cache.get(cache_key, [])

        if code in used_codes:
            return False

        # Mark code as used
        used_codes.append(code)
        cache.set(cache_key, used_codes, timeout=86400 * 365)  # 1 year

        return True

    @staticmethod
    def get_otp_uri(secret: str, account_name: str, issuer: str = "SAMS") -> str:
        """
        Generate OTP URI for QR code generation.

        Args:
            secret: Base32 encoded secret
            account_name: Account name
            issuer: Issuer name

        Returns:
            OTP URI string
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(account_name, issuer_name=issuer)

    @staticmethod
    def validate_otp_setup(user_id: int, secret: str, code: str) -> Dict[str, Any]:
        """
        Validate OTP setup by verifying a test code.

        Args:
            user_id: User ID
            secret: OTP secret
            code: Test code from user

        Returns:
            Dictionary with validation result
        """
        is_valid = OTPService.verify_totp(secret, code)

        return {
            'is_valid': is_valid,
            'message': 'OTP setup successful' if is_valid else 'Invalid OTP code'
        }
