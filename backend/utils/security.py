"""
Security utilities for the SAMS project.
"""
import secrets
import string
from datetime import datetime, timedelta
import hashlib

def generate_secure_token(length=32):
    """
    Generate a cryptographically secure random token.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_qr_token(session_id):
    """
    Generate a unique token for QR codes.
    """
    timestamp = datetime.now().isoformat()
    data = f"{session_id}-{timestamp}-{secrets.token_hex(8)}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]

def validate_token(token, max_age_seconds=3600):
    """
    Basic token validation (placeholder implementation).
    """
    return len(token) >= 16  # Simple length check for now
