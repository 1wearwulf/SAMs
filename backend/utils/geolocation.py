"""
Geolocation utilities for location-based features.
"""

import math
from typing import Tuple, Optional
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.conf import settings
from core.constants import DEFAULT_GEOFENCE_RADIUS_METERS


def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the distance between two coordinates in meters.

    Args:
        coord1: Tuple of (latitude, longitude) for first point
        coord2: Tuple of (latitude, longitude) for second point

    Returns:
        Distance in meters
    """
    return geodesic(coord1, coord2).meters


def is_within_geofence(
    user_coords: Tuple[float, float],
    center_coords: Tuple[float, float],
    radius_meters: int = DEFAULT_GEOFENCE_RADIUS_METERS
) -> bool:
    """
    Check if user coordinates are within the geofence radius.

    Args:
        user_coords: User's (latitude, longitude)
        center_coords: Center point (latitude, longitude)
        radius_meters: Radius in meters

    Returns:
        True if within geofence, False otherwise
    """
    distance = calculate_distance(user_coords, center_coords)
    return distance <= radius_meters


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate that coordinates are within valid ranges.

    Args:
        latitude: Latitude value
        longitude: Longitude value

    Returns:
        True if valid coordinates, False otherwise
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def get_address_from_coordinates(latitude: float, longitude: float) -> Optional[str]:
    """
    Get human-readable address from coordinates using geocoding.

    Args:
        latitude: Latitude
        longitude: Longitude

    Returns:
        Address string or None if geocoding fails
    """
    try:
        geolocator = Nominatim(user_agent="sams-attendance-system")
        location = geolocator.reverse(
            (latitude, longitude),
            timeout=GEOCODING_TIMEOUT_SECONDS
        )
        return location.address if location else None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None


def get_coordinates_from_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates from a human-readable address.

    Args:
        address: Address string

    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    try:
        geolocator = Nominatim(user_agent="sams-attendance-system")
        location = geolocator.geocode(address, timeout=GEOCODING_TIMEOUT_SECONDS)
        if location:
            return (location.latitude, location.longitude)
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None


def calculate_bearing(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the bearing (direction) from coord1 to coord2.

    Args:
        coord1: Starting coordinates (latitude, longitude)
        coord2: Ending coordinates (latitude, longitude)

    Returns:
        Bearing in degrees (0-360)
    """
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing


def get_location_accuracy_tolerance(distance_meters: float) -> float:
    """
    Get acceptable location accuracy tolerance based on distance.

    Args:
        distance_meters: Distance in meters

    Returns:
        Tolerance in meters
    """
    # For distances under 100m, allow 10m tolerance
    # For distances 100-1000m, allow 50m tolerance
    # For distances over 1000m, allow 100m tolerance
    if distance_meters < 100:
        return 10
    elif distance_meters < 1000:
        return 50
    else:
        return 100


def mock_location_for_testing() -> Tuple[float, float]:
    """
    Return mock coordinates for testing purposes.
    These are coordinates for a typical university campus.

    Returns:
        Tuple of (latitude, longitude)
    """
    # Coordinates for a sample university location
    return (40.7128, -74.0060)  # New York coordinates as example
