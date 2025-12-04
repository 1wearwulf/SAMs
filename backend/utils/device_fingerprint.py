"""
Device fingerprinting utilities for anti-cheat measures.
"""
import hashlib
import json
import platform


def generate_device_fingerprint(user_agent, ip_address, accept_language, screen_resolution=None):
    """
    Generate a device fingerprint from request headers and other data.
    """
    fingerprint_data = {
        'user_agent': user_agent,
        'ip_address': ip_address,
        'accept_language': accept_language,
        'screen_resolution': screen_resolution
    }
    
    # Create a hash of the fingerprint data
    fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
    fingerprint_hash = hashlib.sha256(fingerprint_str.encode()).hexdigest()
    
    return fingerprint_hash


def get_device_info(request):
    """
    Extract device information from request.
    Returns a dictionary with device details.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    
    # Parse some basic info from user agent
    device_info = {
        'user_agent': user_agent,
        'ip_address': ip_address,
        'accept_language': accept_language,
        'platform': platform.system(),
        'platform_release': platform.release(),
        'browser': extract_browser_info(user_agent),
        'os': extract_os_info(user_agent),
    }
    
    return device_info


def extract_browser_info(user_agent):
    """Extract browser information from user agent string."""
    user_agent_lower = user_agent.lower()
    
    if 'chrome' in user_agent_lower and 'chromium' not in user_agent_lower:
        return 'Chrome'
    elif 'firefox' in user_agent_lower:
        return 'Firefox'
    elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
        return 'Safari'
    elif 'edge' in user_agent_lower:
        return 'Edge'
    elif 'opera' in user_agent_lower:
        return 'Opera'
    elif 'msie' in user_agent_lower or 'trident' in user_agent_lower:
        return 'Internet Explorer'
    else:
        return 'Unknown'


def extract_os_info(user_agent):
    """Extract operating system information from user agent string."""
    user_agent_lower = user_agent.lower()
    
    if 'windows' in user_agent_lower:
        return 'Windows'
    elif 'mac' in user_agent_lower or 'darwin' in user_agent_lower:
        return 'macOS'
    elif 'linux' in user_agent_lower:
        return 'Linux'
    elif 'android' in user_agent_lower:
        return 'Android'
    elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower:
        return 'iOS'
    else:
        return 'Unknown'


def validate_device_consistency(current_fingerprint, stored_fingerprint, threshold=0.8):
    """
    Validate if the current device fingerprint is consistent with a stored one.
    For now, using simple exact match. Could be enhanced with fuzzy matching.
    """
    # Simple exact match for now
    return current_fingerprint == stored_fingerprint


def get_request_fingerprint(request):
    """
    Extract device fingerprint from request.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    
    return generate_device_fingerprint(user_agent, ip_address, accept_language)


def get_client_ip(request):
    """
    Get client IP address from request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_device_fingerprint(request, user):
    """
    Check if the current device fingerprint matches the user's stored fingerprint.
    Returns True if valid, False otherwise.
    """
    current_fingerprint = get_request_fingerprint(request)
    
    # Get stored fingerprint from user profile or session
    # This is a placeholder - you need to implement your own storage logic
    stored_fingerprint = getattr(user, 'device_fingerprint', None)
    
    if stored_fingerprint:
        return validate_device_consistency(current_fingerprint, stored_fingerprint)
    
    # If no stored fingerprint, this is first login - store it
    return True
