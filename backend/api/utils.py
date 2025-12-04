"""
Common utilities for the SAMS API.
"""
import random
import string
from datetime import datetime, timedelta
from django.utils.timezone import now


def generate_random_code(length=6):
    """Generate a random alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_date_range(days_back=30):
    """Get date range for filtering."""
    end_date = now()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date
