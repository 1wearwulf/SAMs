"""
Custom exceptions for the SAMS project.
"""


class InvalidQRCodeException(Exception):
    """Exception raised for invalid or expired QR codes."""
    pass


class LocationOutOfRangeException(Exception):
    """Exception raised when location is outside the geofence."""
    pass


class AttendanceAlreadyMarkedException(Exception):
    """Exception raised when attendance is already marked for a session."""
    pass


class SessionNotActiveException(Exception):
    """Exception raised when trying to mark attendance for an inactive session."""
    pass


class AntiCheatException(Exception):
    """Exception raised for anti-cheat violations."""
    pass


class DeviceValidationException(Exception):
    """Exception raised for device fingerprint validation failures."""
    pass


class PermissionDeniedException(Exception):
    """Exception raised for permission denied."""
    pass
